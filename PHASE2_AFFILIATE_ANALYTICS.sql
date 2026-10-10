-- NavaBharat AI Phase 2. Additive, idempotent. No changes to existing orders,
-- Razorpay, music, ringtone, AI, storage buckets, or ad_campaigns.
create extension if not exists pgcrypto;
create table if not exists public.nava_affiliate_offers (
 id uuid primary key default gen_random_uuid(),
 title text not null, provider text not null, category text not null default 'Learning',
 description text not null default '', affiliate_url text not null,
 active boolean not null default false, sort_order integer not null default 100,
 created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create index if not exists nava_affiliate_offers_published_idx on public.nava_affiliate_offers(active, sort_order);
create table if not exists public.nava_site_visitors (
 day date not null, visitor_hash text not null,
 first_page text not null default 'home', created_at timestamptz not null default now(),
 primary key(day, visitor_hash)
);
create index if not exists nava_site_visitors_day_idx on public.nava_site_visitors(day);
create table if not exists public.nava_affiliate_clicks (
 day date not null, offer_id uuid not null references public.nava_affiliate_offers(id) on delete cascade,
 visitor_hash text not null, created_at timestamptz not null default now(),
 primary key(day, offer_id, visitor_hash)
);
create index if not exists nava_affiliate_clicks_day_idx on public.nava_affiliate_clicks(day);
create table if not exists public.nava_affiliate_earnings (
 id uuid primary key default gen_random_uuid(), provider text not null,
 income_type text not null default 'affiliate' check(income_type in ('affiliate','monetag','other')),
 amount_inr numeric(12,2) not null check(amount_inr>=0),
 earned_on date not null default current_date,
 reference_note text not null default '',
 confirmed boolean not null default false,
 created_at timestamptz not null default now()
);
alter table public.nava_affiliate_earnings add column if not exists income_type text not null default 'affiliate';
-- Service-role only. Public users interact solely through growth-hub Edge Function.
alter table public.nava_affiliate_offers enable row level security;
alter table public.nava_site_visitors enable row level security;
alter table public.nava_affiliate_clicks enable row level security;
alter table public.nava_affiliate_earnings enable row level security;
revoke all on public.nava_affiliate_offers, public.nava_site_visitors,
 public.nava_affiliate_clicks, public.nava_affiliate_earnings from anon, authenticated;
grant all on public.nava_affiliate_offers, public.nava_site_visitors,
 public.nava_affiliate_clicks, public.nava_affiliate_earnings to service_role;

-- Exact financial aggregates from existing paid order records. Amounts are gross,
-- before fees, refunds, taxes, chargebacks and settlement adjustments.
create or replace function public.nava_growth_financial_stats()
returns jsonb language sql stable security definer set search_path=public as $$
 select jsonb_build_object(
 'core_paid_orders', (select count(*) from public.orders where razorpay_status='paid'),
 'core_paid_gross_inr', coalesce((select sum(amount_inr) from public.orders where razorpay_status='paid'),0),
 'ad_paid_orders', (select count(*) from public.ad_campaigns where payment_status='paid'),
 'ad_paid_gross_inr', coalesce((select sum(amount_inr) from public.ad_campaigns where payment_status='paid'),0),
 'affiliate_confirmed_manual_inr', coalesce((select sum(amount_inr) from public.nava_affiliate_earnings where confirmed=true and income_type='affiliate'),0),
 'monetag_confirmed_manual_inr', coalesce((select sum(amount_inr) from public.nava_affiliate_earnings where confirmed=true and income_type='monetag'),0),
 'other_confirmed_manual_inr', coalesce((select sum(amount_inr) from public.nava_affiliate_earnings where confirmed=true and income_type='other'),0),
 'unconfirmed_manual_inr', coalesce((select sum(amount_inr) from public.nava_affiliate_earnings where confirmed=false),0)
 );
$$;
revoke all on function public.nava_growth_financial_stats() from public, anon, authenticated;
grant execute on function public.nava_growth_financial_stats() to service_role;

create or replace function public.nava_growth_traffic_stats()
returns jsonb language sql stable security definer set search_path=public as $$
 select jsonb_build_object(
 'today_unique_browsers_estimate', (select count(*) from public.nava_site_visitors where day=current_date),
 'last7_browser_days', (select count(*) from public.nava_site_visitors where day >= current_date-6),
 'last30_browser_days', (select count(*) from public.nava_site_visitors where day >= current_date-29),
 'affiliate_clicks_last30_estimate', (select count(*) from public.nava_affiliate_clicks where day >= current_date-29),
 'daily', coalesce((select jsonb_agg(jsonb_build_object('date',z.day,'visitors',z.n) order by z.day desc)
 from (select day,count(*) n from public.nava_site_visitors where day>=current_date-13 group by day) z),'[]'::jsonb)
 );
$$;
revoke all on function public.nava_growth_traffic_stats() from public, anon, authenticated;
grant execute on function public.nava_growth_traffic_stats() to service_role;
