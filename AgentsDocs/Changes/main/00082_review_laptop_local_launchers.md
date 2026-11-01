# Review laptop local launchers

- **Prompt execution date and time:** 2026-11-01 11:37:06 +01:00 (Europe/Sarajevo)
- **Original prompt:**

  > Kreirane su obje datoteke. PowerShell parser prolazi; CMD je statički pregledan bez izvršavanja. Ništa nije pokretano, a postojeće izmjene i izvještaji su sačuvani.
  >
  > SHA-256:
  > Start-Wiki-Greblje.ps1
  > FB8858CD1BD32267515D9C32195F5B92112B4C468C39171C96B242246E7C11BE
  >
  > Start-Wiki-Greblje.cmd
  > D5773B7AEC05B7945742A9DD1C44165EC52851FC0899C02A74A465A2809F1254
  >
  > The prompt supplied the complete contents of both launchers and linked laptop report `00053_prepare_local_launchers.md`. It confirmed that neither launcher nor PostgreSQL, Django, tests, or database commands were executed and that no service, scheduled task, or startup entry was created.

## Task

Review the complete laptop PowerShell and CMD launchers and decide whether they are safe for their first local execution.

## Changes made

- Reviewed the PowerShell launcher's host/user/path/version preconditions and required-file checks.
- Reviewed its PostgreSQL readiness, listener-owner, PID-file, executable, command-line data-directory, stale-PID, single-start, timestamped-log, and post-start verification logic.
- Confirmed that it does not manually remove `postmaster.pid`, retry a failed start, stop PostgreSQL, alter ACLs, or touch unrelated PostgreSQL processes.
- Reviewed secret loading and process-scoped environment handling, including restoration in `finally` without printing secret values.
- Reviewed direct virtual-environment Python use, `manage.py check`, local-only `runserver 127.0.0.1:8000 --noreload`, and the explicit behavior of leaving PostgreSQL running after Django stops.
- Reviewed the CMD wrapper's process-scoped execution-policy bypass and error pause behavior.
- Accepted SHA-256 `FB8858CD1BD32267515D9C32195F5B92112B4C468C39171C96B242246E7C11BE` and `D5773B7AEC05B7945742A9DD1C44165EC52851FC0899C02A74A465A2809F1254` as the reviewed first-execution candidates.
- Noted that an intentional `Ctrl+C` may produce a nonzero child-process exit and cause the CMD wrapper to pause; this is harmless and keeps error output visible.
- No launcher, process, service, database, media, code, secret, Git state, ACL, task, or startup configuration was changed from the desktop session.

## Reasons for implementation decisions

- The current PostgreSQL instance was already started and verified manually after reboot, so the first launcher test exercises the identity-check and Django-start path without requiring another database start.
- The launcher's exact PID/data-directory validation prevents it from accepting an unrelated PostgreSQL server on port 55432.
- A user-invoked launcher is sufficient for travel use and avoids unnecessary persistent system-wide configuration.

## Related reports

- [00081_confirm_post_reboot_manual_start.md](00081_confirm_post_reboot_manual_start.md)
- [00080_confirm_postgres_not_persistent_after_reboot.md](00080_confirm_postgres_not_persistent_after_reboot.md)
- [00070_prepare_laptop_application_smoke_start.md](00070_prepare_laptop_application_smoke_start.md)
- Follow-up launcher execution report: not yet created.
