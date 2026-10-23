# 00007 - Normalizacija dijakritike u pretrazi

- Vrijeme izvršenja prompta: `2026-10-22T14:35:05+02:00` (`Europe/Sarajevo`)
- Git grana: `main`

## Originalni prompt

```text
hoćemo li sada i tu etapu sa č/ć š, ž?Trebamo voditi računa o tome da imamo i đ koje može biti dj.
```

## Opis zadatka

Nadograditi javnu pretragu tako da bosanski dijakritički znakovi ne sprečavaju pronalazak zapisa. Pretraga treba tretirati `č`, `ć` i `c` kao ekvivalentne, `š` kao `s`, `ž` kao `z` te `đ` kao digraf `dj`, uz zadržavanje tokenizacije, morfološkog pravila `Rasima` → `Rasim` i javnih moderacijskih filtera iz prethodne etape.

## Početno potvrđeno stanje

- Korisnik je prije ove izmjene ručno potvrdio da `Numanagić Rasima`, `Rasim Numanagić`, `Numanagić Rasim`, `Rasim` i `Numanagić` vraćaju očekivani zapis.
- Korisnik je također potvrdio da samo prezime ispravno vraća i druge osobe s istim prezimenom.
- Nedostajuće ponašanje prije ove etape bilo je podudaranje bez dijakritike ili s drugom varijantom `c`/`č`/`ć`.

## Sigurnosna kopija

- Prije izmjene kreirana je arhiva `backups/search-diacritics-before-20261022-143334.zip`.
- Arhiva sadrži prethodne verzije `graves/views.py`, `graves/tests.py` i `graves/templates/graves/search.html`.
- Arhiva je otvorena nakon kreiranja i potvrđeno je da sadrži sve tri očekivane datoteke.
- Baza nije kopirana niti mijenjana jer nema migracija ni zapisa podataka.

## Promjene napravljene za prompt

- Dodana je Python normalizacija korisničkog upita: pretvaranje u mala slova, `đ` → `dj`, Unicode razlaganje i uklanjanje kombinirajućih dijakritičkih znakova.
- Dodana je odgovarajuća normalizacija polja baze pomoću Django `Lower` i ugniježđenih `Replace` izraza.
- Pravila za podatke iz baze su `č` → `c`, `ć` → `c`, `š` → `s`, `ž` → `z`, `đ` → `dj`, uz uklanjanje kombinirajućeg akcenta i kvačice ako je tekst spremljen u rastavljenom Unicode obliku.
- Normalizacija je primijenjena na ime, prezime, tekstualne datume, naslov groba, natpis i naziv groblja.
- Postojeća tokenizacija i kontrolisano pravilo završnog `a` sada rade nad normalizovanim vrijednostima.
- Dodani su testovi za `Numanagić`/`Numanagič`/`Numanagic`, `Šaćir Žunić`/`Sacir Zunic`, `Đorđe Đurić`/`Djordje Djuric` i naslov groba `Oštećeni nišan`/`osteceni nisan`.
- Uklonjene su dvije završne linije s razmacima iz `graves/views.py`; nema funkcionalnog uticaja.
- Modeli, migracije, predložak, konfiguracija i podaci nisu mijenjani.

## Provjera

- Python sintaksa izmijenjenih datoteka uspješno je provjerena AST parserom.
- Direktna provjera normalizacije dala je očekivane oblike: `Numanagić`, `Numanagič` i `Numanagic` → `numanagic`; `Šaćir` → `sacir`; `Žunić` → `zunic`; `Đorđe` i `Djordje` → `djordje`.
- Django je uspješno konstruisao queryset s novim anotacijama i filterima bez `FieldError` ili greške izraza.
- `python manage.py check` završio je rezultatom `System check identified no issues (0 silenced)`.
- Integracijski testovi nisu izvršeni jer je u prethodnoj etapi potvrđeno da konfigurirani PostgreSQL korisnik nema dozvolu kreirati bazu `test_wiki_groblje`. Produkcijska baza nije korištena kao zamjena.

## Razlozi za implementacijske odluke

- Normalizuju se i upit i podaci iz baze; normalizacija samo korisničkog unosa ne bi mogla povezati ASCII upit s dijakritikom u spremljenom tekstu.
- `đ` se mapira u `dj`, a ne samo u `d`, prema eksplicitnom korisničkom zahtjevu i uobičajenom unosu bez znaka `đ`.
- Korišteni su ugrađeni Django izrazi umjesto nove PostgreSQL ekstenzije ili migracije kako bi ova etapa ostala mala, povratna i bez promjene sheme.
- Izrazi nad kolonama trenutno nisu indeksirani. Ovo je prihvatljivo za sadašnji mali skup podataka, ali prije značajnog rasta arhiva treba uvesti i indeksirati trajna normalizovana polja ili odgovarajući PostgreSQL indeks.
- Nije uvedena opća fuzzy pretraga; sličnost OCR i tipografskih grešaka ostaje zasebna naredna etapa.

## Povezani izvještaji

- [00005 - Pregled javne pretrage](./00005_review_search_view.md)
- [00006 - Tokenizacija javne pretrage](./00006_tokenize_public_search.md)
- [00008 - Ispravka tipa normalizacijskog izraza](./00008_fix_search_expression_output_field.md) - naknadna ispravka greške otkrivene tek pri izvršavanju SQL upita.

## Naknadna napomena

Početna provjera konstrukcije queryseta nije izvršila SQL. Prvi stvarni lokalni zahtjev otkrio je Django `FieldError` zbog miješanja `TextField` i `CharField` tipova unutar `Replace` izraza. Greška i izvršna provjera ispravke dokumentovane su u izvještaju `00008`.
