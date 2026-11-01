# 00050 - Ciljana izmjena pocetne pg_ctl status provjere

- Vrijeme: 2026-10-31 15:46:14 CET, Europe/Sarajevo (UTC+01:00).
- Grana prema posljednjoj provjeri: main.

## Originalni prompt

```text
Ne izvršavaj skriptu i ne pokreći niti zaustavljaj PostgreSQL.

U outputs/Obnovi-Wiki-Greblje-Laptop.ps1 prvo potvrdi da trenutni SHA-256 glasi:

0E8C9DAB73277408FE17A164CBCC0E8271792880FF996AF5CF1FDE6DF327D7F2

Pronađi tačno ovaj Python blok:

cluster_status = command([PG_BIN/'pg_ctl.exe','-D',DATA,'status'])
require(cluster_status.returncode == 0, 'Postojeci klaster ne radi; nije pokrenut ovom skriptom.')
ready = command([PG_BIN/'pg_isready.exe','-h','127.0.0.1','-p','55432','-t','5'])
require(ready.returncode == 0, 'Klaster ne prihvata veze; nema pokusaja popravke.')

Zamijeni ga tačno ovim blokom:

cluster_status = command([PG_BIN/'pg_ctl.exe','-D',DATA,'status'])
require(
    cluster_status.returncode in (0, 3),
    'Neocekivan pg_ctl status kod: ' + str(cluster_status.returncode)
)
ready = command([PG_BIN/'pg_isready.exe','-h','127.0.0.1','-p','55432','-t','5'])
require(ready.returncode == 0, 'Klaster ne prihvata veze; nema pokusaja popravke.')
if cluster_status.returncode == 3:
    say(
        'pg_ctl status=3, ali server prihvata veze; '
        'identitet klastera bit ce potvrdjen SQL provjerom data_directory.'
    )

Ne mijenjaj ništa drugo.

Nakon izmjene:

1. Potvrdi da je stari blok uklonjen i novi postoji tačno jednom.
2. Provjeri PowerShell i ugrađenu Python sintaksu bez izvršavanja.
3. Prikaži novi SHA-256.
4. Prikaži samo tačan diff s nekoliko okolnih linija.
5. Potvrdi da skripta, PostgreSQL, baze, media, settings i USB nisu izvršeni ili mijenjani, osim ove izmjene skripte i obaveznog izvještaja.
```

## Zadatak, promjena i razlog

Potvrdjen je trazeni pocetni hash. Zamijenjen je samo zadani Python blok uz ocuvanje uvlake i svih ostalih bajtova originala. Po izricitom zahtjevu status 3 vise samostalno ne odbija postupak: pg_isready i naknadna SQL provjera data_directory ostaju obavezne. Nije provjeravano runtime ponasanje niti je pokretan PostgreSQL.

## Provjere

- Prethodni SHA-256: 0E8C9DAB73277408FE17A164CBCC0E8271792880FF996AF5CF1FDE6DF327D7F2 — odgovara.
- Novi SHA-256: 834275D03BDA76C5E1247C31D9DF0853FC6FD8A3252A5A4E6ED4F3ABFDA05AA1.
- Stari blok: 0 pojavljivanja; novi blok: tacno 1.
- Python ast.parse i PowerShell Language.Parser.ParseFile prolaze bez izvrsavanja.
- Diff sadrzi samo trazenu zamjenu oko linije 166.

Jedine izmjene su skripta i ovaj obavezni izvjestaj. Skripta nije izvrsena; PostgreSQL nije pokretan/zaustavljan, a baze, media, settings i USB nisu dirani. Nema SQL-a, izmjena ACL-a, brisanja, migracija, testova, commita ili pusha.

## Povezani izvjestaji

- [Prethodna ciljana ispravka skripte](00107_fix_restore_locale_catalog_query.md)
- [Priprema skripte](00105_prepare_laptop_restore_fallback.md)
- Naknadnih izvjestaja nema u trenutku pisanja.
