# Diagnose fixture integrity failure

- **Prompt execution date and time:** 2026-10-31 16:04:14 +01:00 (Europe/Sarajevo)
- **Original prompt:**

  > SHA-256 odgovara. Pokrećem ispravljenu skriptu...
  > Repozitorij: C:\Users\Administrator\Documents\Codex\2026-10-31\nalazim-se-na-novom-laptopu-i\wiki-greblje
  > ## main...origin/main
  > ?? AgentsDocs/Changes/main/00025_setup_laptop_environment.md
  > ?? AgentsDocs/Changes/main/00040_readonly_laptop_diagnostics.md
  > ?? AgentsDocs/Changes/main/00043_prepare_manual_powershell_diagnostics.md
  > ?? AgentsDocs/Changes/main/00045_revise_manual_start_cleanup.md
  > ?? AgentsDocs/Changes/main/00046_verify_usb_transfer_package.md
  > ?? AgentsDocs/Changes/main/00047_prepare_laptop_restore_fallback.md
  > ?? AgentsDocs/Changes/main/00048_review_restore_script_literals.md
  > ?? AgentsDocs/Changes/main/00049_fix_restore_locale_catalog_query.md
  > ?? AgentsDocs/Changes/main/00050_adjust_restore_status_precheck.md
  > Slobodan prostor: 263122952192 bajtova
  > pg_ctl status=3, ali server prihvata veze; identitet klastera bit ce potvrdjen SQL provjerom data_directory.
  > Potvrdjena administratorska uloga: wiki_local_admin
  > Potvrdjen data direktorij: C:\Users\Administrator\Documents\Codex\2026-10-31\nalazim-se-na-novom-laptopu-i\work\postgres-dev\data
  > Prije uvoza graves_cemetery: 0
  > Prije uvoza graves_grave: 0
  > Prije uvoza graves_person: 0
  > Prije uvoza graves_photo: 0
  > Prije uvoza graves_cemeteryphoto: 0
  > Prije uvoza graves_edithistory: 0
  > Prije uvoza graves_locationsuggestion: 0
  > Prije uvoza graves_editsuggestion: 0
  > Prije uvoza graves_personeditsuggestion: 0
  > Prije uvoza graves_comment: 0
  > Prije uvoza graves_problemreport: 0
  > FAZA: COPY_PACKAGE
  > wiki_groblje_appdata_utf8.json: SHA-256 OK
  > wiki_groblje_media.zip: SHA-256 OK
  > TRANSFER_README.md: SHA-256 OK
  > FAZA: A_PRESERVE_DATABASES
  > FAZA: A_PRESERVE_DATABASES
  > Sacuvana baza: wiki_laptop_dev_before_import_20261031_154812_082023
  > FAZA: B_CREATE_LOCALIZED_DATABASES
  > FAZA: B_CREATE_LOCALIZED_DATABASES
  > wiki_laptop_dev: UTF8; libc; Bosnian (Latin)_Bosnia & Herzegovina.1250; lower/replace = true,true,true,true
  > FAZA: B_CREATE_LOCALIZED_DATABASES
  > test_wiki_groblje: UTF8; libc; Bosnian (Latin)_Bosnia & Herzegovina.1250; lower/replace = true,true,true,true
  > FAZA: C_LOCAL_SETTINGS
  > FAZA: C_MIGRATE_AND_LOADDATA
  > Django migrate: OK
  > ZAUSTAVLJENO U FAZI: C_MIGRATE_AND_LOADDATA
  > Django loaddata nije uspio; exit=1; exceptions=django.db.utils.IntegrityError. Sirovi izlaz nije prikazan radi zastite korisnickih podataka.
  > Nema brisanja ni automatskog vracanja baza/datoteka. Nema alternativnog locale pokusaja.
  > STANJE: {"started": "2026-10-31T15:48:12.082051+01:00", "phase": "C_MIGRATE_AND_LOADDATA", "renamed_databases": {"wiki_laptop_dev": "wiki_laptop_dev_before_import_20261031_154812_082023"}, "created_databases": ["wiki_laptop_dev", "test_wiki_groblje"], "media_backup": null, "settings_backup": "C:\\Users\\Administrator\\Documents\\Codex\\2026-10-31\\nalazim-se-na-novom-laptopu-i\\wiki-greblje\\backups\\laptop-import-20261031\\wiki_local_settings-before-20261031_154812_082023.py", "completed": false, "wiki_laptop_dev_locale": {"encoding": "UTF8", "ctype": "Bosnian (Latin)_Bosnia & Herzegovina.1250", "collate": "Bosnian (Latin)_Bosnia & Herzegovina.1250", "provider": "c", "unicode_checks": [true, true, true, true]}, "test_wiki_groblje_locale": {"encoding": "UTF8", "ctype": "Bosnian (Latin)_Bosnia & Herzegovina.1250", "collate": "Bosnian (Latin)_Bosnia & Herzegovina.1250", "provider": "c", "unicode_checks": [true, true, true, true]}, "error_type": "RuntimeError", "error": "Django loaddata nije uspio; exit=1; exceptions=django.db.utils.IntegrityError. Sirovi izlaz nije prikazan radi zastite korisnickih podataka."}
  > Obnova je zaustavljena (kod 1). Ne pokretati ponovo bez pregleda prijavljenog stanja.
  > PS C:\windows\System32>

## Task

Assess the partial restoration state after a fixture `IntegrityError` and design a diagnostic that identifies the violated constraint without exposing fixture values or repeating the full restore.

## Changes made

- Confirmed that the original empty development database remains preserved as `wiki_laptop_dev_before_import_20261031_154812_082023`.
- Confirmed that the replacement development and persistent test databases were created with the correct UTF-8 Bosnian locale and that all four Unicode normalization checks passed.
- Confirmed that migrations completed, while fixture loading failed before media staging, media replacement, Django checks, or tests.
- Reviewed the repository data migrations that seed monument classification data and the migration that creates the `Urednici` group.
- Compared all seven seeded classification datasets with the transfer fixture: counts, code order, and primary keys match exactly, with no mismatches.
- Reviewed all 58 permission natural-key references in fixture groups and users; every referenced permission is declared by the current installed models.
- Prepared a focused diagnostic that invokes fixture loading only inside an outer transaction that is explicitly rolled back, and reports only exception class, SQLSTATE, constraint name, table, column, and object label/primary key when safely available.
- Did not rerun restoration, alter the laptop database, change media, modify settings, or access production from the desktop session.

## Reasons for implementation decisions

- The database is now in a deliberate partial state, so rerunning the full restoration script would create additional backups and is prohibited.
- Removing seeded classifications from the fixture without evidence would risk breaking foreign-key relationships; the offline comparison shows that their identifiers already align.
- PostgreSQL diagnostic fields identify the violated rule without requiring disclosure of the conflicting personal value from `message_detail`.
- The forced outer rollback prevents fixture rows from being committed during diagnosis; sequence counters may advance, but that does not alter application records and can be reset by a later successful `loaddata`.

## Related reports

- [00065_approve_live_cluster_precheck_fix.md](00065_approve_live_cluster_precheck_fix.md)
- [00064_confirm_live_cluster_despite_pgctl.md](00064_confirm_live_cluster_despite_pgctl.md)
- [00060_review_laptop_restore_script.md](00060_review_laptop_restore_script.md)
- Follow-up fixture repair report: not yet created.
