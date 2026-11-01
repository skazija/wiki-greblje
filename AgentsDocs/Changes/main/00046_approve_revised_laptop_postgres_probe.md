# Approve revised laptop PostgreSQL probe

- **Prompt execution date and time:** 2026-10-31 14:03:01 +01:00 (Europe/Sarajevo)
- **Original prompt verbatim:**

    & {
        $ErrorActionPreference = 'Continue'

        $taskRoot = 'C:\Users\Administrator\Documents\Codex\2026-10-31\nalazim-se-na-novom-laptopu-i'
        $taskBin = 'C:\Program Files\PostgreSQL\16\bin'
        $taskPgCtl = Join-Path $taskBin 'pg_ctl.exe'
        $taskPsql = Join-Path $taskBin 'psql.exe'
        $taskPgIsReady = Join-Path $taskBin 'pg_isready.exe'

        $taskData = Join-Path $taskRoot 'work\postgres-dev\data'
        $taskLog = Join-Path $taskRoot 'work\postgres-dev\server.log'
        $taskSecretsFile = Join-Path $taskRoot 'work\local-secrets.json'

        $taskInitiallyStopped = $false
        $taskStartAttempted = $false
        $taskStartSucceeded = $false
        $taskStartCode = $null
        $taskPostStartStatus = $null
        $taskReadyCode = $null
        $taskSecrets = $null

        $taskSavedEnvironment = @{}
        foreach ($taskName in @(
            'PGPASSWORD', 'PGOPTIONS',
            'PGCLIENTENCODING', 'PGCONNECT_TIMEOUT'
        )) {
            $taskSavedEnvironment[$taskName] =
                [Environment]::GetEnvironmentVariable($taskName, 'Process')
        }

        try {
            Write-Host "Hostname: $env:COMPUTERNAME"
            Write-Host "Korisnik: $env:USERNAME"
            Write-Host "Radna putanja: $((Get-Location).Path)"
            Write-Host "Postojeci klaster: $taskData"

            if ($env:COMPUTERNAME -ne 'MININT-B5ME0EV' -or
                $env:USERNAME -ne 'Administrator') {
                throw 'Neocekivani racunar ili korisnik. Postupak je zaustavljen.'
            }

            foreach ($taskPath in @(
                $taskPgCtl, $taskPsql, $taskPgIsReady,
                $taskSecretsFile, $taskLog,
                (Join-Path $taskData 'PG_VERSION')
            )) {
                if (-not (Test-Path -LiteralPath $taskPath -PathType Leaf)) {
                    throw "Ocekivana datoteka ne postoji: $taskPath"
                }
            }

            $taskVersion = (
                Get-Content -LiteralPath (Join-Path $taskData 'PG_VERSION') `
                    -Raw -ErrorAction Stop
            ).Trim()

            if ($taskVersion -ne '16') {
                throw "Neocekivana verzija klastera: $taskVersion"
            }

            # Tajna se ucitava u memoriju, bez ispisa.
            try {
                $taskSecrets = Get-Content -LiteralPath $taskSecretsFile `
                    -Raw -ErrorAction Stop |
                    ConvertFrom-Json -ErrorAction Stop

                if ([string]::IsNullOrWhiteSpace(
                    [string]$taskSecrets.db_password
                )) {
                    throw 'Nedostaje lozinka.'
                }
            }
            catch {
                throw 'Postojeca tajna nije dostupna ili nema polje db_password.'
            }

            Write-Host "`n=== Pocetni status ==="
            & $taskPgCtl -D $taskData status
            $taskInitialStatus = $LASTEXITCODE

            if ($taskInitialStatus -eq 0) {
                throw 'Klaster vec radi. Ovaj blok ga nece zaustavljati.'
            }

            if ($taskInitialStatus -ne 3) {
                throw "Neocekivan pocetni status: $taskInitialStatus"
            }

            $taskInitiallyStopped = $true

            Write-Host "`n=== Jedini pokusaj pokretanja ==="

            # Postavlja se PRIJE starta, nezavisno od njegovog rezultata.
            $taskStartAttempted = $true

            try {
                & $taskPgCtl -D $taskData -l $taskLog -w -t 60 start
                $taskStartCode = $LASTEXITCODE
                $taskStartSucceeded = ($taskStartCode -eq 0)
            }
            finally {
                # Provjera se izvrsava i nakon timeouta ili izuzetka.
                Write-Host "`n=== Stanje nakon pokusaja starta ==="

                & $taskPgCtl -D $taskData status
                $taskPostStartStatus = $LASTEXITCODE
                Write-Host "pg_ctl status kod: $taskPostStartStatus"

                & $taskPgIsReady -h 127.0.0.1 -p 55432 -t 5
                $taskReadyCode = $LASTEXITCODE
                Write-Host "pg_isready kod: $taskReadyCode"

                switch ($taskReadyCode) {
                    0 { Write-Host 'Server prihvata veze.' }
                    1 { Write-Host 'Server odgovara, ali odbija veze; moguce pokretanje.' }
                    2 { Write-Host 'Nema odgovora na navedenoj adresi i portu.' }
                    default { Write-Host 'Provjera dostupnosti nije uspjela.' }
                }
            }

            if (-not $taskStartSucceeded) {
                throw "Start nije uspjesno zavrsio (kod $taskStartCode). SQL se preskace; slijedi cleanup."
            }

            if ($taskPostStartStatus -ne 0 -or $taskReadyCode -ne 0) {
                throw 'Dostupnost nije potvrdjena. SQL se preskace; slijedi cleanup.'
            }

            $env:PGPASSWORD = [string]$taskSecrets.db_password
            $env:PGCLIENTENCODING = 'UTF8'
            $env:PGCONNECT_TIMEOUT = '5'
            $env:PGOPTIONS = '-c default_transaction_read_only=on'

            $taskSql = @'
    BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY;

    SELECT current_database() AS database_name,
           inet_server_addr() AS server_address,
           inet_server_port() AS server_port;

    SHOW server_encoding;
    SHOW lc_ctype;
    SHOW lc_collate;

    WITH app_tables AS (
        SELECT c.oid, n.nspname, c.relname
        FROM pg_class AS c
        JOIN pg_namespace AS n ON n.oid = c.relnamespace
        WHERE c.relkind IN ('r', 'p')
          AND NOT c.relispartition
          AND n.nspname <> 'information_schema'
          AND n.nspname !~ '^pg_'
          AND NOT EXISTS (
              SELECT 1
              FROM pg_depend AS d
              WHERE d.classid = 'pg_class'::regclass
                AND d.objid = c.oid
                AND d.deptype = 'e'
          )
    )
    SELECT count(*) AS application_table_count
    FROM app_tables;

    WITH app_tables AS (
        SELECT c.oid, n.nspname, c.relname
        FROM pg_class AS c
        JOIN pg_namespace AS n ON n.oid = c.relnamespace
        WHERE c.relkind IN ('r', 'p')
          AND NOT c.relispartition
          AND n.nspname <> 'information_schema'
          AND n.nspname !~ '^pg_'
          AND NOT EXISTS (
              SELECT 1
              FROM pg_depend AS d
              WHERE d.classid = 'pg_class'::regclass
                AND d.objid = c.oid
                AND d.deptype = 'e'
          )
    )
    SELECT CASE
        WHEN count(*) = 0 THEN
            'SELECT 0::bigint AS total_application_rows;'
        ELSE
            'SELECT coalesce(sum(row_count), 0) AS total_application_rows FROM ('
            || string_agg(
                format(
                    'SELECT count(*) AS row_count FROM %I.%I',
                    nspname, relname
                ),
                ' UNION ALL ' ORDER BY nspname, relname
            )
            || ') AS table_counts;'
        END
    FROM app_tables
    \gexec

    COMMIT;
    '@

            Write-Host "`n=== Read-only SQL provjere ==="

            $taskSql | & $taskPsql `
                -X -w `
                -h 127.0.0.1 -p 55432 `
                -U wiki_laptop -d wiki_laptop_dev `
                -v ON_ERROR_STOP=1 `
                -P pager=off `
                -f -

            $taskSqlCode = $LASTEXITCODE
            if ($taskSqlCode -ne 0) {
                throw "SQL provjera nije uspjela (kod $taskSqlCode)."
            }

            Write-Host 'SQL provjere su zavrsene.'
        }
        catch {
            Write-Host "`nGRESKA: $($_.Exception.Message)" -ForegroundColor Red
        }
        finally {
            # Cleanup ne zavisi od uspjesnog starta niti od SQL rezultata.
            try {
                if ($taskInitiallyStopped -and $taskStartAttempted) {
                    Write-Host "`n=== Cleanup nakon pokusaja starta ==="

                    try {
                        & $taskPgCtl -D $taskData -w -t 60 stop -m fast
                        $taskStopCode = $LASTEXITCODE

                        if ($taskStopCode -ne 0) {
                            Write-Host "pg_ctl stop kod: $taskStopCode. Slijedi provjera statusa." `
                                -ForegroundColor Yellow
                        }
                    }
                    catch {
                        Write-Host "Greska zaustavljanja: $($_.Exception.Message)" `
                            -ForegroundColor Red
                    }
                    finally {
                        Write-Host "`n=== Konacni status ==="

                        try {
                            & $taskPgCtl -D $taskData status
                            $taskFinalStatus = $LASTEXITCODE

                            if ($taskFinalStatus -eq 3) {
                                Write-Host 'Potvrdjeno: pg_ctl status = 3; server ne radi.'
                            }
                            else {
                                Write-Host "UPOZORENJE: konacni status je $taskFinalStatus, a ne 3. Zaustavljanje NIJE potvrdjeno." `
                                    -ForegroundColor Red
                            }
                        }
                        catch {
                            Write-Host "Konacni status nije moguce provjeriti: $($_.Exception.Message)" `
                                -ForegroundColor Red
                        }
                    }
                }
            }
            finally {
                # Vracanje prethodnih procesnih varijabli bez ispisa tajni.
                foreach ($taskName in $taskSavedEnvironment.Keys) {
                    [Environment]::SetEnvironmentVariable(
                        $taskName,
                        $taskSavedEnvironment[$taskName],
                        'Process'
                    )
                }

                $taskSecrets = $null
                $taskSavedEnvironment = $null
            }
        }
    }

## Task

Review the revised PowerShell probe before the user runs it manually on the laptop.

## Changes made

- Reviewed the complete revised block without executing it.
- Confirmed that it refuses to act when the cluster was already running, records the start attempt before invoking `pg_ctl`, checks both `pg_ctl status` and `pg_isready`, skips SQL unless startup and readiness are confirmed, and always enters cleanup after an attempted start.
- Confirmed that the SQL session uses a read-only default plus an explicit repeatable-read, read-only transaction, and that `ON_ERROR_STOP` applies to generated `\gexec` statements.
- Confirmed that the process-level PostgreSQL environment variables are restored and that the password is never printed or embedded in the command text.
- Approved the block for one controlled manual run from an ordinary local PowerShell session on the laptop, with the condition that the user must copy the complete output and must not rerun if the final status is anything other than 3.
- No script was executed and no laptop or desktop settings, services, databases, ACLs, or application code were changed.

## Reasons for decisions

- The previous timeout cleanup gap is closed because cleanup now depends on the recorded attempt, not only on a successful start.
- The initial status gate prevents the block from intentionally stopping a cluster that was already running before the probe.
- A final `pg_ctl status = 3` is the required confirmation that the temporary diagnostic server is stopped.
- Laptop-side report `00045` is expected for the revised script; this desktop-side review therefore uses `00046`.

## Related reports

- [00044_review_laptop_postgres_probe.md](00044_review_laptop_postgres_probe.md)
- Laptop-side reports `00040`, `00043`, and `00045` are not yet present in this desktop working tree.
