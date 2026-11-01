# Approve corrected laptop restore script

- **Prompt execution date and time:** 2026-10-31 15:34:24 +01:00 (Europe/Sarajevo)
- **Original prompt:**

  > Prethodni SHA-256 odgovara očekivanom. Stari blok je uklonjen (**0 pojavljivanja**), novi postoji **tačno jednom**. PowerShell i Python sintaksa prolaze provjeru bez izvršavanja.
  >
  > Novi SHA-256:
  >
  > ```text
  > 0E8C9DAB73277408FE17A164CBCC0E8271792880FF996AF5CF1FDE6DF327D7F2
  > ```
  >
  > ```diff
  > --- a/outputs/Obnovi-Wiki-Greblje-Laptop.ps1
  > +++ b/outputs/Obnovi-Wiki-Greblje-Laptop.ps1
  > @@ -282,11 +282,13 @@
  >          try:
  >              with db.cursor() as cur:
  >                  cur.execute('CREATE EXTENSION postgis')
  > -                cur.execute('SHOW server_encoding'); encoding = cur.fetchone()[0]
  > -                cur.execute('SHOW lc_ctype'); ctype = cur.fetchone()[0]
  > -                cur.execute('SHOW lc_collate'); collate = cur.fetchone()[0]
  > -                cur.execute('SELECT datlocprovider FROM pg_database WHERE datname=current_database()')
  > -                provider = cur.fetchone()[0]
  > +                cur.execute(
  > +                    'SELECT pg_encoding_to_char(encoding), datcollate, datctype, datlocprovider '
  > +                    'FROM pg_database WHERE datname=current_database()'
  > +                )
  > +                row = cur.fetchone()
  > +                require(row is not None, 'Nisu pronadjene postavke tekuce baze.')
  > +                encoding, collate, ctype, provider = row
  >                  require((encoding,ctype,collate,provider)==('UTF8',LOCALE,LOCALE,'c'),
  >                          'Locale nije tacno trazeni.')
  >                  cur.execute("SELECT lower(%s)=%s, lower(%s)=%s, lower(%s)=%s, replace(lower(%s),%s,%s)=%s",
  > ```
  >
  > Skripta nije izvršena. Baze, media, settings, USB i servisi nisu dirani. Jedine izmjene su navedena ispravka skripte i obavezni izvještaj `00049`. Stao sam.

## Task

Validate the exact locale-query correction and decide whether the laptop restoration script is ready for local execution.

## Changes made

- Confirmed that the obsolete `SHOW lc_ctype` and `SHOW lc_collate` statements were removed.
- Confirmed that the replacement reads encoding, collation, ctype, and locale provider from the current row in `pg_database`.
- Confirmed that the returned values are assigned consistently and that the subsequent check expects UTF-8, identical Bosnian collation and ctype values, and libc provider code `c`.
- Accepted the new script SHA-256 `0E8C9DAB73277408FE17A164CBCC0E8271792880FF996AF5CF1FDE6DF327D7F2` as the reviewed execution candidate.
- Approved one execution from an ordinary local PowerShell session on the laptop, with instructions not to rerun after any failure.
- No laptop script, database, media, settings, USB content, service, or ACL was changed from the desktop session.

## Reasons for implementation decisions

- The correction directly resolves the only blocking defect found during the complete script review.
- The script's preflight checks occur before database preservation and stop safely when the host, server, package, Git branch, free space, settings shape, or current data state differs from expectations.
- A single local execution is necessary because the Codex sandbox cannot open the laptop PostgreSQL connection, while repeated execution after a partial restore would require state-specific review.

## Related reports

- [00060_review_laptop_restore_script.md](00060_review_laptop_restore_script.md)
- [00059_request_laptop_restore_script_review.md](00059_request_laptop_restore_script_review.md)
- Follow-up execution result report: not yet created.
