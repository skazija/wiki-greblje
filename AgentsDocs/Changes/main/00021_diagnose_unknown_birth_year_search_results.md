# 00021 - Analiza nepoznatih godina u rezultatima pretrage

- Vrijeme izvršenja prompta: `2026-10-23T17:25:53+02:00` (`Europe/Sarajevo`)
- Git grana: `main`

## Originalni prompt

```text
naišao sam na interesantan rezultate. U pretrazi gdje je navedena godina od 1910 nalaze se i dva mezara na kojima nije unesena godina rođenja osobe. To bi možda mogao biti problem. Negdje možda godina rođenja neće biti čitljiva ili unesena a osoba je sigurno rođena poslije kao što je u ovim rezultatima koje sam dobio za Visoko i rođeni poslije 1910.
```

## Opis zadatka

Dijagnosticirati da li filter `Rođeni od` pogrešno uključuje osobe bez unesene godine rođenja te razjasniti odnos rezultata osoba, grobova i groblja.

## Promjene napravljene za prompt

- Nisu mijenjani aplikacijski kod ni podaci.
- Izvršena je read-only provjera ORM upita i stvarnog odgovora javne pretrage za lokaciju `Visoko` i vrijednost `Rođeni od: 1910`.

## Nalaz

- Stvarni odgovor sadrži 3 groblja, 5 grobova i 5 osoba.
- Svih pet osoba prikazanih u odjeljku osoba ima poznatu godinu rođenja koja zadovoljava filter: 1919, 1947, 1942, 1935 i 1923.
- Nijedna osoba s praznom godinom rođenja nije direktno uključena kao podudaranje filtera.
- Jedan od pronađenih grobova sadrži više osoba: jedna osoba ima godinu 1935, dok ostale povezane osobe nemaju unesenu godinu. Grob je zato ispravno uključen preko osobe rođene 1935, ali se na njegovoj detaljnoj stranici vide i ostale osobe iz istog groba.
- Groblje se analogno uključuje ako unutar njega postoji barem jedan odgovarajući grob odnosno osoba; otvaranje groblja zatim prikazuje i druge zapise koji nisu pojedinačno zadovoljili filter.

## Razlozi i preporuka

- Trenutno značenje filtera je strogo i provjerljivo: nepoznata godina nije automatski tretirana kao godina nakon 1910.
- Godina smrti sama po sebi ne dokazuje da je osoba rođena nakon zadane granice, pa takvu pretpostavku ne treba uvoditi nevidljivo.
- Ako korisnicima treba šira pretraga, sigurnije buduće rješenje je zasebna opcija `Uključi osobe s nepoznatom godinom rođenja`, jasno označena u interfejsu.
- Korisno poboljšanje prikaza bilo bi uz rezultat groba navesti osobu ili osobe zbog kojih je grob zadovoljio filter, kako zajednički grobovi ne bi izgledali kao pogrešni rezultati.

## Povezani izvještaji

- [00016 - Napredni filteri javne pretrage](./00016_add_advanced_search_filters.md)
- [00017 - Korisnička provjera naprednih filtera](./00017_verify_advanced_search_filters.md)
- [00020 - Provjera PostGIS testne baze i regresijskih testova](./00020_verify_postgis_test_database.md)
- Naknadni izvještaji: nema ih u trenutku nastanka ovog dokumenta.
