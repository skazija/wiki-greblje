# 00019 - Konfiguracija odvojene PostGIS testne baze

- Vrijeme izvršenja prompta: `2026-10-23T17:03:55+02:00` (`Europe/Sarajevo`)
- Git grana: `main`

## Originalni prompt

```text
Može. Idemo
```

## Opis zadatka

Započeti tačku 6.2: pripremiti Django da regresijske testove javne pretrage izvršava u zasebnoj lokalnoj PostgreSQL/PostGIS bazi, bez mijenjanja razvojne baze `wiki_groblje` i bez dodjeljivanja opće dozvole `CREATEDB` aplikacijskom korisniku.

## Promjene napravljene za prompt

- U `config/settings.py` uvedena je eksplicitna testna baza `test_wiki_groblje`, uz mogućnost lokalne promjene preko varijable `TEST_DB_NAME`.
- Dodana je zaštita koja odbija naziv bez prefiksa `test_`.
- Dodana je zaštita koja odbija korištenje istog naziva za razvojnu i testnu bazu.
- Prije izmjene kreirana je sigurnosna kopija `backups/test-database-config-before-20261023.zip`.
- Potvrđeno je da je lokalni PostgreSQL servis dostupan, da razvojna baza koristi korisnika bez privilegija `CREATEDB`, da PostGIS postoji u razvojnoj bazi i da testna baza još ne postoji.
- Zabilježeno je početno stanje razvojne baze: 14 groblja, 62 groba i 66 osoba.

## Preostali lokalni administrativni korak

Administrativna lozinka za lokalnog PostgreSQL korisnika `postgres` nije pohranjena za komandnu liniju. Zbog toga baza nije kreirana automatski niti je traženo da se lozinka prenosi kroz razgovor. Potrebno je kroz lokalni pgAdmin kreirati bazu `test_wiki_groblje` u vlasništvu korisnika `wiki_user` i u njoj uključiti ekstenziju `postgis`.

Nakon tog koraka treba pokrenuti testove s opcijama `--keepdb --noinput`, potvrditi prolazak 31 testa i ponovo provjeriti da broj zapisa u razvojnoj bazi nije promijenjen.

## Provjera

- `python manage.py check` prolazi bez sistemskih grešaka.
- `config/settings.py` prolazi Python provjeru sintakse.
- `git diff --check` za Django postavke ne prijavljuje greške.
- Kreiranje baze i izvršenje testova čekaju isključivo lokalni administratorski korak opisan iznad.

## Razlozi za implementacijske odluke

- Unaprijed kreirana testna baza omogućava korištenje `--keepdb` bez dodjeljivanja aplikacijskom korisniku prava da kreira proizvoljne baze.
- Eksplicitan testni naziv i dvije provjere štite razvojne i produkcijske podatke od slučajnog korištenja kao testne baze.
- PostGIS se mora uključiti prije migracija jer početne migracije projekta sadrže prostorna polja.
- Administrativna lozinka ostaje samo u lokalnom alatu korisnika i ne unosi se u projektne datoteke, terminalske naredbe ili izvještaj.

## Povezani izvještaji

- [00018 - Dopuna regresijskih testova javne pretrage](./00018_add_search_regression_tests.md)
- [00020 - Provjera PostGIS testne baze i regresijskih testova](./00020_verify_postgis_test_database.md)
