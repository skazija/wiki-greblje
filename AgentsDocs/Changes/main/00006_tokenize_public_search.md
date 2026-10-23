# 00006 - Tokenizacija javne pretrage

- Vrijeme izvršenja prompta: `2026-10-22T14:24:00+02:00` (`Europe/Sarajevo`)
- Git grana: `main`

## Originalni prompt

```text
Super. Možemo li ići dio po dio, a da prije toga kreiramo sigurnosnu kopiju. Za ovu prvu stavku razdvajanja na riječi pretpostavljam da će riješiti problem gdje recimo u slučaju da korisnik traži Numanagić Rasima, Rasim Numanagić, Rasim ili Numanagić dobije u svakom od tih pretraživanja Numanagić Rasim.
```

## Opis zadatka

Prije prve izmjene pretrage napraviti sigurnosnu kopiju datoteka u obimu promjene, a zatim uvesti pretragu po pojedinačnim riječima tako da redoslijed imena i prezimena nije važan. Posebno podržati navedeni slučaj u kojem upit `Numanagić Rasima` treba pronaći osobu pohranjenu kao `Rasim Numanagić`, bez uvođenja opće fuzzy pretrage u ovoj etapi.

## Sigurnosna kopija

- Kreirana je arhiva `backups/search-tokenization-before-20261022-142226.zip` prije izmjene aplikacijskog koda.
- Arhiva sadrži prethodne verzije `graves/views.py`, `graves/tests.py` i `graves/templates/graves/search.html`.
- Arhiva je nakon kreiranja otvorena i provjereno je da sadrži tri očekivane datoteke.
- Baza podataka nije kopirana niti mijenjana jer ova etapa ne uvodi migracije i ne mijenja podatke ni shemu.

## Promjene napravljene za prompt

- `search()` sada razdvaja uneseni upit po razmacima.
- Svaka unesena riječ mora se podudariti s najmanje jednim relevantnim poljem, dok redoslijed riječi nije važan.
- Isto pravilo primijenjeno je na rezultate osoba i grobova; riječi se mogu podudariti u različitim poljima, npr. ime i prezime ili naslov groba i naziv groblja.
- Dodan je usko ograničeni oblik prepoznavanja imena sa završnim `a`: token dužine najmanje pet znakova poput `Rasima` može se tačno podudariti sa spremljenim `Rasim`.
- Fallback koristi tačno podudaranje skraćenog oblika, pa upit `Alma` ne postaje prefiksna pretraga koja bi pronašla `Almir`.
- Sačuvani su postojeći filteri koji javnu pretragu ograničavaju na odobrene osobe, grobove i groblja.
- Dodano je šest regresijskih testova za oba redoslijeda imena, pojedinačno ime ili prezime, oblik `Rasima`, obavezno podudaranje svih tokena, izbjegavanje širokog prefiksnog podudaranja, tokene groba u različitim poljima i skrivanje neodobrene osobe.
- Predložak, modeli, migracije, konfiguracija i podaci nisu mijenjani.

## Provjera

- Python sintaksa `graves/views.py` i `graves/tests.py` uspješno je provjerena AST parserom.
- `python manage.py check` završio je bez sistemskih grešaka: `System check identified no issues (0 silenced)`.
- Django test runner pronašao je svih šest testova, ali ih nije mogao izvršiti jer konfigurirani PostgreSQL korisnik nema dozvolu za kreiranje baze `test_wiki_groblje`: `permission denied to create database`.
- Pokušaj standardne `compileall` provjere nije mogao zamijeniti postojeći `views` bytecode u `__pycache__` zbog Windows dozvole; zato je korištena provjera sintakse koja ne piše bytecode.
- Produkcijska baza nije korištena kao zamjena za testnu bazu.

## Razlozi za implementacijske odluke

- Sekvencijalni `.filter()` za svaki token daje `AND` između riječi, dok `Q(... | ...)` unutar tokena daje `OR` između polja. Tako `Rasim Numanagić` i `Numanagić Rasim` imaju isto značenje, ali `Rasim Hadžić` ne vraća Rasima Numanagića.
- Samo razdvajanje riječi ne može povezati `Rasima` sa spremljenim `Rasim`. Zbog eksplicitnog korisničkog primjera dodan je mali, kontrolisani morfološki fallback.
- Opće uklanjanje završetaka ili približno podudaranje nije uvedeno jer pripada narednoj fazi normalizacije/fuzzy pretrage i moglo bi proizvesti nepovezane rezultate.
- Statusni filteri nisu pojednostavljeni niti premješteni kako se ne bi narušila javna moderacijska pravila.

## Povezani izvještaji

- [00005 - Pregled javne pretrage](./00005_review_search_view.md)
- Naknadni izvještaji: nema ih u trenutku nastanka ovog dokumenta.
