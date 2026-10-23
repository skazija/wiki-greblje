# 00016 - Napredni filteri javne pretrage

- Vrijeme izvršenja prompta: `2026-10-23T16:25:25+02:00` (`Europe/Sarajevo`)
- Git grana: `main`

## Originalni prompt

```text
Može, idemo sa tačkom 5.
```

## Opis zadatka

Implementirati petu etapu plana javne pretrage: filtre za groblje, godine, lokaciju i stručnu klasifikaciju. Filteri trebaju raditi samostalno i zajedno s tekstualnim upitom, čuvati javna moderacijska pravila, davati međusobno dosljedne rezultate grobalja, grobova i osoba te ostati sačuvani kroz paginaciju.

## Sigurnosna kopija

- Prije izmjena kreirana je arhiva `backups/search-filters-before-20261023-162500.zip`.
- Arhiva sadrži prethodne verzije `graves/views.py`, `graves/forms.py`, `graves/tests.py`, `graves/templates/graves/search.html` i `graves/static/graves/css/modules/search.css`.
- Potvrđeno je da arhiva postoji i sadrži pet očekivanih unosa.
- Baza nije kopirana niti mijenjana jer ova etapa ne uvodi modele ni migracije.

## Promjene napravljene za prompt

### Forma i validacija

- Dodan je `SearchFilterForm` koji objedinjuje tekstualni upit i napredne GET filtre.
- Dodani su filteri za tačno groblje i tekstualnu lokaciju, pri čemu lokacija bez dijakritike pretražuje grad ili selo.
- Godine su razdvojene na raspone `rođeni od/do` i `umrli od/do`, kako bi značenje bilo jasno i kako bi se rasponi mogli kombinovati.
- Forma odbija obrnut raspon u kojem je završna godina manja od početne i prikazuje razumljivu poruku uz polje.
- Izbori groblja ograničeni su na odobrena groblja, a izbori klasifikacije na aktivne vrijednosti koje se stvarno koriste na javno odobrenim grobovima.

### Osnovna stručna klasifikacija

- Dodani su filteri za makro-tip, tradiciju, tip spomenika, stanje spomenika i položaj spomenika.
- Motivi i obrasci degradacije nisu uključeni jer ih postojeći model uloga označava kao napredna stručna polja za grupu `Stručnjaci`; njihov eventualni javni filter ostaje zasebna odluka.

### Primjena filtera

- Filteri rade i bez tekstualnog upita, pa se arhiv može pregledati samo po strukturiranim kriterijima.
- Filter groblja i lokacije primjenjuje se na groblja, grobove i osobe.
- Rasponi godina direktno filtriraju odobrene osobe, a grobovi i groblja ostaju u rezultatu samo ako sadrže istu odobrenu osobu koja zadovoljava sve odabrane raspone.
- Klasifikacijski filteri direktno filtriraju grobove, osobe kroz pripadajući grob i groblja kroz odobrene grobove.
- Kada se godina i klasifikacija kombinuju, svi uslovi moraju pripadati istom povezanom grobu odnosno istoj povezanoj osobi; rezultati se dedupliciraju prije paginacije.
- Postojeća tekstualna tokenizacija, dijakritika, rangiranje, moderacijski statusi i zasebni rezultati groblja ostali su sačuvani.

### Interfejs i paginacija

- Ispod glavnog polja dodana je sklopiva cjelina „Napredni filteri“ koja se automatski otvara kada je filter aktivan ili forma sadrži grešku.
- Prikazuje se broj aktivnih filtera, dugme za primjenu i akcija za potpuno čišćenje pretrage.
- Rezultati bez tekstualnog pojma imaju naslov „Rezultati prema odabranim filterima“.
- Sve paginacijske veze za groblja, osobe i grobove čuvaju tekstualni upit i aktivne filtere, a uklanjaju samo parametar stranice koja se mijenja.
- Dodani su pripadajući stilovi koji koriste postojeće boje, Bootstrap raspored i projektne komponente.

### Regresijski testovi

- Dodan je test filtera groblja i lokacije bez tekstualnog upita.
- Dodan je test kombinovanih raspona godine rođenja i smrti kroz sve tri grupe rezultata.
- Dodan je test validacijske greške za obrnut raspon godina.
- Dodan je test svakog od pet osnovnih klasifikacijskih filtera kroz groblja, grobove i osobe.
- Dodan je test da paginacijski query string čuva tekst i filtere, ali uklanja postojeći broj stranice.

## Provjera

- Python sintaksa `graves/forms.py`, `graves/views.py` i `graves/tests.py` uspješno je provjerena.
- `python manage.py check` završio je bez sistemskih grešaka.
- `git diff --check` nije prijavio greške u pet izmijenjenih aplikacijskih datoteka.
- Stvarni lokalni zahtjevi za lokaciju `Visoko`, odabrano groblje, raspon rođenja `1890–1900`, makro-tip i kombinaciju teksta s više filtera vratili su HTTP 200 i validne forme.
- Obrnut raspon `2000–1900` vratio je HTTP 200, nije pokrenuo pretragu i prikazao je očekivanu validacijsku grešku.
- Ranije potvrđeni upiti `1919`, `Nezir 1919`, `Hadzimejlic 1919`, `Numanagic` i `gradsko` i dalje vraćaju HTTP 200 i očekivane brojeve rezultata.
- Paginacijski parametri zadržali su `q`, lokaciju i makro-tip, a uklonili postojeći parametar stranice.
- Django test runner pronašao je 24 testa, ali ih nije izvršio jer konfigurirani PostgreSQL korisnik nema dozvolu kreirati bazu `test_wiki_groblje` (`permission denied to create database`). Aktivna razvojna ili produkcijska baza nije korištena kao zamjena.

## Naknadna korisnička provjera

- Korisnik je kombinovao lokaciju `Visoko` i donju granicu godine rođenja `1940`.
- Interfejs je vratio jedno groblje, dva groba i dvije osobe.
- Rezultat potvrđuje da se lokacijski i vremenski kriterij zajedno primjenjuju kroz sve tri povezane grupe rezultata.
- Na osnovu ove ručne provjere peta etapa plana javne pretrage smatra se funkcionalno potvrđenom.

## Razlozi za implementacijske odluke

- GET parametri omogućavaju dijeljenje, ponovno učitavanje i paginaciju filtrirane pretrage bez skrivene sesijske state logike.
- Odvojeni rasponi rođenja i smrti izbjegavaju nejasno pitanje znači li opći raspon rođenje, smrt ili preklapanje životnog vijeka.
- Povezano filtriranje sve tri vrste rezultata sprječava da filter godine ili klasifikacije ostavi nepovezana groblja i grobove u sažetku.
- Osnovna klasifikacija je uključena jer je kontrolisana i razumljiva uredničkom nivou, dok su napredna ekspertna polja namjerno ostavljena izvan javnog filtera.
- Filtri koriste postojeće modele i zato nisu potrebne migracije baze.

## Povezani izvještaji

- [00005 - Pregled javne pretrage](./00005_review_search_view.md)
- [00011 - Rangiranje rezultata pretrage](./00011_rank_search_results.md)
- [00014 - Zasebni rezultati groblja u javnoj pretrazi](./00014_add_cemetery_search_results.md)
- [00015 - Korisnička provjera rezultata groblja](./00015_verify_cemetery_search_results.md)
- Naknadni: [00017 - Korisnička provjera naprednih filtera](./00017_verify_advanced_search_filters.md)
