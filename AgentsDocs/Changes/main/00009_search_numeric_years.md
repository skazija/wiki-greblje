# 00009 - Pretraga numeričkih godina

- Vrijeme izvršenja prompta: `2026-10-22T14:44:29+02:00` (`Europe/Sarajevo`)
- Git grana: `main`

## Originalni prompt

```text
hoćemo li sada to, normalno uz pravljenje sigurnosne kopije prvo?
```

## Opis zadatka

Nakon prethodno dogovorene i potvrđene tokenizacije i normalizacije dijakritike, napraviti novu sigurnosnu kopiju te omogućiti da javna pretraga numerički token traži u poljima `Person.birth_year` i `Person.death_year`. Kombinovani upit treba zadržati `AND` odnos između tokena, npr. prezime i godina moraju pripadati istoj osobi.

## Sigurnosna kopija

- Prije izmjene kreirana je arhiva `backups/search-years-before-20261022-144311.zip`.
- Arhiva sadrži prethodne verzije `graves/views.py`, `graves/tests.py` i `graves/templates/graves/search.html`.
- Arhiva je otvorena nakon kreiranja i potvrđeno je da sadrži sve tri očekivane datoteke.
- Baza nije kopirana niti mijenjana jer ova etapa nema migraciju i sve izvršne provjere koriste samo čitanje.

## Promjene napravljene za prompt

- `_person_search_token_query()` sada prepoznaje ASCII numerički token dužine do četiri znaka kao moguću godinu.
- Takav token se, uz postojeća tekstualna datumska polja, tačno poredi s `birth_year` i `death_year` cjelobrojnim poljima.
- Tokenizacija zadržava `AND` odnos, pa `Numanagic 1982` vraća samo osobe kod kojih se podudaraju i prezime i godina.
- Pretraga grobova nije promijenjena; numerički token i dalje može pronaći godinu zapisanu u naslovu ili natpisu groba.
- U testni zapis Rasima Numanagića dodane su godine rođenja i smrti.
- Dodani su regresijski testovi za zasebnu godinu rođenja, zasebnu godinu smrti i kombinaciju normalizovanog prezimena s godinom koja razlikuje dvije osobe istog prezimena.
- Modeli, migracije, predložak, konfiguracija i stvarni podaci nisu mijenjani.

## Provjera

- Python sintaksa `graves/views.py` i `graves/tests.py` uspješno je provjerena.
- `python manage.py check` završio je bez sistemskih grešaka.
- Izvršena je stvarna lokalna javna pretraga nad odobrenom osobom s `birth_year=1919`; odgovor je bio HTTP 200 i očekivani zapis je pronađen.
- Izvršena je stvarna lokalna javna pretraga nad odobrenom osobom s `death_year=1944`; odgovor je bio HTTP 200 i očekivani zapis je pronađen.
- Izvršena je stvarna kombinovana pretraga prezime + godina smrti; odgovor je bio HTTP 200 i očekivani zapis je pronađen.
- Sve izvršne provjere bile su samo za čitanje.
- Namjenski Django testovi nisu pokrenuti kroz test runner jer konfigurirani PostgreSQL korisnik i dalje nema pravo kreirati `test_wiki_groblje`; lokalni HTTP zahtjevi korišteni su za provjeru stvarnog SQL izvršavanja bez zamjene testne baze produkcijskom.

## Razlozi za implementacijske odluke

- Godina se poredi s cjelobrojnim poljem kao cijeli broj, umjesto tekstualnog `contains`, jer su `birth_year` i `death_year` strukturirani podaci.
- Ograničenje na najviše četiri ASCII cifre odgovara modelu historijske godine i izbjegava nepotrebnu konverziju proizvoljno dugih numeričkih tokena.
- Postojeća pretraga `birth_date_text` i `death_date_text` ostavljena je aktivna zbog nepreciznih, djelimičnih ili izvorno zapisanih datuma.
- Nisu dodani zasebni filteri raspona godina jer je ova etapa ograničena na ispravku osnovne jedinstvene pretrage; rasponi pripadaju budućoj naprednoj pretrazi.

## Povezani izvještaji

- [00005 - Pregled javne pretrage](./00005_review_search_view.md)
- [00006 - Tokenizacija javne pretrage](./00006_tokenize_public_search.md)
- [00007 - Normalizacija dijakritike u pretrazi](./00007_normalize_search_diacritics.md)
- [00008 - Ispravka tipa normalizacijskog izraza](./00008_fix_search_expression_output_field.md)
- [00010 - Procjena kontekstualnih rezultata grobova](./00010_review_contextual_grave_results.md)

## Naknadna ručna potvrda

Korisnik je lokalno potvrdio da upiti `1919`, `Nezir 1919`, `Hadzimejlic 1919` i `Hadžimejlić 1919` vraćaju očekivane rezultate.
