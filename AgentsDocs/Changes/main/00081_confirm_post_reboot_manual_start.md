# Confirm post-reboot manual PostgreSQL start

- **Prompt execution date and time:** 2026-11-01 11:08:14 +01:00 (Europe/Sarajevo)
- **Original prompt:**

  > === Provjera prije pokretanja ===
  > 127.0.0.1:55432 - no response
  > Potvrđen zaostali PID 6312; pg_ctl će ga obraditi.
  >
  > === Pokretanje projektnog klastera ===
  > Log: C:\Users\Administrator\Documents\Codex\2026-10-31\nalazim-se-na-novom-laptopu-i\work\postgres-dev\startup-20261101_110459.log
  > pg_ctl: another server might be running; trying to start server anyway
  > waiting for server to start....... done
  > server started
  >
  > === Završna provjera ===
  > 127.0.0.1:55432 - accepting connections
  >
  >   TCP    127.0.0.1:55432        0.0.0.0:0              LISTENING       14432
  >
  > ProcessId      : 14432
  > ExecutablePath : C:\Program Files\PostgreSQL\16\bin\postgres.exe
  > CommandLine    : "C:/Program Files/PostgreSQL/16/bin/postgres.exe"  -D "C:/Users/Administrator/Documents/Codex/2026-10-
  >                  31/nalazim-se-na-novom-laptopu-i/work/postgres-dev/data"
  >
  > USPJEH: projektni PostgreSQL je pokrenut.

## Task

Confirm the first successful project-cluster startup after a full laptop restart and choose the durable travel workflow.

## Changes made

- Confirmed that the stale PID from before reboot referred to no live process and was safely handled by `pg_ctl` without manual deletion.
- Started the exact project-owned PostgreSQL 16 data directory once from ordinary local PowerShell.
- Confirmed that the server accepts connections on `127.0.0.1:55432` under new parent PID 14432.
- Confirmed from the executable and command line that the listener uses the expected PostgreSQL binary and laptop project data directory.
- Selected a workspace-local, one-click launcher as the next implementation instead of registering a broad Windows service or changing system ACLs.
- No database schema/data, media, application code, secret, Git state, Windows service, task scheduler, or ACL was changed.

## Reasons for implementation decisions

- The successful post-reboot startup proves the cluster is healthy and that only startup orchestration is missing.
- A launcher can start PostgreSQL only when needed, validate the exact listener/data directory, load process-scoped secrets, and start Django without persistent system-wide privilege changes.
- Deferring automatic boot startup avoids running a development database continuously when the application is not being used.

## Related reports

- [00080_confirm_postgres_not_persistent_after_reboot.md](00080_confirm_postgres_not_persistent_after_reboot.md)
- [00079_clarify_actual_laptop_restart.md](00079_clarify_actual_laptop_restart.md)
- [00070_prepare_laptop_application_smoke_start.md](00070_prepare_laptop_application_smoke_start.md)
- Follow-up launcher report: not yet created.
