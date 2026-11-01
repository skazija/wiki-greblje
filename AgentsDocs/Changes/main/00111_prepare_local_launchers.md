# 00053 - Priprema jednostavnih lokalnih pokretaca

- Vrijeme: 2026-11-01 11:32:38 CET, Europe/Sarajevo (UTC+01:00).
- Grana: main; laptop MININT-B5ME0EV.

## Originalni prompt

```text
Kreiraj folder:

C:\Users\Administrator\Documents\Codex\2026-10-31\nalazim-se-na-novom-laptopu-i\work\launchers

U njemu pripremi:

1. Start-Wiki-Greblje.ps1
2. Start-Wiki-Greblje.cmd

PowerShell pokretač mora:

- raditi samo na računaru MININT-B5ME0EV i korisniku Administrator;
- koristiti tačne postojeće putanje projekta, venv-a, PostgreSQL 16 alata, data foldera i local-secrets.json;
- ne sadržavati literalne lozinke, MapTiler ključ ili druge tajne;
- prvo provjeriti pg_isready na 127.0.0.1:55432;
- ako PostgreSQL već radi, potvrditi da listener koristi očekivani projektni data folder;
- ako ne radi, potvrditi da je port slobodan i da PID iz postmaster.pid nije živ proces;
- pokrenuti klaster samo jednom pomoću pg_ctl, s novim timestampovanim logom i čekanjem do 60 sekundi;
- nikada ručno ne brisati postmaster.pid;
- nakon starta potvrditi pg_isready i tačan data folder;
- učitati lokalne tajne samo u memoriju;
- postaviti DJANGO_SETTINGS_MODULE=wiki_local_settings, PYTHONPATH, DB_PASSWORD, LOCAL_DJANGO_SECRET, LOCAL_MAPTILER_API_KEY i EASYOCR_MODULE_PATH;
- direktno koristiti .venv\Scripts\python.exe bez activate skripte;
- pokrenuti manage.py check;
- zatim pokrenuti Django na 127.0.0.1:8000 s --noreload;
- prikazati URL i objasniti da Ctrl+C zaustavlja Django;
- ostaviti PostgreSQL pokrenut nakon zatvaranja Django servera;
- u finally bloku vratiti prethodne procesne varijable bez prikazivanja tajni;
- pri grešci stati bez alternativnih popravki, brisanja, ACL promjena ili diranja drugih PostgreSQL procesa.

CMD datoteka treba samo pokrenuti pregledanu PS1 datoteku preko:

powershell.exe -NoProfile -ExecutionPolicy Bypass -File ...

i zadržati prozor otvoren ako dođe do greške.

Provjeri PowerShell i CMD sintaksu bez izvršavanja. Ne pokreći PostgreSQL, Django, testove ili bazne naredbe. Ne kreiraj Windows servis, scheduled task ili startup unos.

Prikaži kompletan sadržaj obje datoteke, njihove SHA-256 vrijednosti i obavezni AGENTS.md izvještaj. Zatim stani.
```

## Zadatak i promjene

Kreiran work/launchers i dvije nove datoteke Start-Wiki-Greblje.ps1 i Start-Wiki-Greblje.cmd izvan repozitorija. Postojeci outputs pokretac nije mijenjan. U repozitoriju je dodan samo ovaj izvjestaj; sacuvane su sve zatecene izmjene i neprateni izvjestaji.

## Odluke i ponasanje

Prva izvrsna PostgreSQL provjera u pripremljenom PS1 je pg_isready. Status 0 zahtijeva potvrdu vlasnika listenera, identicnog PID-a i data putanje u postmaster.pid, PostgreSQL 16 executable putanje i -D argumenta zivog procesa. Time se identitet provjerava bez SQL-a i bez administratorske lozinke. Ako procesne informacije nisu dostupne, skripta staje.

Samo status 2 (nema odgovora), slobodan port 55432 na svim lokalnim adresama i nepostojeci ili mrtvi stari PID dozvoljavaju jedan pg_ctl start. Status odbijanja veze ili druge greske zaustavlja postupak. Start koristi jedinstven timestamp log i -w -t 60. Neuspjeh ne pokrece retry, stop niti brisanje PID datoteke; poruka upozorava da se klaster mozda jos pokrece. Nakon uspjeha ponavljaju se readiness i identitet provjere.

Tajne se citaju tek poslije provjere klastera i ne ispisuju. Koriste se postojeci nazivi kljuceva iz manage-local.ps1. Sve procesne varijable koje skripta mijenja cuvaju se i vracaju u finally, ukljucujuci UTF-8 i privremene direktorije potrebne postojecem lokalnom okruzenju. Lokacija se takodjer vraca. Python se poziva direktno; check mora proci prije runservera. PostgreSQL ostaje pokrenut.

CMD koristi trazeni powershell.exe poziv s navodnicima oko PS1 putanje i relativno lociranje preko %~dp0. Svaki nenulti exit kod zadrzava prozor preko pause i vraca 1.

## Staticka provjera

- PowerShell Language.Parser.ParseFile: bez gresaka, bez izvrsavanja PS1.
- CMD: staticki pregled navodnika, %~dp0, %errorlevel%, zagrada i exit /b; sadrzaj provjeren protiv ocekivane strukture. cmd.exe nema parse-only mod; CMD nije izvrsen.
- Nema literalnih tajni. local-secrets.json nije citan tokom pripreme.
- PS1 SHA-256: FB8858CD1BD32267515D9C32195F5B92112B4C468C39171C96B242246E7C11BE
- CMD SHA-256: D5773B7AEC05B7945742A9DD1C44165EC52851FC0899C02A74A465A2809F1254

Nije potvrdjeno runtime ponasanje. Nisu izvrseni pokretaci, pg_isready, pg_ctl, PostgreSQL, Django, testovi ili bazne naredbe. Nisu kreirani servis, scheduled task ili startup unos. Nema brisanja, ACL promjena, commita, pusha ili pristupa produkciji.

## Povezani izvjestaji

- [Prethodni pregled konteksta pokretaca](00110_local_launcher_context_review.md)
- [Ranije razmatranje start timeouta](00103_revise_manual_start_cleanup.md)
- Naknadnih izvjestaja nema u trenutku pisanja.