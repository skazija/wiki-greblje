# 00020 - Provjera PostGIS testne baze i regresijskih testova

- Vrijeme izvršenja prompta: `2026-10-23T17:14:51+02:00` (`Europe/Sarajevo`)
- Git grana: `main`

## Originalni prompt

```text
kreirana baza i dodata ekstenzija. Sada imaju dvije ekstenzije plpqsql i postgis
```

## Opis zadatka

Provjeriti ručno kreiranu lokalnu testnu bazu, izvršiti kompletan Django testni paket u njoj i potvrditi da razvojna baza nije izmijenjena.

## Promjene napravljene za prompt

- Potvrđeno je da je konfigurirana testna baza `test_wiki_groblje`, odvojena od razvojne baze `wiki_groblje`.
- Potvrđeno je da je vlasnik testne baze `wiki_user` i da su instalirane ekstenzije `plpgsql` i `postgis`.
- Prvo izvršenje migracija u praznoj bazi otkrilo je da migracija `0027_cemetery_editor_permissions` očekuje unaprijed kreiran `ContentType` zapis.
- Migracija `0027` izmijenjena je tako da pomoću `get_or_create` sigurno kreira ili pronalazi tip sadržaja i dozvole `view_cemetery` i `change_cemetery` prije njihovog dodjeljivanja grupi `Urednici`.
- Prije izmjene migracije kreirana je sigurnosna kopija `backups/migration-0027-before-fresh-db-fix-20261023.zip`.
- Testna baza je sačuvana za naredna izvršenja pomoću opcije `--keepdb`.

## Provjera

- Kompletan paket je pronašao i uspješno izvršio svih 31 test: `Ran 31 tests ... OK`.
- Sve migracije, uključujući popravljenu migraciju `0027`, uspješno su primijenjene u testnoj bazi.
- Grupa `Urednici` u testnoj bazi ima dozvole `change_cemetery` i `view_cemetery`.
- `python manage.py makemigrations --check --dry-run` završio je porukom `No changes detected`.
- Python provjera sintakse prolazi za postavke i izmijenjenu migraciju.
- Razvojna baza je prije i poslije testova ostala na 14 groblja, 62 groba i 66 osoba.

## Razlozi za implementacijske odluke

- `plpgsql` je standardna PostgreSQL proceduralna ekstenzija i očekivano je da postoji uz prostornu ekstenziju `postgis`.
- Migracija dozvola mora raditi u potpuno praznoj bazi jer će se isti postupak koristiti pri postavljanju projekta na laptop ili drugi novi server.
- Korišten je `get_or_create` kako bi migracija ostala sigurna i kada zapisi već postoje te kako ne bi nastali duplikati.
- Testna baza se zadržava jer aplikacijski korisnik namjerno nema opću privilegiju `CREATEDB`, a buduća testiranja su zato brža i sigurnija.

## Povezani izvještaji

- [00018 - Dopuna regresijskih testova javne pretrage](./00018_add_search_regression_tests.md)
- [00019 - Konfiguracija odvojene PostGIS testne baze](./00019_configure_postgis_test_database.md)
- Naknadni izvještaji: nema ih u trenutku nastanka ovog dokumenta.
