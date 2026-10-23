# 00011 - Rangiranje rezultata pretrage

- Vrijeme izvršenja prompta: `2026-10-22T14:57:42+02:00` (`Europe/Sarajevo`)
- Git grana: `main`

## Originalni prompt

```text
super. Možemo danas da još to odradimo i da za danas završimo. Slažeš li se?
```

## Opis zadatka

Napraviti novu sigurnosnu kopiju i kao završnu etapu rada uvesti rangiranje javnih rezultata pretrage. Direktna podudaranja osobe ili naslova groba trebaju se prikazati prije djelimičnih i kontekstualnih podudaranja, bez skrivanja rezultata i bez narušavanja prethodno uvedene tokenizacije, dijakritike, oblika imena i numeričkih godina.

## Sigurnosna kopija

- Prije izmjene kreirana je arhiva `backups/search-ranking-before-20261022-145552.zip`.
- Arhiva sadrži prethodne verzije `graves/views.py`, `graves/tests.py` i `graves/templates/graves/search.html`.
- Arhiva je otvorena nakon kreiranja i potvrđeno je da sadrži sve tri očekivane datoteke.
- Baza nije kopirana niti mijenjana jer ova etapa ne uvodi migracije i izvršne provjere su samo za čitanje.

## Promjene napravljene za prompt

### Osobe

- Dodane su normalizovane izračunate vrijednosti punog imena u redoslijedu `ime prezime` i `prezime ime`.
- Osobe se rangiraju ovim redom: tačno puno ime u bilo kojem redoslijedu; tačno pojedinačno ime ili prezime; podudaranje na početku imena; djelimično podudaranje imena; ostala podudaranja poput same godine.
- Za rangiranje se koriste i kontrolisane varijante završnog `a`, pa `Numanagic Rasima` dobiva isti najviši rang kao direktan oblik `Numanagić Rasim`.
- Numerički tokeni godine ne ulaze u tekst punog imena, pa kombinacije imena i godine zadržavaju smislen poredak.

### Grobovi

- Grobovi se rangiraju ovim redom: tačan naslov; naslov koji počinje cijelim upitom; naslov koji sadrži cijeli upit; natpis koji sadrži cijeli upit; tačan ili početni naziv groblja; ostala tokenizovana podudaranja.
- Rezultati pronađeni samo kroz natpis nisu uklonjeni, nego se prikazuju poslije direktnog podudaranja naslova.
- Poredak se primjenjuje u SQL querysetu prije paginacije, tako da relevantni rezultati ne ostaju skriveni na kasnijoj stranici zbog naknadnog preslagivanja.

### Testovi

- Dodan je regresijski test koji potvrđuje da se tačno puno ime prikazuje prije dužeg djelimičnog imena.
- Dodan je regresijski test koji potvrđuje redoslijed: tačan naslov groba, podudaranje unutar naslova, zatim podudaranje samo u natpisu.
- Modeli, migracije, predložak, konfiguracija i podaci nisu mijenjani.

## Provjera

- Python sintaksa `graves/views.py` i `graves/tests.py` uspješno je provjerena.
- `python manage.py check` završio je bez sistemskih grešaka.
- Stvarni lokalni zahtjev `Numanagic` vratio je HTTP 200. Tri direktna podudaranja naslova imala su rang 2, a tri podudaranja pronađena samo u natpisu rang 3; redoslijed je ispravan.
- Stvarni lokalni zahtjev `NUMANAGIC RASIMA` vratio je HTTP 200 i očekivana osoba dobila je najviši rang 0.
- Stvarni lokalni zahtjev `1919` vratio je HTTP 200 i očekivana osoba je ostala dostupna kao rezultat godine.
- Za sve izvršene provjere potvrđeno je da su rangovi sortirani uzlazno.
- Sve provjere baze bile su samo za čitanje.
- Namjenski Django testovi nisu izvršeni kroz test runner jer konfigurirani PostgreSQL korisnik nema dozvolu kreirati `test_wiki_groblje`; stvarni lokalni HTTP zahtjevi potvrđuju izvršavanje novog SQL-a.

## Razlozi za implementacijske odluke

- Rangiranje mijenja samo redoslijed, ne skup rezultata. Time se čuva arhivska vrijednost kontekstualnih spominjanja.
- Tačna i naslovna podudaranja imaju prednost jer najvjerovatnije odgovaraju korisnikovoj namjeri.
- Stabilni sekundarni poredak po prezimenu/imenu ili ID-u osigurava predvidljive stranice kada više rezultata ima isti rang.
- Rangiranje u bazi je potrebno zbog ispravne paginacije.
- Korišteno je eksplicitno i objašnjivo `Case/When` rangiranje umjesto neprozirnog fuzzy rezultata; približna pretraga ostaje moguća buduća etapa.

## Povezani izvještaji

- [00005 - Pregled javne pretrage](./00005_review_search_view.md)
- [00006 - Tokenizacija javne pretrage](./00006_tokenize_public_search.md)
- [00007 - Normalizacija dijakritike u pretrazi](./00007_normalize_search_diacritics.md)
- [00008 - Ispravka tipa normalizacijskog izraza](./00008_fix_search_expression_output_field.md)
- [00009 - Pretraga numeričkih godina](./00009_search_numeric_years.md)
- [00010 - Procjena kontekstualnih rezultata grobova](./00010_review_contextual_grave_results.md)
- [00012 - Ispravka rangiranja upita koji sadrži samo godinu](./00012_fix_year_only_search_ranking.md)

## Naknadna napomena

Lokalni razvojni server prijavio je `ValueError: An empty Q() can't be used as a When() condition` za upit `1919`. Naknadna ispravka u izvještaju `00012` potpuno uklanja prazne `Q()` početne vrijednosti i za upit bez tekstualnog imena preskače `Case/When` izraz.
