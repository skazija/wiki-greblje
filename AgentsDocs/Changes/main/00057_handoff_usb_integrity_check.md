# Handoff USB integrity check

- **Prompt execution date and time:** 2026-10-31 15:13:39 +01:00 (Europe/Sarajevo)
- **Original prompt:**

  > Dobio sam obavijest da je stik priključen i da je saržaj u folderu d:\backup i da se čeka dalja naredba

## Task

Provide the next safe laptop-side instruction after the USB transfer package was reported at `D:\backup`.

## Changes made

- Prepared a read-only laptop-side verification step for the three intended transfer files.
- Included the expected SHA-256 hashes, fixture object count, and media archive file count.
- Explicitly prohibited use of the two incomplete artifacts from earlier export attempts.
- No database, media, USB, service, or laptop state was changed from the desktop session.

## Reasons for implementation decisions

- The active Codex environment remains the desktop repository, so laptop filesystem operations must be issued in the laptop Codex GUI.
- Verifying checksums and archive contents before any database or media change detects an incomplete or corrupted USB copy while the existing laptop environment remains untouched.
- Separating verification from restoration provides a clear checkpoint before the recoverable database replacement procedure.

## Related reports

- [00056_prepare_usb_transfer_package.md](00056_prepare_usb_transfer_package.md)
- [00054_confirm_laptop_database_locale_cause.md](00054_confirm_laptop_database_locale_cause.md)
- Follow-up laptop restore report: not yet created.
