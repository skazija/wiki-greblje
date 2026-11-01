# Retry MapTiler secret direct write

- **Prompt execution date and time:** 2026-10-31 16:35:55 +01:00 (Europe/Sarajevo)
- **Original prompt:**

  > javlja da ključ još nedostaje

## Task

Safely retry the laptop MapTiler secret update after verifying that the prior atomic replacement did not update the original file.

## Changes made

- Determined that the previous `File.Replace` path did not complete and that its original exception was masked by the clipboard cleanup exception in `finally`.
- Confirmed that the original laptop secret file remained readable and unchanged, which is the safe failure state.
- Prepared a second desktop clipboard step with the same length and SHA-256 validation.
- Prepared a simpler laptop update that creates a timestamped backup, writes the updated JSON directly with UTF-8 encoding, immediately reparses and fingerprints the stored value, and automatically restores the backup if validation fails.
- Changed clipboard cleanup to a one-space value accepted by Windows PowerShell.
- No secret file, clipboard, server, database, media, application code, Git state, or MapTiler account was changed from the desktop session.

## Reasons for implementation decisions

- The clipboard had already been cleared by the read-only verification, so the validated value must be copied again from the desktop source.
- Direct overwrite of the existing file avoids the failing replacement mechanism and preserves the file's existing path and security descriptor.
- A pre-write backup and immediate post-write hash validation provide a recoverable operation without exposing the key.

## Related reports

- [00073_verify_maptiler_write_after_clipboard_cleanup_error.md](00073_verify_maptiler_write_after_clipboard_cleanup_error.md)
- [00072_prepare_secure_maptiler_key_transfer.md](00072_prepare_secure_maptiler_key_transfer.md)
- Follow-up map verification report: not yet created.
