alter table public.media_transcriptions
  add column if not exists surah_key text,
  add column if not exists surah_name text,
  add column if not exists surah_number integer;

alter table public.media_sources
  add column if not exists surah_key text,
  add column if not exists surah_name text,
  add column if not exists surah_number integer;

update public.media_transcriptions
set surah_key = 'araf', surah_name = 'A‘râf', surah_number = 7
where surah_key is null and lower(file_name) like '%araf%';

update public.media_sources
set surah_key = 'araf', surah_name = 'A‘râf', surah_number = 7
where surah_key is null;

create index if not exists media_transcriptions_surah_idx
  on public.media_transcriptions (surah_key);

create index if not exists media_sources_surah_ayah_idx
  on public.media_sources (surah_key, ayah_start, ayah_end);
