# Prepare laptop restore handoff

- **Prompt execution date and time:** 2026-10-31 15:18:10 +01:00 (Europe/Sarajevo)
- **Original prompt:**

  > Potvrđen laptop **MININT-B5ME0EV**. Paket u `D:\backup` prošao je provjeru.
  >
  > | Datoteka | Veličina | Rezultat |
  > |---|---:|---|
  > | `wiki_groblje_appdata_utf8.json` | 213.228 B | SHA-256 odgovara; validan JSON sa **478 objekata** |
  > | `wiki_groblje_media.zip` | 532.509.518 B | SHA-256 odgovara; **211 datoteka**, sve pod `media/` |
  > | `TRANSFER_README.md` | 2.032 B | Postoji |
  >
  > SHA-256:
  >
  > ```text
  > wiki_groblje_appdata_utf8.json
  > BD2E9D073C7E563BDDA8F9E29CD17ADE818958BFC2843DB5278DBCF372D36BBA
  >
  > wiki_groblje_media.zip
  > 642EF3156E4D64A1964D3D8567F405BF8437543FA43FC6176E3BEA4E752F641A
  >
  > TRANSFER_README.md
  > ```
  >
  > `wiki_groblje_pg18.dump` i `wiki_groblje_appdata.json` označeni su kao nepotpuni i nisu korišteni.
  >
  > Kreiran je izvještaj `AgentsDocs/Changes/main/00047_verify_usb_transfer_package.md`. Druge datoteke, baza, servisi i USB sadržaj nisu mijenjani.
  >
  > Čekam sljedeću naredbu.

## Task

Review the successful laptop-side USB integrity check and prepare the safe restoration handoff for the laptop Codex GUI.

## Changes made

- Accepted the verified fixture checksum, media checksum, 478-object fixture count, and 211-file media archive count as the transfer integrity checkpoint.
- Reviewed the repository database configuration, including the explicit `test_wiki_groblje` test database name.
- Prepared a staged laptop restore instruction that preserves the current `wiki_laptop_dev` database and any existing test database by renaming rather than deleting them.
- Required creation of both development and persistent test databases with UTF-8 and the Windows Bosnian Latin locale.
- Required PostGIS enablement, migrations, fixture loading, staged media extraction, database and filesystem count verification, normalization checks, Django system checks, and the full 31-test suite using `--keepdb`.
- Added stop conditions for checksum drift, unexpected database state, unavailable locale, PostgreSQL sandbox restrictions, and any failed migration/import/test step.
- No desktop database, laptop database, media directory, USB content, or service was changed in this desktop-side handoff step.

## Reasons for implementation decisions

- The verified USB checkpoint permits restoration work to begin without repeating the transfer.
- Renaming existing databases and media provides a recoverable rollback path and avoids destructive deletion.
- The test database must also use the Bosnian locale; otherwise Django's search tests can continue failing even after the development database is corrected.
- Pre-creating the test database and running tests with `--keepdb` preserves its verified locale instead of allowing it to be recreated from the cluster's `C`-locale template.
- A staged extraction prevents a partially extracted ZIP from replacing the laptop media directory.
- The laptop Codex sandbox previously could not reliably access the local PostgreSQL socket, so the handoff explicitly requires stopping and producing a reviewable local PowerShell script rather than weakening ACLs or improvising.

## Related reports

- [00057_handoff_usb_integrity_check.md](00057_handoff_usb_integrity_check.md)
- [00056_prepare_usb_transfer_package.md](00056_prepare_usb_transfer_package.md)
- [00054_confirm_laptop_database_locale_cause.md](00054_confirm_laptop_database_locale_cause.md)
- Follow-up laptop restore report: not yet created.
