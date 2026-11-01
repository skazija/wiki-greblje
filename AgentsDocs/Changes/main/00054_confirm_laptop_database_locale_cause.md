# Confirm laptop database locale cause

- **Prompt execution date and time:** 2026-10-31 14:57:36 +01:00 (Europe/Sarajevo)
- **Original prompt:**

  > BEGIN
  >   database_name  | encoding | locale_provider | lc_collate | lc_ctype
  > -----------------+----------+-----------------+------------+----------
  >  wiki_laptop_dev | UTF8     | c               | C          | C
  > (1 row)
  >
  >  lower_s_caron | lower_z_caron | lower_d_stroke | dj_normalization
  > ---------------+---------------+----------------+------------------
  >  f             | f             | f              | f
  > (1 row)
  >
  >  public_table_count
  > --------------------
  >                  31
  > (1 row)
  >
  >  cemeteries | graves | persons | grave_photos | cemetery_photos
  > ------------+--------+---------+--------------+-----------------
  >           0 |      0 |       0 |            0 |               0
  > (1 row)
  >
  > COMMIT
  > Provjera završena. PostgreSQL nije mijenjan.

## Task

Interpret the completed laptop database probe and choose the safest repair strategy.

## Changes made

- Confirmed that `wiki_laptop_dev` uses UTF-8 encoding with the libc locale provider and `LC_COLLATE=C`, `LC_CTYPE=C`.
- Confirmed that lowercase conversion for `Š`, `Ž`, and `Đ`, plus the project's `Đ/đ` to `dj` normalization, all fail under this database locale.
- Confirmed that 31 public tables exist because migrations were applied, while the principal content tables contain zero cemeteries, graves, persons, grave photos, and cemetery photos.
- Determined that the six laptop search-test failures are caused by the database locale rather than application code.
- Recommended a recoverable repair: rename the existing laptop development and test databases as backups, create replacements under their original names from `template0` with the desktop's verified Bosnian locale, apply migrations, and rerun all 31 tests.
- No database, service, process, ACL, repository code, or application setting was changed.

## Reasons for decisions

- The failed Boolean normalization checks directly reproduce the behavior behind the failed search tests.
- Rebuilding only the two local laptop databases is less invasive than recreating the PostgreSQL cluster.
- Renaming instead of dropping preserves all current migration, reference, or authentication rows until the replacement environment is fully verified.
- The database repair changes local state and therefore requires explicit user approval before preparation or execution.

## Related reports

- [00052_fix_postgres_locale_catalog_query.md](00052_fix_postgres_locale_catalog_query.md)
- [00032_confirm_laptop_postgres_locale.md](00032_confirm_laptop_postgres_locale.md)
- [00029_review_laptop_setup_report.md](00029_review_laptop_setup_report.md)
