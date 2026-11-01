# Fix raw photo signal fixture import

- **Prompt execution date and time:** 2026-10-31 16:09:23 +01:00 (Europe/Sarajevo)
- **Original prompt:**

  > Brojevi prije dijagnostike: {"graves_cemetery": 0, "graves_cemeteryphoto": 0, "graves_grave": 0, "graves_person": 0, "graves_photo": 0}
  > Brojevi poslije rollbacka: {"graves_cemetery": 0, "graves_cemeteryphoto": 0, "graves_grave": 0, "graves_person": 0, "graves_photo": 0}
  > Lanac izuzetaka: IntegrityError -> UniqueViolation
  > SQLSTATE: 23505
  > Constraint: graves_locationsuggestion_pkey
  > Tabela: graves_locationsuggestion
  > Kolona: <nije dostupna>
  > Primarna poruka: duplicate key value violates unique constraint "graves_locationsuggestion_pkey"
  > Django model: graves.Photo
  > Primarni klju?: 1
  > Dijagnostika zavr?ena; fixture transakcija je poni?tena.
  > PS C:\windows\System32>

## Task

Identify why loading `graves.Photo(pk=1)` violates the `graves_locationsuggestion_pkey` constraint, implement the permanent application fix, and verify it before resuming the laptop restore.

## Changes made

- Traced `Photo` post-save behavior to `graves.signals.photo_extract_gps`.
- Confirmed that Django fixture deserialization emits `post_save` with `raw=True`, while the existing receiver ignored that flag and attempted normal EXIF/location side effects.
- Determined the exact collision mechanism: previously deserialized `LocationSuggestion` rows use explicit fixture primary keys, while the photo signal attempts to create another location suggestion before fixture sequence reset, causing a duplicate primary key.
- Updated `photo_extract_gps` to accept `raw=False` and return immediately when `raw` is true.
- Added `PhotoSignalTests.test_photo_signal_skips_raw_fixture_loads`, which supplies an object without photo attributes and proves the raw path returns before normal signal processing.
- Ran the targeted test with the existing test database: 1 test passed.
- Ran the full suite with `--keepdb --noinput`: all 32 tests passed and Django reported no system-check issues.
- Did not alter the desktop database or media, and did not modify the laptop database, media, settings, USB content, PostgreSQL process, or partial restore state.

## Reasons for implementation decisions

- Django signal receivers must avoid database queries and side effects when `raw=True`, because the database may not yet be internally consistent during fixture loading.
- Guarding the signal fixes the underlying application behavior for every future fixture import rather than editing valid location data out of the transfer fixture.
- The regression test increases the suite from 31 to 32 tests; any laptop continuation verification must therefore expect exactly 32 passing tests.
- A continuation script is required for the laptop because the original restore already preserved the old database, created localized databases, updated local settings, and ran migrations; repeating those phases would create unnecessary additional backups.

## Related reports

- [00066_diagnose_fixture_integrity_failure.md](00066_diagnose_fixture_integrity_failure.md)
- [00065_approve_live_cluster_precheck_fix.md](00065_approve_live_cluster_precheck_fix.md)
- Follow-up laptop continuation-script report: not yet created.
