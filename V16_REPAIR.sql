-- NavaBharat AI V16 one-time Supabase repair/migration.
-- Run this entire script once in Supabase SQL Editor.
-- It does NOT delete customer files or orders.

alter table public.orders add column if not exists razorpay_order_id text;
create index if not exists orders_razorpay_order_id_idx on public.orders(razorpay_order_id);

alter table public.ringtones enable row level security;
alter table public.music_library enable row level security;
alter table public.generated_assets enable row level security;
alter table public.orders enable row level security;
alter table public.download_entitlements enable row level security;

drop policy if exists "public read active ringtones" on public.ringtones;
create policy "public read active ringtones" on public.ringtones for select using(active=true);

drop policy if exists "public read published music" on public.music_library;
create policy "public read published music" on public.music_library for select using(published=true);

drop policy if exists "public read generated assets" on public.generated_assets;

grant usage on schema public to anon, authenticated;
grant select on public.ringtones, public.music_library to anon, authenticated;

revoke all on public.orders, public.download_entitlements, public.generated_assets, public.catalog_sources from anon, authenticated;
grant all on public.orders, public.download_entitlements, public.generated_assets, public.catalog_sources to service_role;
grant all on public.ringtones, public.music_library to service_role;

insert into storage.buckets(id,name,public) values
('generated-images','generated-images',false)
on conflict (id) do nothing;

-- Customer preview/download files stay private.
-- Generated source files are retained; entitlement expiry only controls customer access.
