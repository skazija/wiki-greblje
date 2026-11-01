# Prepare laptop application smoke start

- **Prompt execution date and time:** 2026-10-31 16:21:17 +01:00 (Europe/Sarajevo)
- **Original prompt:**

  > kako ćemo je pokrenuti cmd pa prebaciti se u folder itd..? Ili na neki drugi način?

## Task

Provide a simple, safe way to start the restored laptop development application for an initial browser smoke test.

## Changes made

- Chose an ordinary local PowerShell session instead of CMD or virtual-environment activation.
- Prepared one pasteable PowerShell block that validates the expected laptop, project files, PostgreSQL readiness, and local secrets before starting Django.
- The block invokes the project virtual environment's Python executable directly, sets only process-scoped environment variables, adds the laptop work directory to `PYTHONPATH`, changes to the repository directory, and starts `runserver` on `127.0.0.1:8000` with autoreload disabled.
- Included instructions to keep the terminal open while testing and use `Ctrl+C` for a controlled stop.
- No application server, database, media, settings, service, Git state, USB content, or ACL was changed from the desktop session.

## Reasons for implementation decisions

- Directly invoking `.venv\Scripts\python.exe` avoids PowerShell activation-script execution-policy issues.
- Binding to `127.0.0.1` makes the smoke-test server available only on the laptop itself.
- Disabling autoreload prevents a second process and makes startup/shutdown behavior easier to understand during the first verification.
- Loading secrets into the PowerShell process without printing them matches the existing laptop local-settings design.

## Related reports

- [00069_confirm_laptop_restore_complete.md](00069_confirm_laptop_restore_complete.md)
- [00068_approve_laptop_restore_continuation.md](00068_approve_laptop_restore_continuation.md)
- Follow-up browser smoke-test report: not yet created.
