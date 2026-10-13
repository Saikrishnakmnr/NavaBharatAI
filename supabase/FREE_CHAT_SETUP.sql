-- Additive only. Run once in the existing project's Supabase SQL editor.
-- Does not alter customers, purchases, music, advertisements, or existing RLS.
create table if not exists public.nava_chat_quota (
  bucket text primary key,
  hits integer not null default 0,
  expires_at timestamptz not null
);
create index if not exists nava_chat_quota_expiry on public.nava_chat_quota(expires_at);
alter table public.nava_chat_quota enable row level security;
revoke all on public.nava_chat_quota from public, anon, authenticated;
grant all on public.nava_chat_quota to service_role;

create or replace function public.nava_take_chat_quota(
  p_actor text,
  p_user_minute integer default 6,
  p_user_day integer default 60,
  p_global_minute integer default 20,
  p_global_day integer default 300
) returns boolean language plpgsql security definer set search_path = public as $$
declare
  minute_start timestamptz := date_trunc('minute', now());
  day_start timestamptz := date_trunc('day', now() at time zone 'UTC') at time zone 'UTC';
  keys text[];
  ceilings integer[];
  expiry timestamptz[];
  next_hits integer;
  i integer;
begin
  if p_actor is null or p_actor !~ '^[a-f0-9]{64}$' then return false; end if;
  -- Bounds remain enforced even if an operator accidentally misconfigures secrets.
  ceilings := array[least(greatest(coalesce(p_global_minute,20),1),1000),
                    least(greatest(coalesce(p_global_day,300),1),100000),
                    least(greatest(coalesce(p_user_minute,6),1),60),
                    least(greatest(coalesce(p_user_day,60),1),1000)];
  keys := array['global-minute:'||minute_start::text, 'global-day:'||day_start::text,
                'user-minute:'||p_actor||':'||minute_start::text, 'user-day:'||p_actor||':'||day_start::text];
  expiry := array[minute_start+interval '2 minutes',day_start+interval '2 days',
                  minute_start+interval '2 minutes',day_start+interval '2 days'];
  -- Deterministic lock order makes concurrent allowance checks atomic.
  -- The exception block rolls back all increments if any bucket is full.
  begin
    for i in 1..4 loop
      insert into public.nava_chat_quota as q(bucket,hits,expires_at)
      values(keys[i],1,expiry[i])
      on conflict(bucket) do update set hits=q.hits+1
      returning hits into next_hits;
      if next_hits>ceilings[i] then raise exception 'chat_quota_exceeded' using errcode='P0001'; end if;
    end loop;
  exception when sqlstate 'P0001' then return false;
  end;
  delete from public.nava_chat_quota where expires_at < now();
  return true;
end;
$$;
revoke all on function public.nava_take_chat_quota(text,integer,integer,integer,integer) from public,anon,authenticated;
grant execute on function public.nava_take_chat_quota(text,integer,integer,integer,integer) to service_role;
