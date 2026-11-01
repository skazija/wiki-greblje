# Objašnjenje sadržaja baze na laptopu

## Vrijeme izvršenja

2026-10-31 12:23:23 +01:00 (Europe/Sarajevo)

## Originalni prompt

> prebacio sam poruku. Interesuje me situacija sa bazom podataka. Koliko znam bazu nismo prebacivali i da smo je "izbacili" iz push. Akoje tako onda laptoop neće imati nikakve podatke u bazi?

## Opis zadatka

Provjeriti šta Git prenosi na laptop, šta migracije automatski dodaju u novu PostgreSQL/PostGIS bazu i da li laptop ima stvarne razvojne ili produkcijske podatke.

## Izvršene provjere i promjene

- Potvrđeno je da aktivna aplikacija koristi PostgreSQL/PostGIS backend definisan u `config/settings.py`, a ne SQLite.
- Potvrđeno je da PostgreSQL razvojna baza, testna baza i njihovi dumpovi nisu sinhronizovani kroz Git.
- Laptopova nova baza nakon migracija sadrži strukturu tabela, Django dozvole/grupe i projektne klasifikacijske šifarnike iz data migracija `0022`, `0025` i `0027`.
- Laptop nema stvarne zapise groblja, mezara, osoba i fotografija iz desktop razvojne ili produkcijske baze, osim vlastitog lokalno kreiranog administratora.
- Desktop razvojna baza trenutno sadrži 14 groblja, 62 mezara, 66 osoba, 85 fotografija mezara i 12 fotografija groblja. Ovi zapisi nisu preneseni na laptop.
- Uočeno je da je stari `db.sqlite3` još uvijek Git-praćen iz commita `8863f32`, iako ga sadašnji PostgreSQL settings ne koriste. Laptop ga dobija kloniranjem, ali on nije aktivna baza.
- Uočena je i 61 ranije Git-praćena datoteka pod `media/`. Današnji `.gitignore` sprečava dodavanje novih media datoteka, ali ne uklanja već praćene fajlove. Nova laptop baza nema odgovarajuće zapise koji bi ih normalno povezali sa sadržajem.
- Nisu mijenjani baza, Git praćenje, media sadržaj ni aplikacijski kod. Dodan je samo ovaj izvještaj.

## Razlozi za odluke

- Treba jasno razlikovati migracije i šifarnike, koji pripadaju kodu, od stvarnih korisničkih podataka, koji pripadaju bazi.
- Stari SQLite i već praćeni media fajlovi ne uklanjaju se u okviru objašnjenja jer korisnik nije tražio čišćenje repozitorija.
- Prije kopiranja razvojnih podataka na laptop treba odlučiti da li je potreban prazan razvojni set ili kontrolisani dump desktop razvojne baze, uz zaseban prenos odgovarajućih media datoteka.

## Povezani izvještaji

- [Plan postavljanja razvojnog okruženja na laptopu](00026_plan_laptop_development_setup.md)
- [Pregled izvještaja o postavljanju laptopa](00029_review_laptop_setup_report.md)
