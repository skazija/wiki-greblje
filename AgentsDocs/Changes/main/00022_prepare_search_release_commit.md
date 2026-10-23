# 00022 - Priprema paketa napredne pretrage za commit

- Vrijeme izvršenja prompta: `2026-10-23T17:42:40+02:00` (`Europe/Sarajevo`)
- Git grana: `main`

## Originalni prompt

```text
može
```

## Opis zadatka

Pregledati akumulirane lokalne izmjene, pripremiti provjeren paket napredne pretrage i projektne dokumentacije za Git commit te odvojiti lokalne sigurnosne kopije od sadržaja repozitorija.

## Promjene napravljene za prompt

- Pregledani su Git status, historija, statistika i sadržaj izmjena aplikacijskog koda, migracije, testova, predloška, CSS-a i dokumentacije.
- Direktorij `backups/` dodan je u `.gitignore`; lokalne ZIP arhive i budući database dumpovi ne ulaze u commit.
- Ispravljeni su linkovi u `AGENTS.md` tako da poštuju stvarno veliko/malo slovo naziva `docs/Roadmap.md` na Linuxu i vode na najnoviji status projekta.
- Kreiran je `docs/STATUS_2026-10-23.md`, a TODO, Roadmap i Changelog usklađeni su sa završenom naprednom pretragom i lokalnom testnom infrastrukturom.
- Popup sadržaj markera groblja i groba promijenjen je iz JavaScript template-stringova u obične escaped stringove. Time nazivi koji sadrže `${...}` ostaju običan tekst i ne mogu se tumačiti kao JavaScript izraz.
- U dokumentaciji su uklonjene tri prijavljene greške završnih razmaka.

## Završna provjera

- Kompletan Django paket: 31 pronađen i 31 prolazni test.
- `python manage.py check`: bez sistemskih grešaka.
- `python manage.py makemigrations --check --dry-run`: `No changes detected`.
- Testna baza je korištena sa `--keepdb --noinput`; razvojna baza nije korištena za testove.
- Pregled osjetljivih obrazaca nije pronašao lozinke, API ključeve, privatne ključeve niti sadržaj `.env` datoteke u planiranom paketu.

## Git rezultat

- Predložena poruka commita: `Improve public search and add regression coverage`.
- Pokušaj `git add -A` zaustavljen je prije bilo kakvog staginga jer radno okruženje dozvoljava samo čitanje direktorija `.git`; Git nije mogao kreirati `.git/index.lock`.
- Nijedna promjena nije stageovana, commitovana niti poslana na GitHub.
- DELL nije kontaktiran niti izmijenjen.

## Razlozi za implementacijske odluke

- Sigurnosne kopije su lokalni operativni artefakti i ne pripadaju historiji izvornog koda.
- Tačna veličina slova u Markdown linkovima mora raditi i na Linux produkcijskom serveru.
- Statusna dokumentacija mora razlikovati lokalno potvrđenu funkcionalnost od još neizvršenog DELL deploymenta.
- JavaScript popup koristi obične stringove jer je Django `escapejs` namijenjen sadržaju JavaScript string literala, dok `${...}` unutar template-stringa ima posebno izvršno značenje.

## Povezani izvještaji

- [00018 - Dopuna regresijskih testova javne pretrage](./00018_add_search_regression_tests.md)
- [00019 - Konfiguracija odvojene PostGIS testne baze](./00019_configure_postgis_test_database.md)
- [00020 - Provjera PostGIS testne baze i regresijskih testova](./00020_verify_postgis_test_database.md)
- [00021 - Analiza nepoznatih godina u rezultatima pretrage](./00021_diagnose_unknown_birth_year_search_results.md)
- Naknadni izvještaji: nema ih u trenutku nastanka ovog dokumenta.
