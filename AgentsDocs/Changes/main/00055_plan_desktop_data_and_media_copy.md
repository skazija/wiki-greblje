# Plan desktop data and media copy

- **Prompt execution date and time:** 2026-10-31 15:00:39 +01:00 (Europe/Sarajevo)
- **Original prompt:**

  > možeš li mi reči šta sad pokušavamo? U čemu je problem?

  Follow-up prompt:

  > možemo li mi reči šta sad pokušavamo? U čemu je problem?

  Current prompt:

  > možemo li mi reči šta sad pokušavamo? U čemu je problem?

## Task

Assess whether the desktop database and uploaded photographs can be copied to the laptop so the laptop mirrors the desktop development environment, and prepare a safe transfer strategy.

## Changes made

- Reviewed the official PostgreSQL 16 documentation for consistent `pg_dump` archives, `pg_restore`, `template0`, and locale behavior.
- Confirmed that uploaded photographs are stored under `C:\wiki-groblje\media`, which is excluded from Git.
- Measured the desktop media folder read-only: 211 files totaling 534,490,601 bytes (about 510 MiB).
- Queried the desktop database read-only without displaying credentials:
  - database: `wiki_groblje`;
  - PostgreSQL server: `18.4`;
  - PostGIS: `3.6.2`;
  - database size: approximately 32 MB;
  - locale: `Bosnian (Latin)_Bosnia & Herzegovina.1250` for both `LC_COLLATE` and `LC_CTYPE`;
  - content, confirmed independently through Django ORM and direct SQL: 14 cemeteries, 62 graves, 66 persons, 85 grave photos, and 12 cemetery photos.
- Identified a major-version compatibility constraint: the desktop source server is PostgreSQL 18, while the laptop currently has PostgreSQL 16. A direct logical restore from a PostgreSQL 18 dump into PostgreSQL 16 is not officially guaranteed.
- Recommended aligning the laptop with PostgreSQL 18 and PostGIS 3.6.2 before restoring the database, while preserving the existing PostgreSQL 16 installation until verification succeeds.
- No database dump, media archive, installation, transfer, restore, service change, or repository modification other than this report was performed.

## Reasons for decisions

- Git intentionally excludes both uploaded media and local backups, so database and media transfer must be performed outside Git.
- A custom-format `pg_dump` is portable and consistent, but restoring to an older PostgreSQL major version is not guaranteed; matching versions avoids an unnecessary migration risk.
- The database dump stores photo records and paths, while the corresponding binary image files must be copied separately from `media` with their relative directory structure intact.
- Keeping the existing laptop PostgreSQL 16 environment until the PostgreSQL 18 restore and tests pass provides a recoverable rollback path.

## Related reports

- [00054_confirm_laptop_database_locale_cause.md](00054_confirm_laptop_database_locale_cause.md)
- [00032_confirm_laptop_postgres_locale.md](00032_confirm_laptop_postgres_locale.md)
- [00029_review_laptop_setup_report.md](00029_review_laptop_setup_report.md)
