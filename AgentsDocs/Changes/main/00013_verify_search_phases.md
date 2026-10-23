# 00013 - Provjera završenosti etapa javne pretrage

- Vrijeme izvršenja prompta: `2026-10-23T15:30:43+02:00` (`Europe/Sarajevo`)
- Git grana: `main`

## Originalni prompt

```text
koliko znam završili smo dio liste od 1 do 4- Da li je tako? Ako jeste idemo onda na 5.
```

## Opis zadatka

Provjeriti u stvarnom kodu, predlošku, testovima i ranijim izvještajima jesu li završene prve četiri planirane etape poboljšanja javne pretrage. Prelazak na napredne filtre iz pete etape uslovljen je potvrdom da su prve četiri etape potpune.

## Izvršene provjere i nalaz

- Tačka 1 je implementirana: upit se dijeli na tokene i svaki token mora odgovarati barem jednom relevantnom polju osobe ili groba.
- Tačka 2 je implementirana: podržani su puno ime u oba redoslijeda, kontrolisana varijanta završnog `a`, numeričke godine i kombinacija imena s godinom.
- Tačka 4 je implementirana: osobe i grobovi rangiraju se po direktnosti podudaranja prije paginacije, a podudaranja samo u natpisu ostaju dostupna poslije direktnijih rezultata.
- Tačka 3 nije potpuno implementirana. Trenutni `search()` nema zaseban queryset, paginaciju ni prikaz rezultata groblja. Naziv groblja trenutno služi kao jedno od polja za pronalazak povezanih grobova, dok `Cemetery.city` i `Cemetery.village` nisu uključeni u tekstualnu pretragu.
- Zbog neispunjenog korisnikovog uslova nije započeta tačka 5 niti su mijenjani aplikacijski kod, predložak, stilovi, modeli, migracije ili testovi.

## Razlozi za odluku

- Zaseban rezultat groblja nije isto što i vraćanje svih grobova povezanih s grobljem čiji naziv odgovara upitu.
- Prelazak na filtre uz označavanje tačke 3 završenom ostavio bi dokumentovani funkcionalni nedostatak i pogrešno prikazao stanje plana.
- Zaštita javnih statusa i postojeće ponašanje pretrage moraju ostati očuvani kada se tačka 3 naknadno implementira.

## Povezani izvještaji

- [00005 - Pregled javne pretrage](./00005_review_search_view.md)
- [00006 - Tokenizacija javne pretrage](./00006_tokenize_public_search.md)
- [00007 - Normalizacija dijakritike u pretrazi](./00007_normalize_search_diacritics.md)
- [00009 - Pretraga numeričkih godina](./00009_search_numeric_years.md)
- [00011 - Rangiranje rezultata pretrage](./00011_rank_search_results.md)
- [00012 - Ispravka rangiranja upita koji sadrži samo godinu](./00012_fix_year_only_search_ranking.md)
- Naknadni: [00014 - Zasebni rezultati groblja u javnoj pretrazi](./00014_add_cemetery_search_results.md)
