# Adjust read-only laptop SQL probe

- **Prompt execution date and time:** 2026-10-31 14:49:45 +01:00 (Europe/Sarajevo)
- **Original prompt:**

  > BEGIN
  >   database_name  | server_address | server_port |        server_started
  > -----------------+----------------+-------------+-------------------------------
  >  wiki_laptop_dev | 127.0.0.1      |       55432 | 2026-10-31 11:55:24.810355+01
  > (1 row)
  >
  > psql:<stdin>:8: ERROR:  permission denied to examine "data_directory"
  > DETAIL:  Only roles with privileges of the "pg_read_all_settings" role may examine this parameter.
  > GRESKA: SQL provjera nije uspjela, kod 3.
  > Provjera završena. PostgreSQL nije pokretan niti zaustavljan.

## Task

Interpret the SQL permission error and prepare the next least-privilege read-only probe.

## Changes made

- Confirmed that `wiki_laptop` can connect successfully to `wiki_laptop_dev` on `127.0.0.1:55432`.
- Confirmed that the running PostgreSQL instance started at `2026-10-31 11:55:24.810355+01`.
- Determined that the probe stopped at `SHOW data_directory` because the application role intentionally lacks `pg_read_all_settings`; no broader privilege is needed or recommended.
- Prepared a follow-up read-only probe that omits `data_directory` and retrieves encoding, locale, application-table count, and total application-row count.
- No role grants, database data, processes, services, ACLs, repository code, or application settings were changed.

## Reasons for decisions

- The data directory was already independently confirmed from the live `postgres.exe` command line, so granting `pg_read_all_settings` would unnecessarily widen the application role's privileges.
- `ON_ERROR_STOP` correctly halted the previous probe before the locale and count queries; those queries therefore need to be rerun without the restricted setting.
- The follow-up remains protected by both `default_transaction_read_only=on` and an explicit read-only transaction.

## Related reports

- [00050_confirm_live_laptop_postgres_process.md](00050_confirm_live_laptop_postgres_process.md)
- [00049_identify_unexpected_postgres_listener.md](00049_identify_unexpected_postgres_listener.md)
