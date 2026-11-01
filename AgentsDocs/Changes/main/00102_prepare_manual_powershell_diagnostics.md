# 00043 - Priprema rucne PowerShell dijagnostike

- Vrijeme: 2026-10-31 13:39:33, Europe/Sarajevo (CET, UTC+01:00), prema alatu za sat; dijagnosticke naredbe nisu pokretane.
- Grana prema posljednjoj provjeri: main.
- Korisnik izricito rezervise indeks 00043 jer je 00042 zauzet na desktopu.

## Originalni prompt

```text
Pripremi jedan kompletan PowerShell blok koji mogu ručno zalijepiti u obični lokalni PowerShell na laptopu pod korisnikom Administrator. Blok mora:

1. koristiti stvarne, prethodno potvrđene putanje do pg_ctl.exe, psql.exe, data direktorija i server.log;
2. pokrenuti samo postojeći PostgreSQL klaster;
3. ako pokretanje ne uspije, prikazati grešku i odmah stati bez brisanja postmaster.pid i bez drugih popravki;
4. ako uspije, izvršiti read-only SQL provjere za server_encoding, lc_ctype, lc_collate, broj korisničkih tabela i ukupan broj zapisa;
5. ne prikazivati lozinku niti sadržaj tajnih datoteka;
6. u finally dijelu uredno zaustaviti klaster samo ako je u ovom postupku uspješno pokrenut;
7. ne mijenjati ACL, konfiguraciju, kod ili bazu.

Samo pripremi i objasni blok; nemoj ga izvršavati. Za obavezni izvještaj koristi indeks 00043 jer je 00042 zauzet na desktopu.
```

## Zadatak i promjene

Pripremljen je jedan PowerShell blok za rucno izvrsavanje u obicnom lokalnom terminalu pod korisnikom Administrator. Blok nije izvrsen. Jedina izmjena u ovom koraku je ovaj izvjestaj. Nema izmjena konfiguracije, koda aplikacije, ACL-a ili baze; nema start/stop, migracija, testova, brisanja, commita ili pusha.

## Odluke i predvidjeno ponasanje

- Koriste se potvrdjene putanje C:\Program Files\PostgreSQL\16\bin\pg_ctl.exe i psql.exe, te radni korijen C:\Users\Administrator\Documents\Codex\2026-10-31\nalazim-se-na-novom-laptopu-i.
- Data: work\postgres-dev\data; log: work\postgres-dev\server.log; postojece tajne: work\local-secrets.json.
- Prije bilo kakvog pokretanja provjerava se hostname MININT-B5ME0EV, korisnik Administrator, postojece datoteke i PG_VERSION=16. pg_ctl status mora dati 3. Ako server vec radi ili status nije ocekivan, blok staje bez stop komande.
- pg_ctl -w -t 60 start koristi samo postojeci klaster. Kod greske nema ponovnog pokusaja ni popravki, i ne brise se postmaster.pid. Pokretanje se smatra uspjesnim iskljucivo nakon izlaznog koda 0.
- psql koristi eksplicitno 127.0.0.1:55432, wiki_laptop_dev i wiki_laptop, -X -w i ON_ERROR_STOP=1. Lozinka se ucitava u memoriju i ne ispisuje. Procesne varijable PGPASSWORD, PGOPTIONS, PGCLIENTENCODING i PGCONNECT_TIMEOUT vracaju se na prethodne vrijednosti u finally bloku.
- SQL koristi REPEATABLE READ, READ ONLY transakciju, prikazuje server_encoding, lc_ctype i lc_collate. Broji aplikacijske tabele van sistemskih shema, izostavlja clanove ekstenzija i particije koje roditeljska tabela vec obuhvata. SELECT count(*) rezultati se sabiraju bez prikaza redova ili licnih podataka. Isti kriteriji koriste se za broj tabela i zapisa. Psql gexec izvrsava iskljucivo generisani SELECT s citiranim identifikatorima.
- Finally poziva pg_ctl stop -m fast -w samo kada je ovaj blok uspjesno pokrenuo klaster, zatim prikazuje status. Greška zaustavljanja se prikazuje bez alternativnih postupaka.
- Start/stop PostgreSQL-a prirodno azurira operativni log, PID i interne datoteke klastera. Nema namjernih izmjena seme, aplikacijskih podataka ili postavki. Broj zapisa znaci sumu redova aplikacijskih tabela, ne broj jedinstvenih osoba.

## Provjera i ogranicenja

Pregled logike bez izvrsavanja. Nema tvrdnje da je blok runtime provjeren. Ako pg_ctl start vrati gresku, cak i nakon djelimicnog starta ili isteka cekanja, zastavica ostaje false: prema izricitom zahtjevu nema naknadnog stopa ni drugih popravki. Izlazna greska se prikazuje i postupak staje.

## Povezani izvjestaji

- [Read-only dijagnostika laptopa](00101_readonly_laptop_diagnostics.md)
- [Pocetno postavljanje laptopa](00100_setup_laptop_environment.md)
- Izvjestaj 00042 nije lokalno pregledan; korisnik navodi da je zauzet na desktopu.
- Naknadnih izvjestaja nema u trenutku pisanja.
