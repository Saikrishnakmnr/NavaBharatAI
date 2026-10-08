-- NavaBharat AI permission repair
-- Run this once in Supabase SQL Editor.
-- Do NOT grant customer write access to orders or generated_assets.

grant usage on schema public to anon, authenticated;

grant select on public.ringtones to anon, authenticated;
grant select on public.music_library to anon, authenticated;
revoke all on public.generated_assets from anon, authenticated;

alter table public.ringtones enable row level security;
drop policy if exists "public read active ringtones" on public.ringtones;
create policy "public read active ringtones" on public.ringtones for select to anon, authenticated using(active=true);

alter table public.music_library enable row level security;
drop policy if exists "public read published music" on public.music_library;
create policy "public read published music" on public.music_library for select to anon, authenticated using(published=true);

alter table public.generated_assets enable row level security;
drop policy if exists "public read generated assets" on public.generated_assets;
create policy "public read generated assets" on public.generated_assets for select to anon, authenticated using(true);

-- Transactional tables stay private. Edge Functions use the service role.
revoke all on public.orders from anon, authenticated;
revoke all on public.download_entitlements from anon, authenticated;
revoke all on public.catalog_sources from anon, authenticated;

grant all on public.orders to service_role;
grant all on public.download_entitlements to service_role;
grant all on public.catalog_sources to service_role;
grant all on public.ringtones to service_role;
grant all on public.music_library to service_role;
grant all on public.generated_assets to service_role;

insert into storage.buckets(id,name,public) values
('generated-images','generated-images',false)
on conflict (id) do nothing;
