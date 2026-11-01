# Review laptop PostgreSQL probe script

- **Prompt execution date and time:** 2026-10-31 13:41:06 +01:00 (Europe/Sarajevo)
- **Original prompt:**

  > evo pripreme: & {
  >     $ErrorActionPreference = 'Continue'
  >
  >     $taskRoot = 'C:\Users\Administrator\Documents\Codex\2026-10-31\nalazim-se-na-novom-laptopu-i'
  >     $taskPgCtl = 'C:\Program Files\PostgreSQL\16\bin\pg_ctl.exe'
  >     $taskPsql = 'C:\Program Files\PostgreSQL\16\bin\psql.exe'
  >     $taskData = Join-Path $taskRoot 'work\postgres-dev\data'
  >     $taskLog = Join-Path $taskRoot 'work\postgres-dev\server.log'
  >     $taskSecretsFile = Join-Path $taskRoot 'work\local-secrets.json'
  >
  >     [...full PowerShell block supplied in the prompt...]
  > }

## Task

Review the proposed PowerShell start/read-only-query/stop block for correctness and safety before the user executes it manually on the laptop.

## Changes made

- Reviewed the block without executing it.
- Confirmed the host/user guards, expected-path checks, PostgreSQL version guard, secret non-display behavior, saved/restored process environment, explicit read-only transaction, `ON_ERROR_STOP`, and conditional shutdown logic.
- Verified the intended `pg_ctl`, `psql`, `\gexec`, and read-only transaction behavior against the official PostgreSQL 16 documentation.
- Found one blocking safety gap: PostgreSQL documents that `pg_ctl -w -t 60 start` can return a nonzero timeout status while startup continues in the background and eventually succeeds. In that path, the script leaves `$taskStartedHere` false and therefore skips shutdown.
- Recommended revising the script to track every start attempt and safely detect and stop a server that becomes active after a timeout before the block is approved for execution.
- No script was executed and no laptop or desktop settings, services, databases, ACLs, or application code were changed.

## Reasons for decisions

- The diagnostic should never leave the development cluster running unintentionally after a failed or timed-out start command.
- The remaining safeguards are appropriately narrow: the script refuses a pre-existing running cluster, only issues `SELECT` statements inside a read-only transaction, restores environment variables, and stops only a cluster it started.
- Official PostgreSQL documentation explicitly warns that the start operation may continue after the `pg_ctl` timeout, so the edge case must be handled rather than treated as theoretical.
- Laptop-side report `00043` is expected for the prepared script; this desktop-side review therefore uses `00044` to preserve unique report indices.

## Related reports

- [00042_review_laptop_postgres_diagnostics.md](00042_review_laptop_postgres_diagnostics.md)
- Laptop-side reports `00040_readonly_laptop_diagnostics.md` and `00043` are not yet present in this desktop working tree.
