# 00018 - Dopuna regresijskih testova javne pretrage

- Vrijeme izvršenja prompta: `2026-10-23T16:47:23+02:00` (`Europe/Sarajevo`)
- Git grana: `main`

## Originalni prompt

```text
ok, sad sam shvatio. pa hoćemo li tačku 6.1?
```

## Opis zadatka

Izvršiti prvi dio šeste etape plana javne pretrage: dopuniti nedostajuće regresijske testove za moderaciju, rangiranje i paginaciju te deduplikaciju markera. Ne mijenjati PostgreSQL dozvole ni konfiguraciju testne baze; osposobljavanje izvršenja testova ostaje zasebna tačka 6.2.

## Sigurnosna kopija

- Prije izmjene kreirana je arhiva `backups/search-regression-tests-before-20261023-164500.zip`.
- Arhiva sadrži prethodnu verziju `graves/tests.py`.
- Potvrđeno je da arhiva postoji i sadrži jedan očekivani unos.
- Baza nije kopirana niti mijenjana jer su promjene ograničene na testni kod.

## Promjene napravljene za prompt

### Moderacija

- Postojeći test neodobrene osobe proširen je tako da pokriva i status `pending` i status `rejected`.
- Dodan je test koji potvrđuje da grob na čekanju ili odbijeni grob nije vidljiv te da su skrivene i njegove odobrene osobe.
- Dodan je test koji potvrđuje da groblje na čekanju ili odbijeno groblje skriva samo groblje, njegove odobrene grobove i odobrene osobe.

### Rangiranje i paginacija

- Dodan je test s jedanaest osoba koji potvrđuje da se tačno puno ime rangira prije djelimičnih imena, da se rangiranje izvršava prije paginacije i da se rezultat ne ponavlja na drugoj stranici.
- Dodan je analogan test s jedanaest grobova koji potvrđuje rangiranje tačnog naslova prije djelimičnih naslova i stabilnu podjelu na dvije stranice.
- Dodan je test koji potvrđuje da tekstualno nevažeći brojevi stranica za groblja, osobe i grobove ne izazivaju grešku, nego sigurno vraćaju prvu stranicu.

### Markeri

- Dodan je test u kojem je isti grob pronađen direktno i preko dvije pronađene osobe; `map_graves` mora sadržavati samo jedan ID groba.
- Dodan je test koji potvrđuje da rezultati groblja i groba koriste odvojene kontekstne liste i odvojene JavaScript kolekcije `cemeteryMarkers` i `graveMarkers`.

## Postojeća pokrivenost koja nije duplicirana

- Puno ime, oba redoslijeda imena i kontrolisana završna varijanta `a` već imaju regresijske testove.
- Numeričke godine, kombinacija imena i godine te rasponi rođenja i smrti već imaju regresijske testove.
- Normalizacija `č/ć/c`, `š/s`, `ž/z`, `đ/dj` i dijakritike naslova groba već ima regresijske testove.
- Nezavisna paginacija groblja i čuvanje GET filtera u paginacijskom query stringu već su pokriveni.

## Provjera

- Python sintaksa `graves/tests.py` uspješno je provjerena.
- `python manage.py check` završio je bez sistemskih grešaka.
- `git diff --check` nije prijavio greške u testnom fajlu.
- Django test runner sada pronalazi 31 test, odnosno sedam više nego prije ove etape.
- Izvršenje se zaustavlja prije pokretanja prvog testa jer konfigurirani PostgreSQL korisnik nema dozvolu kreirati bazu `test_wiki_groblje` (`permission denied to create database`). Zbog toga novi testovi još nisu označeni kao prolazni; samo je potvrđeno da se mogu učitati i otkriti.

## Razlozi za implementacijske odluke

- Moderacijski testovi provjeravaju roditeljske veze, jer odobreno dijete ne smije postati javno ako je njegov grob ili groblje neodobreno.
- Paginacijski testovi koriste više od deset rezultata kako bi stvarno prešli granicu stranice i dokazali da rangiranje nije naknadno preslagivanje samo trenutne stranice.
- Deduplikacija se provjerava na ID-jevima u kontekstu, a odvojene JavaScript kolekcije štite od kolizije jednakih numeričkih ID-jeva različitih modela.
- Testovi su dodani u postojeći `SearchViewTests` kako bi dijelili iste javne statuse i osnovne testne objekte bez uvođenja nove testne infrastrukture.

## Povezani izvještaji

- [00011 - Rangiranje rezultata pretrage](./00011_rank_search_results.md)
- [00012 - Ispravka rangiranja upita koji sadrži samo godinu](./00012_fix_year_only_search_ranking.md)
- [00014 - Zasebni rezultati groblja u javnoj pretrazi](./00014_add_cemetery_search_results.md)
- [00016 - Napredni filteri javne pretrage](./00016_add_advanced_search_filters.md)
- [00017 - Korisnička provjera naprednih filtera](./00017_verify_advanced_search_filters.md)
- Naknadni izvještaji: nema ih u trenutku nastanka ovog dokumenta.
