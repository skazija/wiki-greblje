# Provjera trenutnog računara za razvoj

## Vrijeme izvršenja

2026-10-31 11:36:21 +01:00 (Europe/Sarajevo)

## Originalni prompt

> pozrdav prijatelju. Pripremio sam laptop po dogovoru. Mislim da sam instalirao sve po dogovoru. Trenutno sam na laptopu pokrenuo Codex gui. Kako da nastavimo dalje?

## Opis zadatka

Provjeriti lokalni repozitorij i Python okruženje dostupne trenutnoj Codex sesiji te odrediti siguran naredni korak prije pristupa produkcijskom serveru. Naknadno je potvrđeno da ove provjere nisu izvršene na novom laptopu, nego na računaru na kojem je ovoj sesiji dostupan postojeći `C:\wiki-groblje`.

## Izvršene provjere i promjene

- Potvrđeno je da je repozitorij otvoren na grani `main`, da prati `origin/main` i da je prije ovog izvještaja radno stablo bilo čisto.
- Potvrđeno je da je Git `2.54.0.windows.1` instaliran u `C:\Program Files\Git`, ali obična naredba `git` nije dostupna u Codex terminalu.
- Utvrđeno je da korisnički `PATH` sadrži Start Menu mapu `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Git` umjesto izvršne mape `C:\Program Files\Git\cmd`.
- Potvrđeni su postojeći `venv`, Python `3.14.5`, pip `26.1.1` i konzistentnost instaliranih Python paketa pomoću `pip check`.
- `python manage.py check --verbosity 2` završio je bez grešaka.
- Puni Django regresijski paket izvršen je sa `--keepdb --noinput`: svih 31 test je prošao, a izdvojena testna baza je sačuvana.
- Testovi su prijavili samo upozorenje da lokalni direktorij `staticfiles/` ne postoji; to nije uzrokovalo pad provjere i direktorij se uobičajeno stvara kroz `collectstatic` kada je potreban.
- Pokušaj čitanja GitHub remotea nije bio mjerodavan jer Codex sandbox postavlja izlazne proxy varijable na blokirajući lokalni endpoint `127.0.0.1:9`. U Git konfiguraciji nije pronađen zaseban proxy.
- Aplikacijski kod i konfiguracija nisu mijenjani. Jedina promjena je ovaj obavezni izvještaj.

## Naknadna ispravka konteksta

Provjere u ovom izvještaju odnose se na uređaj naziva `DESKTOP-T8ME4IM`, odnosno na računar na kojem ova Codex sesija vidi postojeći projekt. Laptop na kojem su zasad instalirani samo potrebni programi nije bio dostupan ovoj sesiji i na njemu ove provjere nisu izvršene.

## Razlozi za odluke

- Prije novih implementacija prvo je potvrđeno lokalno okruženje kako se problemi instalacije ne bi zamijenili za probleme aplikacije.
- Za Git provjere korištena je puna, potvrđena putanja do `git.exe`, bez mijenjanja korisničke ili sistemske konfiguracije bez izričitog zahtjeva.
- Produkcijski VPN, SSH i deployment nisu mijenjani jer prompt traži sljedeći korak, a ne autorizuje produkcijske promjene.
- Puni testni paket je siguran jer projekt koristi unaprijed izdvojenu PostgreSQL/PostGIS testnu bazu i opciju `--keepdb`.

## Povezani izvještaji

- [Provjera PostGIS testne baze](00020_verify_postgis_test_database.md)
- [Kontrolisani deployment pretrage na DELL](00024_deploy_search_to_dell.md)
