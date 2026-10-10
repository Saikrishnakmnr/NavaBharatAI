-- NavaBharat AI: ADDITIVE marketplace SQL. Does not alter orders, generated_assets, entitlements, music or ringtone tables.
create extension if not exists pgcrypto;
create table if not exists public.ad_campaigns (
 id uuid primary key default gen_random_uuid(),
 public_id text unique not null,
 recovery_hash text not null,
 razorpay_order_id text unique not null,
 razorpay_payment_id text,
 advertiser_name text not null,
 email text not null,
 title text not null,
 description text not null default '',
 destination_url text not null,
 video_url text not null default '',
 format text not null check (format in ('slideshow','video')),
 placement text not null check (placement in ('home','search','jobs','creator','video')),
 duration_days int not null check (duration_days in (7,30)),
 amount_inr int not null check (amount_inr > 0),
 payment_status text not null default 'unpaid' check (payment_status in ('unpaid','paid')),
 status text not null default 'awaiting_payment' check (status in ('awaiting_payment','pending_review','active','paused','rejected')),
 images text[] not null default '{}',
 created_at timestamptz not null default now(),
 paid_at timestamptz,
 starts_at timestamptz,
 ends_at timestamptz
);
create index if not exists ad_campaigns_active_idx on public.ad_campaigns(status,ends_at);
create index if not exists ad_campaigns_created_idx on public.ad_campaigns(created_at desc);
alter table public.ad_campaigns enable row level security;
revoke all on public.ad_campaigns from anon, authenticated;
grant all on public.ad_campaigns to service_role;
-- Images are uploaded by the verified payment-owner through ad-market Edge Function only.
insert into storage.buckets (id,name,public,file_size_limit,allowed_mime_types)
values ('ad-campaign-media','ad-campaign-media',false,350000,ARRAY['image/jpeg'])
on conflict (id) do nothing;
