-- Run once in Supabase SQL Editor. Never grant public writes.
create table if not exists public.nava_prices (
 key text primary key, regular_price integer not null check(regular_price between 1 and 100000),
 offer_price integer not null check(offer_price between 1 and regular_price),
 offer_enabled boolean not null default false, offer_label text not null default '', updated_at timestamptz not null default now()
);
alter table public.nava_prices enable row level security;
revoke all on public.nava_prices from anon, authenticated;
