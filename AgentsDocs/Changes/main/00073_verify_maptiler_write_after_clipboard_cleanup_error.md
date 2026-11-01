# Verify MapTiler write after clipboard cleanup error

- **Prompt execution date and time:** 2026-10-31 16:33:41 +01:00 (Europe/Sarajevo)
- **Original prompt:**

  > Set-Clipboard : Value cannot be null.
  > Parameter name: text
  > At line:77 char:9
  > +         Set-Clipboard -Value ''
  > +         ~~~~~~~~~~~~~~~~~~~~~~~
  >     + CategoryInfo          : NotSpecified: (:) [Set-Clipboard], ArgumentNullException
  >     + FullyQualifiedErrorId : System.ArgumentNullException,Microsoft.PowerShell.Commands.SetClipboardCommand

## Task

Determine whether the MapTiler secret update succeeded despite the final clipboard-clearing error and provide a non-destructive verification.

## Changes made

- Identified the error as a Windows PowerShell behavior where `Set-Clipboard -Value ''` is treated as a null value.
- Confirmed from the script order that the failing cleanup command runs in `finally`, after the validated temporary JSON replacement attempt.
- Prepared a read-only laptop verification that hashes the stored `maptiler_api_key` without displaying it and compares it with the reviewed desktop fingerprint.
- Replaced clipboard cleanup with a single-space value, which removes the key without passing a null/empty string to Windows PowerShell.
- Explicitly prohibited rerunning the secret-write block before checking the resulting file.
- No secret file, clipboard, server, database, media, code, or MapTiler account was changed from the desktop session.

## Reasons for implementation decisions

- Repeating the atomic replacement unnecessarily could create additional backups and obscure whether the first write succeeded.
- A hash comparison proves the stored value exactly matches the desktop key without disclosing it.
- The currently running Django process must still be restarted after a successful stored-value check because it captured the previous empty value at startup.

## Related reports

- [00072_prepare_secure_maptiler_key_transfer.md](00072_prepare_secure_maptiler_key_transfer.md)
- [00071_diagnose_laptop_maptiler_key.md](00071_diagnose_laptop_maptiler_key.md)
- Follow-up map verification report: not yet created.
