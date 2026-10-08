create extension if not exists pgcrypto;
create table if not exists public.ringtones(id uuid primary key default gen_random_uuid(),title text not null,movie text,artist text,language text not null default 'English',category text not null default 'Ringtone',tags text,duration_seconds int,preview_path text,full_path text,preview_url text,source_url text,source_license text,rights_confirmed boolean not null default false,regular_price_inr int not null default 20 check(regular_price_inr>=10),price_inr int not null default 10 check(price_inr>=10),active boolean not null default true,downloads bigint not null default 0,created_at timestamptz not null default now(),updated_at timestamptz not null default now());
alter table public.ringtones add column if not exists regular_price_inr int not null default 20;
alter table public.ringtones add column if not exists price_inr int not null default 10;
create table if not exists public.generated_assets(id uuid primary key,kind text not null,storage_path text not null,preview_path text,provider text,metadata jsonb default '{}',created_at timestamptz default now());
create table if not exists public.music_library(id uuid primary key default gen_random_uuid(),title text not null,audio_path text,preview_url text,audio_url text,language text,genre text,published boolean default false,created_at timestamptz default now());
create table if not exists public.orders(id uuid primary key default gen_random_uuid(),public_order_id text unique not null,kind text not null,item_id uuid references public.ringtones(id) on delete set null,asset_id uuid references public.generated_assets(id) on delete set null,amount_inr int not null,razorpay_link_id text,razorpay_payment_id text,razorpay_status text default 'created',customer_email text,customer_data jsonb default '{}',created_at timestamptz default now(),paid_at timestamptz,downloaded_at timestamptz);
create table if not exists public.download_entitlements(id uuid primary key default gen_random_uuid(),order_id uuid references public.orders(id) on delete cascade,item_id uuid references public.ringtones(id) on delete cascade,asset_id uuid references public.generated_assets(id) on delete cascade,expires_at timestamptz not null,download_count int default 0,created_at timestamptz default now());
create table if not exists public.catalog_sources(id uuid primary key default gen_random_uuid(),name text not null,source_url text not null,license text not null,enabled boolean default true,last_import_at timestamptz);
alter table public.ringtones enable row level security;drop policy if exists "public read active ringtones" on public.ringtones;create policy "public read active ringtones" on public.ringtones for select using(active=true);
alter table public.music_library enable row level security;drop policy if exists "public read published music" on public.music_library;create policy "public read published music" on public.music_library for select using(published=true);
alter table public.generated_assets enable row level security;create policy "public read generated assets" on public.generated_assets for select using(true);
insert into public.catalog_sources(name,source_url,license) values('CC0 Ringback','https://commons.wikimedia.org/wiki/Special:Redirect/file/US_ringback_tone.ogg','CC0 1.0'),('CC0 Tone F','https://commons.wikimedia.org/wiki/Special:Redirect/file/Tone.f.ogg','CC0 1.0'),('CC0 Tone C','https://commons.wikimedia.org/wiki/Special:Redirect/file/Tone.c.ogg','CC0 1.0') on conflict do nothing;

-- Storage buckets used by the no-Streamlit application.
insert into storage.buckets(id,name,public) values
('music-library','music-library',true),
('ringtone-full','ringtone-full',false),
('ringtone-preview','ringtone-preview',false),
('generated-audio','generated-audio',false)
on conflict (id) do nothing;

-- Public playback is limited to published library rows at the database level; uploaded full ringtone
-- files remain private and are served only through signed URLs after payment.

-- Permission repair: public clients may read only public catalog/library/assets.
-- Customer writes/payments remain server-side through Edge Functions using the service role.
grant usage on schema public to anon, authenticated;
grant select on public.ringtones, public.music_library to anon, authenticated;
drop policy if exists "public read generated assets" on public.generated_assets;

-- Keep private transactional tables server-only.
revoke all on public.orders, public.download_entitlements, public.catalog_sources from anon, authenticated;
grant all on public.orders, public.download_entitlements, public.catalog_sources to service_role;
grant all on public.ringtones, public.music_library, public.generated_assets to service_role;

insert into storage.buckets(id,name,public) values
('generated-images','generated-images',false)
on conflict (id) do nothing;
