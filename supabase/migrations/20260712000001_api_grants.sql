grant usage on schema public to anon, authenticated, service_role;

grant select on table public.media_transcriptions to anon, authenticated;
grant select on table public.media_sources to anon, authenticated;

grant all privileges on table public.media_transcriptions to service_role;
grant all privileges on table public.media_sources to service_role;

grant usage, select on all sequences in schema public to service_role;
