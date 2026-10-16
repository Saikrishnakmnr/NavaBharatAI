-- NEW EBOOK MODULE ONLY. Does not alter existing nava_* tables or orders.
create extension if not exists pgcrypto;
create table if not exists public.nava_ebooks (
 id uuid primary key default gen_random_uuid(), title text not null, author text not null default 'RacharlaGPT', language text not null check(language in ('Telugu','English','Bilingual')),category text not null default 'General',description text not null default '', regular_price integer not null check(regular_price between 1 and 100000), offer_price integer not null check(offer_price between 1 and 100000),offer_enabled boolean not null default false,published boolean not null default false,pdf_path text,cover_path text,created_at timestamptz not null default now(),updated_at timestamptz not null default now(),check(offer_price<=regular_price));
create table if not exists public.nava_ebook_orders (
 id uuid primary key default gen_random_uuid(), public_order_id text not null unique,book_id uuid not null references public.nava_ebooks(id),book_title text not null,amount_inr integer not null check(amount_inr>0),razorpay_order_id text not null unique,razorpay_payment_id text,status text not null default 'created' check(status in ('created','paid','refund_pending','refunded')),recovery_hash text not null,customer_name text,customer_email text,paid_at timestamptz,refunded_at timestamptz,created_at timestamptz not null default now());
create table if not exists public.nava_ebook_recovery_events(id bigint generated always as identity primary key,order_id uuid references public.nava_ebook_orders(id),result text not null,created_at timestamptz not null default now());
create table if not exists public.nava_ebook_refunds(id uuid primary key default gen_random_uuid(),order_id uuid not null references public.nava_ebook_orders(id),razorpay_refund_id text unique,reason text not null,status text not null,created_at timestamptz not null default now());
create unique index if not exists nava_ebook_refund_one_per_order on public.nava_ebook_refunds(order_id);
create index if not exists nava_ebook_orders_created on public.nava_ebook_orders(created_at desc);
alter table public.nava_ebooks enable row level security;
alter table public.nava_ebook_orders enable row level security;
alter table public.nava_ebook_recovery_events enable row level security;
alter table public.nava_ebook_refunds enable row level security;
revoke all on public.nava_ebooks,public.nava_ebook_orders,public.nava_ebook_recovery_events,public.nava_ebook_refunds from anon,authenticated;
grant usage on schema public to service_role;
grant select,insert,update,delete on public.nava_ebooks,public.nava_ebook_orders,public.nava_ebook_recovery_events,public.nava_ebook_refunds to service_role;
grant usage,select on all sequences in schema public to service_role;
insert into storage.buckets(id,name,public,file_size_limit,allowed_mime_types) values('nava-ebook-pdfs','nava-ebook-pdfs',false,52428800,array['application/pdf']) on conflict(id) do update set public=false;
insert into storage.buckets(id,name,public,file_size_limit,allowed_mime_types) values('nava-ebook-covers','nava-ebook-covers',true,5242880,array['image/jpeg','image/png','image/webp']) on conflict(id) do update set public=true;
-- Public cover reads only. Writes and private PDF downloads use server-side service role.
