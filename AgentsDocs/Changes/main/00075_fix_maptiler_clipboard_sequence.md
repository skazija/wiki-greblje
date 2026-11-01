# Fix MapTiler clipboard sequence

- **Prompt execution date and time:** 2026-10-31 16:39:25 +01:00 (Europe/Sarajevo)
- **Original prompt:**

  > javlja da clipboard ne sadrži očekivani desktop ključ

## Task

Determine why the clipboard hash did not match and provide a transfer sequence that does not overwrite the key while copying commands into the remote laptop session.

## Changes made

- Identified the sequencing defect: after the desktop placed the key in the shared clipboard, copying the laptop update block from the chat replaced the key with PowerShell source text.
- Prepared a laptop receiver block that is pasted and started first, then pauses at `Read-Host` before reading the clipboard.
- Prepared a desktop sender block that validates the source key and places it in the clipboard only after the laptop receiver is already waiting.
- Required the user to return to the laptop and press Enter without copying or pasting anything else.
- Retained SHA-256 validation, timestamped backup, direct UTF-8 write, post-write validation, automatic backup restoration on failure, and accepted clipboard cleanup.
- No key, secret file, clipboard, server, database, media, code, Git state, or MapTiler account was changed from the desktop session.

## Reasons for implementation decisions

- Shared clipboard transfer can be correct while still failing if subsequent command copying overwrites its contents.
- Pausing the already-loaded laptop receiver removes the need to copy any command after the key is placed in the clipboard.
- The key value remains absent from chat, terminal output, Git, reports, and command literals.

## Related reports

- [00074_retry_maptiler_secret_direct_write.md](00074_retry_maptiler_secret_direct_write.md)
- [00073_verify_maptiler_write_after_clipboard_cleanup_error.md](00073_verify_maptiler_write_after_clipboard_cleanup_error.md)
- Follow-up map verification report: not yet created.
