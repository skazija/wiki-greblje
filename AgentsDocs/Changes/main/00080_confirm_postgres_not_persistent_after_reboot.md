# Confirm PostgreSQL is not persistent after reboot

- **Prompt execution date and time:** 2026-11-01 11:01:59 +01:00 (Europe/Sarajevo)
- **Original prompt:**

  > === PostgreSQL nakon restarta ===
  > 127.0.0.1:55432 - no response
  > pg_isready kod: 2
  >
  > === Listener 55432 ===
  > Nema listenera na portu 55432.
  >
  > === PostgreSQL procesi ===
  >
  > The output listed several inaccessible `postgres.exe` processes but no listener or command line for the project-owned cluster.
  >
  > === postmaster.pid ===
  > PID zapisan u datoteci: 6312

## Task

Interpret the genuine post-restart state and prepare the safe startup of the project-owned PostgreSQL cluster.

## Changes made

- Confirmed that the project PostgreSQL server does not start automatically after a full Windows restart.
- Confirmed that port 55432 has no listener and `pg_isready` returns code 2.
- Identified `postmaster.pid` PID 6312 as stale after reboot; no manual deletion was authorized or recommended.
- Kept unrelated PostgreSQL processes out of scope because none listens on the project port or is identified as the project data-directory parent process.
- Prepared a one-attempt local startup that first reconfirms the port is free and the stale PID is absent, uses the exact project data directory, writes to a new timestamped log, waits for startup, and verifies readiness.
- Deferred automatic startup/service/launcher design until a clean manual startup succeeds after reboot.
- No process, service, database, media, code, secret, Git state, PID file, ACL, or Windows startup configuration was changed from the desktop session.

## Reasons for implementation decisions

- A one-click project launcher is likely safer and simpler than registering a broad Windows service, but the underlying post-reboot `pg_ctl` startup must first be proven.
- The stale PID file should be handled by PostgreSQL tooling rather than deleted manually.
- A unique new log avoids the earlier append-permission problem on the pre-existing `server.log` and preserves diagnostic evidence if startup fails.

## Related reports

- [00079_clarify_actual_laptop_restart.md](00079_clarify_actual_laptop_restart.md)
- [00078_confirm_laptop_post_sleep_state.md](00078_confirm_laptop_post_sleep_state.md)
- [00050_confirm_live_laptop_postgres_process.md](00050_confirm_live_laptop_postgres_process.md)
- Follow-up launcher report: not yet created.
