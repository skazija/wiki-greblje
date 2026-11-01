# Fix PostgreSQL locale catalog query

- **Prompt execution date and time:** 2026-10-31 14:53:15 +01:00 (Europe/Sarajevo)
- **Original prompt:**

  > BEGIN
  >  server_encoding
  > -----------------
  >  UTF8
  > (1 row)
  >
  > psql:<stdin>:4: ERROR:  unrecognized configuration parameter "lc_ctype"
  > GRESKA: SQL provjera nije uspjela, kod 3.
  > Provjera završena. PostgreSQL nije mijenjan.

## Task

Correct the PostgreSQL 16 locale query and continue the least-privilege read-only database inspection.

## Changes made

- Acknowledged that `SHOW lc_ctype` and `SHOW lc_collate` were incorrect for PostgreSQL 16 because these are database catalog properties, not runtime configuration parameters.
- Verified in the official PostgreSQL 16 documentation that `pg_database.datctype` stores `LC_CTYPE`, `datcollate` stores `LC_COLLATE`, `encoding` stores the database encoding, and `datlocprovider` identifies the locale provider.
- Prepared a corrected read-only query against `pg_database`, plus Boolean Unicode case-folding checks and exact counts for the primary application data tables.
- No role privileges, server configuration, processes, databases, ACLs, or application code were changed.

## Reasons for decisions

- Querying the shared system catalog requires no unnecessary grant of `pg_read_all_settings`.
- Boolean checks for `Š`, `Ž`, and `Đ` avoid console-encoding ambiguity while directly testing the behavior involved in the failed search tests.
- The previous transaction terminated on error and did not modify the database because both the session default and explicit transaction were read-only.

## Related reports

- [00051_adjust_readonly_laptop_sql_probe.md](00051_adjust_readonly_laptop_sql_probe.md)
- [00050_confirm_live_laptop_postgres_process.md](00050_confirm_live_laptop_postgres_process.md)
