# Review laptop restore script

- **Prompt execution date and time:** 2026-10-31 15:30:15 +01:00 (Europe/Sarajevo)
- **Original prompt:**

  > Nisam našao doslovno upisane lozinke, API ključeve ili druge tajne. Redakcija nije potrebna; SHA-256 konstante u skripti su kontrolni zbirovi paketa. Skripta nije izvršena niti izmijenjena. Kreiran je samo obavezni izvještaj `00048`.
  >
  > SHA-256 originalne skripte:
  >
  > ```text
  > 9FC22D58E576135FB205CBEBC3C21270691F229171381AB2A8D6D1DCC568D196
  > ```
  >
  > Kompletan pregledani sadržaj:
  >
  > The prompt then supplied the complete, unredacted contents of `outputs/Obnovi-Wiki-Greblje-Laptop.ps1` and its complete list of directly and dynamically loaded commands and modules. The supplied script is identified by the SHA-256 above. Its relevant locale verification block was:
  >
  > ```python
  > cur.execute('SHOW server_encoding'); encoding = cur.fetchone()[0]
  > cur.execute('SHOW lc_ctype'); ctype = cur.fetchone()[0]
  > cur.execute('SHOW lc_collate'); collate = cur.fetchone()[0]
  > cur.execute('SELECT datlocprovider FROM pg_database WHERE datname=current_database()')
  > provider = cur.fetchone()[0]
  > ```

## Task

Independently review the complete laptop restoration script before authorizing execution.

## Changes made

- Reviewed the script's preconditions, secret handling, Git checks, disk-space checks, server identity checks, database preservation flow, localized database creation, PostGIS setup, Django settings adjustment, migrations, fixture import, safe ZIP extraction, media preservation, file-reference validation, Django check, persistent test database use, failure behavior, and state logging.
- Independently recalculated the desktop `TRANSFER_README.md` SHA-256 and confirmed that it matches the script constant `18CE59B24556B1152315BB26C77542DFF6569BB67898D70122BD62BEA8E5BC4E`.
- Confirmed that the referenced application models and content tables exist in the repository.
- Found one blocking defect: the new-database validation calls `SHOW lc_ctype` and `SHOW lc_collate`. The laptop's PostgreSQL 16 instance already demonstrated that `lc_ctype` is not exposed as a configuration parameter, so the script would stop after creating the first replacement database.
- Prepared an exact replacement that reads encoding, collation, ctype, and provider from `pg_database` in one query.
- Did not execute or modify the laptop script, database, media, settings, USB package, service, or ACLs.

## Reasons for implementation decisions

- The script must not be executed with a known deterministic failure after the old development database has been renamed.
- `pg_database` is the already proven source for database locale metadata on this laptop and avoids unsupported `SHOW` commands.
- All other reviewed safeguards support the requested recoverable restore: original databases and media are renamed, not deleted; failures stop without automatic rollback; and test execution uses the explicitly localized persistent database with `--keepdb`.

## Related reports

- [00059_request_laptop_restore_script_review.md](00059_request_laptop_restore_script_review.md)
- [00058_prepare_laptop_restore_handoff.md](00058_prepare_laptop_restore_handoff.md)
- [00054_confirm_laptop_database_locale_cause.md](00054_confirm_laptop_database_locale_cause.md)
- Follow-up corrected-script report: not yet created.
