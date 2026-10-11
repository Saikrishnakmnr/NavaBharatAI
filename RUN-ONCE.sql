-- Run once in Supabase SQL Editor BEFORE deploying the three purchase Edge Functions.
ALTER TABLE public.orders ADD COLUMN IF NOT EXISTS recovery_hash text;
-- Null for historical orders: their download recovery must be handled by support.
-- No email, phone or customer account is required for NEW purchases.

-- Maintenance settings, server-only writes (RLS enabled, no public grants).
CREATE TABLE IF NOT EXISTS public.nava_site_settings (
 id integer PRIMARY KEY CHECK (id=1),
 maintenance_enabled boolean NOT NULL DEFAULT false,
 maintenance_message text NOT NULL DEFAULT 'We are improving NavaBharat AI. Please visit again shortly.',
 updated_at timestamptz NOT NULL DEFAULT now()
);
INSERT INTO public.nava_site_settings(id,maintenance_enabled) VALUES(1,false) ON CONFLICT (id) DO NOTHING;
ALTER TABLE public.nava_site_settings ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.nava_site_settings FROM anon, authenticated;
