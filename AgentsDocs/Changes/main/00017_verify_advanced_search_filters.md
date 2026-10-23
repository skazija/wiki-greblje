# 00017 - Korisnička provjera naprednih filtera

- Vrijeme izvršenja prompta: `2026-10-23T16:35:48+02:00` (`Europe/Sarajevo`)
- Git grana: `main`

## Originalni prompt

```text
Izgleda da je sve ok. Za unos Grad: Visoko i Rođeni od:1940 vraća 1 groblje, 2 groba i 2 osobe
```

## Opis zadatka

Evidentirati korisnikovu ručnu provjeru kombinovanog lokacijskog i vremenskog filtera te potvrditi funkcionalni status pete etape plana javne pretrage.

## Potvrđeni rezultati

- Kao lokacija je uneseno `Visoko`.
- Kao donja granica godine rođenja unesena je `1940`.
- Pretraga je vratila jedno groblje, dva groba i dvije osobe.
- Rezultat potvrđuje da se oba kriterija istovremeno primjenjuju i da groblja i grobovi ostaju u rezultatu samo kada su povezani s odgovarajućim osobama.
- Peta etapa plana javne pretrage označena je kao funkcionalno završena i ručno potvrđena.

## Promjene napravljene za prompt

- Izvještaj `00016` dopunjen je korisničkom potvrdom i vezom na ovaj izvještaj.
- Aplikacijski kod, forma, predložak, stilovi, testovi, modeli, migracije, konfiguracija i baza nisu mijenjani.

## Razlozi za odluku

- Kombinacija lokacije i godine provjerava važniji slučaj od pojedinačnog filtera jer prolazi kroz relacije groblje → grob → osoba.
- Ručna provjera u browseru dopunjuje automatske testove koje razvojni PostgreSQL korisnik trenutno ne može pokrenuti zbog zabrane kreiranja testne baze.

## Povezani izvještaji

- [00014 - Zasebni rezultati groblja u javnoj pretrazi](./00014_add_cemetery_search_results.md)
- [00015 - Korisnička provjera rezultata groblja](./00015_verify_cemetery_search_results.md)
- [00016 - Napredni filteri javne pretrage](./00016_add_advanced_search_filters.md)
- Naknadni: [00018 - Dopuna regresijskih testova javne pretrage](./00018_add_search_regression_tests.md)
