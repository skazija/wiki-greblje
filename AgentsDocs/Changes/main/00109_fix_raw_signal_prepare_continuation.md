# 00051 - Raw signal zastita i priprema nastavka uvoza

- Vrijeme provjere: 2026-10-31 16:13:42 CET, Europe/Sarajevo (UTC+01:00).
- Grana prema posljednjoj provjeri: main. Procitan AGENTS.md.

## Originalni prompt

```text
Ne pokreći obnovu, loaddata, testove niti PostgreSQL start/stop.

Primijeni sljedeću identičnu aplikacijsku ispravku.

1. U graves/signals.py promijeni:

@receiver(post_save, sender=Photo)
def photo_extract_gps(sender, instance, created, **kwargs):
    if not instance.image:

u:

@receiver(post_save, sender=Photo)
def photo_extract_gps(sender, instance, created, raw=False, **kwargs):
    if raw:
        return

    if not instance.image:

2. U graves/tests.py u postojeći import iz .models dodaj Photo.

Iza tog importa dodaj:

from .signals import photo_extract_gps


class PhotoSignalTests(TestCase):
    def test_photo_signal_skips_raw_fixture_loads(self):
        photo_extract_gps(
            sender=Photo,
            instance=object(),
            created=True,
            raw=True,
        )

Na desktopu ova ispravka prolazi ciljani test i cijeli paket: 32 testa, OK.

Provjeri diff i Python sintaksu bez povezivanja s bazom. Ne commituj i ne pushaj.

Zatim pripremi novu skriptu:

outputs/Nastavi-Wiki-Greblje-Laptop.ps1

Nemoj je izvršavati. Skripta mora nastaviti iz postojećeg djelimičnog stanja, a ne ponoviti početnu obnovu.

Mora:

- potvrditi laptop, korisnika, repozitorij i granu main;
- potvrditi gornju raw=True zaštitu i novi regresijski test;
- provjeriti hash lokalnog fixturea i ZIP-a;
- potvrditi da postoji rezervna baza:
  wiki_laptop_dev_before_import_20261031_154812_082023;
- potvrditi da postoje wiki_laptop_dev i test_wiki_groblje;
- SQL-om potvrditi tačan data_directory, PostgreSQL 16, UTF8, bosanski LC_COLLATE/LC_CTYPE i četiri Unicode provjere;
- potvrditi da su migracije već primijenjene i da su glavne terenske tabele još prazne;
- potvrditi da wiki_local_settings.py već koristi test_wiki_groblje i projektni media folder;
- ne preimenovati, kreirati, brisati niti ponovo migrirati baze;
- pokrenuti samo loaddata nad trenutnom wiki_laptop_dev;
- potvrditi brojeve 14 groblja, 62 groba, 66 osoba, 85 fotografija grobova i 12 fotografija groblja;
- raspakovati media prvo u novi staging folder;
- potvrditi 211 datoteka i sve baze-fajl reference;
- sačuvati postojeći media pod rezervnim imenom, bez brisanja;
- premjestiti provjereni media u projekat;
- pokrenuti manage.py check;
- pokrenuti manage.py test --keepdb --noinput i zahtijevati tačno 32 uspješna testa;
- nakon testova ponovo potvrditi brojeve razvojnih podataka;
- pri bilo kojoj grešci stati bez brisanja ili automatskog vraćanja;
- ne prikazivati tajne ni vrijednosti korisničkih podataka.

Neka provjeri PowerShell i ugrađenu Python sintaksu bez izvršavanja, prikaže diff aplikacijske izmjene, SHA-256 nastavne skripte i njen kompletan sanitizovan sadržaj radi pregleda. Kreiraj obavezni AGENTS.md izvještaj.
```

## Promjene i razlozi

- graves/signals.py: photo_extract_gps prima raw=False i odmah vraca kontrolu kada je raw=True, prije pristupa instance.image ili drugih polja. Time fixture ucitavanje preskace EXIF/GPS signal. Ocuvan je izostanak zavrsnog newlinea; konacni Git diff sadrzi samo trazenu funkcionalnu promjenu.
- graves/tests.py: dodati Photo i signal import, te identican trazeni PhotoSignalTests test. Staticki je pronadjeno 32 test metode; njihovo izvrsavanje nije radjeno.
- Kreirana zasebna outputs/Nastavi-Wiki-Greblje-Laptop.ps1. Prethodna skripta Obnovi nije mijenjana. Nastavna skripta nije izvrsena.

Nastavna skripta provjerava postojeci projekat i patch preko AST-a, lokalne hash vrijednosti, konkretnu rezervnu bazu i dvije ciljne baze. Administratorska i aplikacijska lozinka ucitavaju se u memoriju bez ispisa. Provjere preko psycopg2 koriste default_transaction_read_only=on. SQL potvrđuje data_directory, PostgreSQL 16, locale obje ciljne baze preko pg_database, Unicode i PostGIS.

Koristi stvarni wiki_local_settings iz work direktorija, koji prema procitanom trenutnom tekstu vec cilja test_wiki_groblje i projektni media. Taj modul nije mijenjan. MigrationExecutor se koristi samo za pregled primijenjenih razvojnih migracija i praznog plana; nema poziva migrate. Provjerava prazninu glavnih terenskih i pratecih korisnickih modela.

Skripta ima samo Django pozive loaddata, check i test --keepdb --noinput. Ne sadrzi SQL za CREATE/ALTER/DROP DATABASE, pg_terminate_backend, initdb, PostgreSQL start/stop ili novu obnovu. Testni runner moze obavljati svoje uobicajeno pripremanje sheme testne baze; skripta ne poziva zasebne migracije. Rezervna baza se samo provjerava i nikada ne otvara radi izmjene.

Novi media prvo ide u jedinstveni staging unutar ignorisanog lokalnog paketa. Provjerava 211 datoteka, sigurne ZIP putanje i sva neprazna FileField polja bez ispisa njihovih vrijednosti. Postojeci projektni media cuva pod jedinstvenim imenom u backups; nema brisanja. Poslije check i tacno 32 uspjesna testa ponovo provjerava razvojne brojeve. Sanitizovano stanje cuva u continue-state-<timestamp>.json. Pri gresci nema automatskog rollbacka ni ponovnog pokretanja.

## Provjera

- AST sintaksa signals.py i tests.py prolazi bez importa ili pristupa bazi.
- PowerShell Parser i ast.parse ugradjenog Python programa prolaze bez izvrsavanja.
- git diff --check prolazi; Git javlja samo informativnu LF/CRLF poruku za signals.py.
- SHA-256 nastavne skripte: 131B8285BF62FB75D6FE4930705672C8F19B1FAC1DA06583EE4FD2A95DB89C27.
- Nema literalnih lozinki ili API kljuceva u nastavnoj skripti; hash konstante nisu tajne. Prikazana kopija ne zahtijeva redakciju.
- Izvjestaj o desktop rezultatu 32 testa OK potice od korisnika. Lokalni testovi nisu izvrseni i ne tvrdi se lokalni runtime prolaz.

Nisu pokretani obnova, loaddata, check, testovi, PostgreSQL start/stop niti SQL provjere. Nisu mijenjani baza, media, settings, USB ili ACL. Nema commita, pusha ili pristupa produkciji. Izmjene su ogranicene na dva trazena aplikacijska fajla, novu nastavnu skriptu i ovaj izvjestaj.

## Povezani izvjestaji

- [Posljednja izmjena prethodne skripte](00108_adjust_restore_status_precheck.md)
- [Prvobitna priprema obnove](00105_prepare_laptop_restore_fallback.md)
- Naknadnih izvjestaja nema u trenutku pisanja.
