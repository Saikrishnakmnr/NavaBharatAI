-- EMERGENCY PERMISSION REPAIR: run in Supabase SQL Editor as database owner.
-- No public access. The Edge Functions use SUPABASE_SERVICE_ROLE_KEY.
BEGIN;
CREATE TABLE IF NOT EXISTS public.nava_site_settings (
 id integer PRIMARY KEY CHECK (id=1),
 maintenance_enabled boolean NOT NULL DEFAULT false,
 maintenance_message text NOT NULL DEFAULT 'We are improving NavaBharat AI. Please visit again shortly.',
 updated_at timestamptz NOT NULL DEFAULT now()
);
INSERT INTO public.nava_site_settings(id,maintenance_enabled) VALUES (1,false) ON CONFLICT (id) DO NOTHING;
ALTER TABLE public.nava_site_settings ENABLE ROW LEVEL SECURITY;
GRANT USAGE ON SCHEMA public TO service_role;
GRANT SELECT, INSERT, UPDATE ON TABLE public.nava_site_settings TO service_role;
REVOKE ALL ON TABLE public.nava_site_settings FROM anon, authenticated;
-- Restore live operation only if you intend to bring the public app online now.
UPDATE public.nava_site_settings SET maintenance_enabled=false,updated_at=now() WHERE id=1;
COMMIT;
SELECT id,maintenance_enabled,updated_at FROM public.nava_site_settings;
