# Handle laptop PowerShell execution policy

- **Prompt execution date and time:** 2026-10-31 15:39:35 +01:00 (Europe/Sarajevo)
- **Original prompt:**

  > kaže da ne može da pokrene skriptu pošto je disabled on this system

## Task

Provide a safe way to run the reviewed laptop restore script when the laptop's PowerShell execution policy blocks `.ps1` files.

## Changes made

- Prepared a local PowerShell command that rechecks the reviewed script SHA-256 before execution.
- Limited the execution-policy bypass to a newly launched PowerShell process by using the `-ExecutionPolicy Bypass` process argument.
- Did not recommend or perform a user-, machine-, registry-, or Group Policy execution-policy change.
- Preserved the instruction to stop and report if the script hash differs or if organizational policy still blocks execution.
- No script, database, media, settings, USB content, service, ACL, or execution policy was changed from the desktop session.

## Reasons for implementation decisions

- The script content identified by SHA-256 `0E8C9DAB73277408FE17A164CBCC0E8271792880FF996AF5CF1FDE6DF327D7F2` has already been reviewed and approved.
- A child-process-only bypass permits this one reviewed script to run without weakening the laptop's persistent PowerShell policy.
- Rechecking the hash immediately before launch prevents execution if the file changed after review.

## Related reports

- [00061_approve_corrected_laptop_restore_script.md](00061_approve_corrected_laptop_restore_script.md)
- [00060_review_laptop_restore_script.md](00060_review_laptop_restore_script.md)
- Follow-up execution result report: not yet created.
