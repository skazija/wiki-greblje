# 00025 - Izolovano razvojno okruženje na laptopu

- Vrijeme početka: 2026-10-31, Europe/Sarajevo (CET, UTC+01:00).
- Grana: main; početni commit: 181956c.

## Originalni prompt

```text
možeš li sve to uradoto korak po korak bez da se ugrozi produkcija na desktopu?
```

## Zadatak i odluke

Postaviti razvojno okruženje isključivo na laptopu MININT-B5ME0EV. Produkciji nije pristupano, nema SSH-a, deploya, pusha niti kopiranja produkcijskih podataka ili tajni.

Repozitorij je kloniran u zaseban direktorij. Zavisnosti se instaliraju u .venv koristeći Python 3.13.15. PostgreSQL 16.15 koristi zaseban klaster izvan repozitorija, sluša isključivo 127.0.0.1:55432 i ima dvije nove baze wiki_laptop_dev i test_wiki_laptop_dev s PostGIS 3.6.2. Korisnik wiki_laptop nema SUPERUSER, CREATEDB ni CREATEROLE.

Lokalni settings modul i PowerShell pokretači nalaze se izvan repozitorija. Produkcijski config/settings.py je neizmijenjen. GDAL 3.13.3 i GEOS 3.15.0 potvrđeni su direktnim učitavanjem DLL-ova iz C:\OSGeo4W. Lokalni tajni podaci čuvaju se izvan repozitorija i nisu ispisivani u izvještaj.

Postojeći Tesseract 5.5.3 ima bos, hrv, eng, srp i srp_latn jezičke podatke. Node nije potreban za postojeći projekt bez package.json.

## Provjera

Instalacija i provjere aplikacije su u toku; završni rezultat će biti dopisan.

## Povezani izvještaji

- [Odvojena PostGIS testna baza](00019_configure_postgis_test_database.md)
- [Provjera prazne baze i testova](00020_verify_postgis_test_database.md)
