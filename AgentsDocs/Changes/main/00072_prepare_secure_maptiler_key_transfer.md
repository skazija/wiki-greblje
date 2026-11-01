# Prepare secure MapTiler key transfer

- **Prompt execution date and time:** 2026-10-31 16:29:42 +01:00 (Europe/Sarajevo)
- **Original prompt:**

  > kaže da ključ nedostaje ili je prazan

## Task

Repair the laptop's missing local MapTiler key without displaying the key, committing it, or changing application code.

## Changes made

- Confirmed that the laptop `maptiler_api_key` value in `work\local-secrets.json` is missing or empty.
- Prepared a desktop PowerShell step that reads the existing `.env` key, verifies its known length and SHA-256, and places it in the synchronized clipboard without displaying it.
- Prepared a laptop PowerShell step that reads the clipboard, validates the same SHA-256 before any write, updates only `maptiler_api_key`, validates a temporary JSON file, atomically replaces `local-secrets.json`, and creates a timestamped backup.
- Included clipboard clearing and a required Django process restart so the process-scoped environment receives the repaired value.
- No key value was written to a report, chat response, terminal output, Git-tracked file, or command literal.
- No desktop or laptop secret file, application server, database, media, MapTiler account, or browser state was changed from the desktop session.

## Reasons for implementation decisions

- The map failure is caused by an absent local secret rather than a code, database, media, or locale defect.
- Hash validation ensures the clipboard contains the reviewed desktop key before the laptop secret file is changed.
- An atomic same-directory replacement plus timestamped backup protects the existing JSON from partial writes and preserves recovery.
- Restarting Django is required because the currently running process already captured the empty key in its environment and settings.

## Related reports

- [00071_diagnose_laptop_maptiler_key.md](00071_diagnose_laptop_maptiler_key.md)
- [00070_prepare_laptop_application_smoke_start.md](00070_prepare_laptop_application_smoke_start.md)
- [MapTiler and coordinate handling](../../Topics/MAPTILER_AND_COORDINATES.md)
- Follow-up map verification report: not yet created.
