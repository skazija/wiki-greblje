# Potvrda pogrešnog PostgreSQL localea na laptopu

## Vrijeme izvršenja

2026-10-31 12:36:53 +01:00 (Europe/Sarajevo)

## Originalni prompt

> Uspješna zabilježena inicijalizacija koristila je **`--encoding=UTF8 --locale=C`**.
>
> Pokretanje postojećeg klastera nije uspjelo. Tačan izlaz:
>
> ```text
> pg_ctl: another server might be running; trying to start server anyway
> pg_ctl: could not open log file "C:\Users\Administrator\Documents\Codex\2026-10-31\nalazim-se-na-novom-laptopu-i\work\postgres-dev\server.log": Permission denied
> pg_ctl start exit code: 1
> ```
>
> SQL upiti nisu izvršeni. Budući da pokretanje nije uspjelo, `stop` nije pozvan i konačno stanje klastera nije dodatno provjeravano.
>
> Nisam pokušavao alternativne popravke niti mijenjao kod, konfiguraciju, baze, podatke, izvještaje ili ACL dozvole. Zaustavio sam rad.

## Opis zadatka

Ocijeniti potvrđeni `initdb` locale i neuspjelo pokretanje PostgreSQL klastera te odrediti najmanje rizičan put ispravke laptop okruženja.

## Izvršene provjere i promjene

- Potvrđeno je da je laptop klaster inicijaliziran sa `UTF8` kodiranjem i localeom `C`.
- Locale `C` potvrđuje uzrok šest testnih neuspjeha: PostgreSQL `Lower()` ne obavlja potrebnu Unicode transformaciju bosanskih velikih slova prije aplikacijske zamjene dijakritike.
- Potvrđeno je da pokušaj pokretanja nije došao do SQL dijagnostike jer proces nije mogao otvoriti `server.log` zbog dozvola.
- Poruka da drugi server možda radi nije dovoljan dokaz aktivnog procesa. `postmaster.pid` se ne smije uklanjati bez odvojene provjere procesa i porta.
- Preporučen je najmanje destruktivan put: zadržati postojeći klaster i, nakon sigurnog pokretanja iz normalnog Windows konteksta, ponovo kreirati samo prazne razvojnu i testnu bazu s provjerenim bosanskim localeom.
- Nikakve baze, podatkovni direktoriji, PID datoteke, ACL dozvole ili aplikacijski kod nisu mijenjani. Dodan je samo ovaj izvještaj.

## Razlozi za odluke

- Desktop okruženje potvrđeno prolazi svih 31 test s localeom `Bosnian (Latin)_Bosnia & Herzegovina.1250`, pa kod ne treba mijenjati radi laptop-specifičnog `C` localea.
- Ponovno kreiranje cijelog klastera nije potrebno ako se samo dvije prazne laptop baze mogu napraviti iz `template0` s ispravnim localeom.
- Brisanje i ponovno kreiranje baza zahtijeva izričitu potvrdu korisnika i mora se izvršiti tek nakon provjere procesa, porta i stabilnog načina pokretanja PostgreSQL-a.

## Povezani izvještaji

- [Pregled laptop read-only dijagnostike](00031_review_laptop_read_only_diagnostics.md)
- [Pregled izvještaja o postavljanju laptopa](00029_review_laptop_setup_report.md)
