# Approve live-cluster precheck fix

- **Prompt execution date and time:** 2026-10-31 15:46:52 +01:00 (Europe/Sarajevo)
- **Original prompt:**

  > Početni SHA-256 je potvrđen. Stari blok ima **0 pojavljivanja**, novi **tačno 1**. PowerShell i ugrađena Python sintaksa prolaze bez izvršavanja.
  >
  > Novi SHA-256:
  >
  > ```text
  > 834275D03BDA76C5E1247C31D9DF0853FC6FD8A3252A5A4E6ED4F3ABFDA05AA1
  > ```
  >
  > ```diff
  > --- a/outputs/Obnovi-Wiki-Greblje-Laptop.ps1
  > +++ b/outputs/Obnovi-Wiki-Greblje-Laptop.ps1
  > @@ -166,9 +166,17 @@
  >
  >      # Nema start/stop komandi: postojeceg servera mora biti moguce provjeriti.
  >      cluster_status = command([PG_BIN/'pg_ctl.exe','-D',DATA,'status'])
  > -    require(cluster_status.returncode == 0, 'Postojeci klaster ne radi; nije pokrenut ovom skriptom.')
  > +    require(
  > +        cluster_status.returncode in (0, 3),
  > +        'Neocekivan pg_ctl status kod: ' + str(cluster_status.returncode)
  > +    )
  >      ready = command([PG_BIN/'pg_isready.exe','-h','127.0.0.1','-p','55432','-t','5'])
  >      require(ready.returncode == 0, 'Klaster ne prihvata veze; nema pokusaja popravke.')
  > +    if cluster_status.returncode == 3:
  > +        say(
  > +            'pg_ctl status=3, ali server prihvata veze; '
  > +            'identitet klastera bit ce potvrdjen SQL provjerom data_directory.'
  > +        )
  >      secrets = json.loads((WORK/'local-secrets.json').read_text(encoding='utf-8-sig'))
  >      admin_password = (WORK/'postgres-dev/admin-password.txt').read_text(encoding='utf-8-sig').strip()
  >      # Ime je iz ranije uspjesne initdb -U naredbe; privilegije se provjeravaju SQL-om.
  > ```
  >
  > Skripta nije izvršena. PostgreSQL, baze, media, settings i USB nisu dirani. Jedine izmjene su navedena zamjena i obavezni izvještaj `00050`.

## Task

Validate the corrected live-cluster precheck and decide whether the restoration script can be executed again after its mutation-free precheck stop.

## Changes made

- Confirmed that the old strict `pg_ctl status == 0` condition was removed.
- Confirmed that the replacement accepts only status codes 0 and 3, still requires `pg_isready == 0`, and records the known status discrepancy.
- Confirmed that the later script logic retains the stronger privileged SQL checks for the exact data directory, PostgreSQL 16, and superuser role before any package copy or database mutation.
- Accepted SHA-256 `834275D03BDA76C5E1247C31D9DF0853FC6FD8A3252A5A4E6ED4F3ABFDA05AA1` as the reviewed execution candidate.
- Approved one new local execution using a child-process-only PowerShell execution-policy bypass and an immediate hash check.
- No laptop script, database, media, settings, USB content, PostgreSQL process, service, ACL, or persistent execution policy was changed from the desktop session.

## Reasons for implementation decisions

- Direct diagnostics established that the intended cluster is live despite `pg_ctl status = 3`.
- Requiring readiness and then verifying `data_directory` through an authenticated superuser connection prevents the relaxed status check from targeting an unrelated PostgreSQL listener.
- The earlier execution stopped before the restoration state file and all material changes, so a single rerun of the corrected script is safe.

## Related reports

- [00064_confirm_live_cluster_despite_pgctl.md](00064_confirm_live_cluster_despite_pgctl.md)
- [00063_diagnose_stopped_laptop_cluster.md](00063_diagnose_stopped_laptop_cluster.md)
- [00061_approve_corrected_laptop_restore_script.md](00061_approve_corrected_laptop_restore_script.md)
- Follow-up execution result report: not yet created.
