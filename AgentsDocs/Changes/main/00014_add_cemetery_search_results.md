# 00014 - Zasebni rezultati groblja u javnoj pretrazi

- Vrijeme izvršenja prompta: `2026-10-23T15:35:31+02:00` (`Europe/Sarajevo`)
- Git grana: `main`

## Originalni prompt

```text
Može, idemo sa preostalim opcijama tačke 3.
```

## Opis zadatka

Dovršiti treću etapu plana javne pretrage tako da se odobrena groblja prikazuju kao zasebna vrsta rezultata i mogu pronaći po nazivu, gradu i selu. Spriječiti da upit koji odgovara samo nazivu groblja automatski izlista sve njegove grobove, uz očuvanje korisnih višerječnih upita u kojima naziv groblja daje kontekst stvarnom podudaranju groba.

## Sigurnosna kopija

- Prije izmjena kreirana je arhiva `backups/search-cemeteries-before-20261023-153500.zip`.
- Arhiva sadrži prethodne verzije `graves/views.py`, `graves/tests.py` i `graves/templates/graves/search.html`.
- Potvrđeno je da arhiva postoji i sadrži tri očekivana unosa.
- Baza nije kopirana niti mijenjana jer ova etapa ne uvodi migracije.

## Promjene napravljene za prompt

### Pretraga groblja

- U `search()` je dodan zaseban queryset samo za odobrena groblja.
- Naziv, grad i selo normalizuju se istom logikom za dijakritiku koja se koristi za osobe i grobove.
- Svaki token višerječnog upita mora odgovarati nazivu, gradu ili selu, pa su podržane kombinacije polja poput `Maculje Rostovo`.
- Groblja se rangiraju ovim redom: tačan naziv; naziv koji počinje upitom; naziv koji sadrži upit; tačan grad ili selo; početak grada ili sela; djelimično podudaranje lokacije; ostala tokenizovana podudaranja.
- Dodana je nezavisna paginacija groblja s deset rezultata po stranici.

### Razdvajanje groblja i grobova

- Naziv groblja ostaje kontekstualno polje za kombinovane upite grobova, primjerice `groblje kameni`.
- Queryset grobova sada dodatno zahtijeva da barem jedan token stvarno odgovara naslovu ili natpisu groba.
- Time upit koji odgovara samo nazivu groblja vraća zaseban rezultat groblja, umjesto svih povezanih grobova, bez gubitka korisnih kombinovanih upita.

### Prikaz i mapa

- Dodana je zasebna sekcija „Pronađena groblja“ iznad osoba i grobova.
- Kartica groblja prikazuje naziv, grad, selo, vezu na detalje i akciju prikaza na mapi kada lokacija postoji.
- Ukupan sažetak sada navodi broj grobalja, osoba i grobova.
- Paginacijske veze čuvaju stranice sve tri vrste rezultata.
- Groblja s trenutne stranice dodana su na mapu rezultata s vlastitim markerima, popupom i funkcijom fokusiranja.

### Regresijski testovi

- Dodani su testovi pretrage groblja po nazivu, gradu i selu bez dijakritike.
- Dodan je test rangiranja tačnog naziva prije djelimičnog naziva.
- Dodan je test nezavisne paginacije rezultata groblja.
- Dodan je test da upit samo po nazivu groblja ne izlista sve povezane grobove.
- Dodan je test koji potvrđuje da groblje na čekanju nije javno vidljivo.

## Provjera

- Python sintaksa `graves/views.py` i `graves/tests.py` uspješno je provjerena.
- `python manage.py check` završio je bez sistemskih grešaka.
- `git diff --check` nije prijavio greške u izmijenjenim aplikacijskim datotekama.
- Stvarni lokalni HTTP zahtjevi za `Novi Travnik`, `Rostovo` i `Gradsko groblje Visoko` vratili su HTTP 200, po jedno očekivano groblje, nula automatski izlistanih grobova i marker groblja.
- Stvarni višerječni zahtjev `Maculje Rostovo` vratio je očekivano groblje i potvrdio spajanje tokena preko naziva i sela.
- Django test runner pronašao je 19 testova, ali ih nije izvršio jer konfigurirani PostgreSQL korisnik nema dozvolu kreirati bazu `test_wiki_groblje` (`permission denied to create database`). Produkcijska ili aktivna razvojna baza nije korištena kao zamjena za testnu bazu.

## Naknadna korisnička provjera

- Korisnik je potvrdio da upit `gradsko` prikazuje mapu s lokacijama Gradskog groblja Visoko i gradskog groblja u Fojnici.
- Korisnik je potvrdio da upit `Visoko` vraća groblja u Visokom.
- Potvrđeno je da markeri rade i da svaki vodi na odgovarajuće odabrano groblje.
- Na osnovu ove ručne provjere treća etapa plana javne pretrage smatra se funkcionalno potvrđenom.

## Razlozi za implementacijske odluke

- Groblje je samostalan arhivski entitet i treba imati vlastiti rezultat, odvojeno od pripadajućih grobova.
- Grad i selo su strukturirana polja i pouzdanija su od pokušaja izvlačenja lokacije iz opisa.
- Uslov da barem jedan token odgovara sadržaju groba uklanja neželjeno masovno izlistavanje, ali čuva naziv groblja kao koristan kontekst u preciznijem upitu.
- Rangiranje i paginacija izvršavaju se u bazi radi stabilnog i predvidljivog redoslijeda rezultata.
- Na mapi se koriste odvojene kolekcije markera groblja i grobova kako jednaki numerički ID-jevi različitih modela ne bi prepisivali jedni druge.

## Povezani izvještaji

- [00005 - Pregled javne pretrage](./00005_review_search_view.md)
- [00006 - Tokenizacija javne pretrage](./00006_tokenize_public_search.md)
- [00007 - Normalizacija dijakritike u pretrazi](./00007_normalize_search_diacritics.md)
- [00009 - Pretraga numeričkih godina](./00009_search_numeric_years.md)
- [00011 - Rangiranje rezultata pretrage](./00011_rank_search_results.md)
- [00012 - Ispravka rangiranja upita koji sadrži samo godinu](./00012_fix_year_only_search_ranking.md)
- [00013 - Provjera završenosti etapa javne pretrage](./00013_verify_search_phases.md)
- Naknadni: [00015 - Korisnička provjera rezultata groblja](./00015_verify_cemetery_search_results.md)
