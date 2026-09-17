# Supabase schema migrations

Schema authority:

```text
GitHub repository → supabase/migrations/
```

The Magnus API **does not** run migrations at boot. Railway starts only the application process.

## Create a migration

1. Install [Supabase CLI](https://supabase.com/docs/guides/cli).
2. From the repo root:

```bash
supabase link --project-ref uktsxijrewbqjcjnrfdv
supabase migration new <descriptive_name>
```

3. Edit the new SQL file under `supabase/migrations/`.
4. Commit and push to GitHub.

## Apply to production (Supabase project `magnus-ai`)

Run from a trusted environment with database access (local machine after `supabase link`, or CI):

```bash
supabase db push
```

Do **not** use the Supabase Dashboard Table Editor as the normal schema workflow. Emergency dashboard changes must be backported into `supabase/migrations/`.

## Railway relationship

- `railway.toml` has **no** pre-deploy migration command.
- Deploy flow: apply/push migrations → deploy Railway (or push migrations immediately after merge, before relying on new schema).

## Local development

Optional Docker Postgres (`docker compose up -d db`) for tests. Apply the same migration files to local Postgres only if you mirror production schema locally; Day 1 tests only require a reachable database and `SELECT 1`.
