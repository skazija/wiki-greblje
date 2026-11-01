# 00045 - Ispravka cleanup postupka nakon pokusaja starta

- Vrijeme: 2026-10-31 13:42:33 CET, Europe/Sarajevo (UTC+01:00).
- Grana prema posljednjoj provjeri: main.
- Indeks 00045 izricito zahtijeva korisnik jer je 00044 zauzet na desktopu.

## Originalni prompt

```text
Nemoj još izvršavati blok. Potrebna je jedna sigurnosna ispravka.

PostgreSQL dokumentacija navodi da pg_ctl -w -t start može vratiti nonzero kod zbog timeouta, a pokretanje se ipak može nastaviti u pozadini. U trenutnom bloku tada $taskStartedHere ostaje false i finally preskače zaustavljanje.

Izmijeni blok tako da:

1. posebno prati da je pokušaj pokretanja izvršen;
2. početna provjera i dalje odbija rad ako klaster već radi;
3. nakon svakog pokušaja pokretanja, uključujući timeout ili drugi nonzero rezultat, provjeri da li se pokrenuti klaster aktivirao ili još pokreće;
4. ako ga je ovaj blok pokrenuo ili pokušao pokrenuti, finally mora sigurno pokušati uredno zaustavljanje i potvrditi završni status 3;
5. nikada ne zaustavlja klaster koji je radio prije pokretanja bloka;
6. ne briše postmaster.pid, ne mijenja ACL, konfiguraciju ili bazu;
7. zadrži postojeće read-only SQL zaštite i vraćanje varijabli okruženja.

Prikaži cijeli revidirani PowerShell blok, ali ga nemoj izvršavati. Za obavezni izvještaj koristi indeks 00045 jer je 00044 zauzet na desktopu.
```

## Zadatak i promjene

Pripremljen je revidirani blok u odgovoru korisniku. Nije izvrsen. Jedina lokalna izmjena je ovaj izvjestaj. Nema starta/stopa, SQL-a, migracija, testova, izmjena ACL-a/konfiguracije/koda/baze, brisanja, commita ili pusha.

## Razlozi i logika

PostgreSQL 16 dokumentacija za pg_ctl potvrđuje da start ili stop nakon isteka timeouta moze nastaviti rad u pozadini. Izvor: https://www.postgresql.org/docs/16/app-pg-ctl.html (opcija -w).

- Odvojene zastavice prate pocetni status, pokusaj starta i uspjesan rezultat starta.
- Pocetni pg_ctl status mora biti 3; status 0 ili drugi kod odbija postupak bez postavljanja zastavice za pokusaj i bez stop komande.
- Zastavica pokusaja postavlja se neposredno prije pg_ctl start. Unutrasnji finally provjerava status i pg_isready i nakon nonzero koda ili izuzetka.
- Read-only SQL se izvrsava samo ako su start, status i pg_isready uspjesni. Zadrzani su REPEATABLE READ READ ONLY, ON_ERROR_STOP, eksplicitni lokalni host/port, citanje tajne bez ispisa i prethodni kriteriji za broj tabela/redova.
- Spoljasnji finally pokusava pg_ctl stop -m fast -w nakon SVAKOG pokusaja starta, bez uslovljavanja uspjehom starta ili trenutnim statusom. Nakon toga obavezno provjerava status. Samo kod 3 se prikazuje kao potvrda da server ne radi; svaki drugi kod se jasno prijavljuje. Greska stopa ne preskace zavrsnu provjeru i ne pokrece alternativne metode.
- Vracaju se sve ranije procesne varijable okruzenja. Nema brisanja PID datoteke.

## Ogranicenja

Blok je pregledan, ali nije runtime testiran. Provjera statusa i start nisu atomski prema drugim alatima: tokom postupka niko drugi ne smije pokretati isti klaster. Pocetno aktivan klaster se ne zaustavlja. Ne tvrdi se da je stop uspio ako konacni status nije 3. U slucaju neuspjeha nema prisilnog kill-a, brisanja ili ponovnog starta. Normalan PostgreSQL start/stop prirodno azurira operativne datoteke i log; SQL ne mijenja aplikacijske podatke.

## Povezani izvjestaji

- [Prethodno pripremljeni blok](00102_prepare_manual_powershell_diagnostics.md)
- [Read-only dijagnostika](00101_readonly_laptop_diagnostics.md)
- Izvjestaj 00044 nije lokalno pregledan; korisnik navodi da je zauzet na desktopu.
- Naknadnih izvjestaja nema u trenutku pisanja.
