# 00015 - Korisnička provjera rezultata groblja

- Vrijeme izvršenja prompta: `2026-10-23T16:17:51+02:00` (`Europe/Sarajevo`)
- Git grana: `main`

## Originalni prompt

```text
radi prijatelju. probao sam unos gradsko i dobio mapu sa lokacijama gradskog groblja visoko i Fojnica. Probao sam Visoko i dobio groblja u Visokom. Makrei isto rade, svaki od njih vodi na odabrano groblje.
```

## Opis zadatka

Evidentirati korisnikovu ručnu funkcionalnu provjeru zasebnih rezultata groblja, lokacijske pretrage i markera na mapi te potvrditi status treće etape plana javne pretrage.

## Potvrđeni rezultati

- Upit `gradsko` prikazuje mapu s lokacijama Gradskog groblja Visoko i gradskog groblja u Fojnici.
- Upit `Visoko` vraća groblja evidentirana u Visokom.
- Markeri na mapi rade i svaki vodi na odgovarajuće odabrano groblje.
- Time su zasebni rezultati groblja, pretraga po lokaciji i veza rezultata s mapom ručno potvrđeni u stvarnom lokalnom interfejsu.
- Treća etapa plana javne pretrage označena je kao funkcionalno završena i potvrđena.

## Promjene napravljene za prompt

- Izvještaj `00014` dopunjen je korisničkom potvrdom i vezom na ovaj izvještaj.
- Aplikacijski kod, predložak, stilovi, testovi, modeli, migracije, konfiguracija i baza nisu mijenjani.

## Razlozi za odluku

- Ručna provjera pokriva ponašanje koje automatski testovi trenutno ne mogu izvršiti zbog nedostatka PostgreSQL dozvole za kreiranje testne baze.
- Posebno je važno zabilježiti potvrdu markera i navigacije jer se oni izvršavaju u browseru i nisu obuhvaćeni provjerom Django queryseta.

## Povezani izvještaji

- [00013 - Provjera završenosti etapa javne pretrage](./00013_verify_search_phases.md)
- [00014 - Zasebni rezultati groblja u javnoj pretrazi](./00014_add_cemetery_search_results.md)
- Naknadni: [00016 - Napredni filteri javne pretrage](./00016_add_advanced_search_filters.md)
