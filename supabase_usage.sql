-- Notely AI: per-user daily usage cap.
-- Run this once in the Supabase dashboard -> SQL Editor.
-- Until it is run, the app keeps working and simply does not enforce a cap.

create table if not exists public.usage (
    user_id uuid    not null references auth.users(id) on delete cascade,
    day     date    not null default (now() at time zone 'utc')::date,
    kind    text    not null,             -- 'transcribe' or 'ai'
    count   integer not null default 0,
    primary key (user_id, day, kind)
);

alter table public.usage enable row level security;

-- Each signed-in user can read and write only their own usage rows.
create policy "usage_select_own" on public.usage
    for select using (auth.uid() = user_id);

create policy "usage_insert_own" on public.usage
    for insert with check (auth.uid() = user_id);

create policy "usage_update_own" on public.usage
    for update using (auth.uid() = user_id) with check (auth.uid() = user_id);
