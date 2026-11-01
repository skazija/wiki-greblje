# 00047 - Priprema obnove laptopa; fallback zbog sandbox pristupa

- Vrijeme: 2026-10-31 15:23:40 CET, Europe/Sarajevo (UTC+01:00).
- Hostname: MININT-B5ME0EV.
- Repozitorij: C:\Users\Administrator\Documents\Codex\2026-10-31\nalazim-se-na-novom-laptopu-i\wiki-greblje.
- Potvrdjena grana: main. Najveci prethodni lokalni indeks: 00046.

## Originalni prompt

```text
Nastavi na laptopu MININT-B5ME0EV i pročitaj AGENTS.md.

Cilj je obnoviti lokalno razvojno okruženje iz već provjerenog paketa D:\backup. Ne pristupaj produkciji, ne pushaj i ništa postojeće ne briši.

Koristi postojeći PostgreSQL 16 klaster na 127.0.0.1:55432. Nemoj ga ponovo pokretati niti zaustavljati ako već prihvata veze.

Prije izmjena:

1. Potvrdi tačnu putanju repozitorija, aktivnu Git granu i status.
2. Potvrdi da PostgreSQL proces koristi očekivani work\postgres-dev\data.
3. Sigurno odredi postojeću administratorsku PostgreSQL ulogu i učitaj postojeće lozinke samo u memoriju. Ne prikazuj tajne.
4. Provjeri slobodan prostor. Potrebno je najmanje 2 GB.
5. Kopiraj samo ove datoteke u ignorisani lokalni folder backups\laptop-import-20261031:
   - D:\backup\wiki_groblje_appdata_utf8.json
   - D:\backup\wiki_groblje_media.zip
   - D:\backup\TRANSFER_README.md
6. Poslije kopiranja ponovo potvrdi ranije provjerene SHA-256 vrijednosti. Ne koristi wiki_groblje_pg18.dump niti wiki_groblje_appdata.json.

Ako su sve provjere uredne, izvrši sljedeće:

A. Očuvanje postojeće baze

- Potvrdi da je postojeća razvojna baza wiki_laptop_dev prazna kao u ranijoj dijagnostici.
- Prekini samo veze prema toj lokalnoj razvojnoj bazi.
- Preimenuj je u jedinstveno rezervno ime poput wiki_laptop_dev_before_import_20261031_HHMMSS.
- Ako postoji test_wiki_groblje, također je preimenuj u jedinstveno rezervno ime.
- Ne briši rezervne baze.

B. Nove baze

Kreiraj baze wiki_laptop_dev i test_wiki_groblje iz template0, s vlasnikom wiki_laptop i postavkama:

- ENCODING UTF8
- locale provider libc
- LC_COLLATE: Bosnian (Latin)_Bosnia & Herzegovina.1250
- LC_CTYPE: Bosnian (Latin)_Bosnia & Herzegovina.1250

U obje baze omogući postojeću PostGIS ekstenziju. Ne instaliraj PostgreSQL 18 i ne mijenjaj postojeći klaster.

Odmah potvrdi locale vrijednosti i da sljedeće provjere vraćaju true:

- lower('Š') = 'š'
- lower('Ž') = 'ž'
- lower('Đ') = 'đ'
- replace(lower('Đorđe'), 'đ', 'dj') = 'djordje'

Ako Windows/PostgreSQL odbije navedeni locale, stani bez alternativnih pokušaja i prijavi tačnu grešku.

C. Migracije i podaci

- Aktiviraj postojeći venv i postojeću laptop .env konfiguraciju.
- Pokreni Django migracije nad wiki_laptop_dev.
- Učitaj wiki_groblje_appdata_utf8.json pomoću manage.py loaddata.
- Ne prikazuj sadržaj korisničkih zapisa ili lozinki.
- Potvrdi broj zapisa:
  - cemeteries: 14
  - graves: 62
  - persons: 66
  - grave photos: 85
  - cemetery photos: 12

D. Fotografije

- Raspakuj ZIP prvo u privremeni staging folder unutar backups\laptop-import-20261031.
- Potvrdi da staging sadrži tačno 211 datoteka pod media/.
- Ako u korijenu projekta već postoji media folder, preimenuj ga u rezervno ime; ne briši ga.
- Tek nakon provjere premjesti novi media folder u korijen projekta.
- Potvrdi da novi media sadrži 211 datoteka i da putanje fotografija iz baze postoje na disku.

E. Završna provjera

- Pokreni manage.py check.
- Pokreni svih 31 test koristeći postojeću, pravilno lokalizovanu testnu bazu:
  python manage.py test --keepdb --noinput
- Potvrdi da svi testovi prolaze.
- Ne briši rezervne baze, rezervni media folder, lokalni paket niti sadržaj USB stika.

Ako Codex sandbox ne može pristupiti PostgreSQL-u, nemoj mijenjati ACL dozvole i nemoj improvizovati. Pripremi jednu preglednu PowerShell skriptu za pokretanje u običnom lokalnom PowerShellu, objasni šta ona radi i stani prije njenog izvršavanja.

Ako bilo koji korak nakon preimenovanja stare baze ne uspije, ne briši niti automatski vraćaj baze. Zaustavi se, navedi tačnu fazu i trenutno stanje.

Na kraju napravi obavezni AGENTS.md izvještaj i prikaži sažetak svih izvršenih promjena, rezervnih imena, rezultata provjera i testova.
```

## Izvrsene provjere

Procitan AGENTS.md. Hostname i putanja odgovaraju laptopu. Git status prije ove izmjene:

```text
## main...origin/main
?? AgentsDocs/Changes/main/00025_setup_laptop_environment.md
?? AgentsDocs/Changes/main/00040_readonly_laptop_diagnostics.md
?? AgentsDocs/Changes/main/00043_prepare_manual_powershell_diagnostics.md
?? AgentsDocs/Changes/main/00045_revise_manual_start_cleanup.md
?? AgentsDocs/Changes/main/00046_verify_usb_transfer_package.md
```

- C: ima 263132942336 slobodnih bajtova, oko 245 GiB; vise od trazenih 2 GB.
- git check-ignore potvrdjuje da backups/laptop-import-20261031/probe pripada ignorisanom backups direktoriju.
- pg_ctl status: no server running u ovoj sesiji.
- pg_isready na 127.0.0.1:55432: no response.
- Pokusaj administratorske read-only veze s postojecom tajnom iz memorije nije uspio:

```text
connection to server at "127.0.0.1", port 55432 failed: Permission denied (0x0000271D/10013)
Is the server running on that host and accepting TCP/IP connections?
```

- Zato stvarni serverski data_directory, administratorske SQL privilegije i praznina razvojne baze nisu potvrđeni u ovom koraku. Uloga wiki_local_admin poznata je iz ranije uspjesne initdb -U naredbe, ali trenutna veza nije uspjela.
- .env u repozitoriju ne postoji. Stvarna ranije pripremljena laptop konfiguracija koristi work/wiki_local_settings.py, work/manage-local.ps1 i work/local-secrets.json. Lokalni settings trenutno cilja test_wiki_laptop_dev i work/media, sto se razlikuje od novih zahtjeva.

## Promjene i pripremljeni fallback

Kreirana je jedna korisnicka skripta: outputs/Obnovi-Wiki-Greblje-Laptop.ps1 u korijenu radnog direktorija, izvan repozitorija. Nije izvrsena. Pripremljen je samo ovaj obavezni izvjestaj uz tu skriptu.

Skripta zahtijeva da isti postojeci server vec radi: ne sadrzi pg_ctl start/stop, ne mijenja ACL i ne pokusava popravke. SQL SHOW data_directory i verzija 16 moraju potvrditi pravi server prije izmjena. Provjerava postojecu administratorsku ulogu i aplikacijsku lozinku u memoriji. Provjerava prostor i prazninu terenskih tabela (sistemske dozvole, lokalni admin i seed katalozi mogu postojati).

Plan skripte:

1. Provjera USB hash vrijednosti, 478 fixture objekata, pet trazenih brojaca i 211 sigurnih ZIP putanja. Kopiranje iskljucivo tri zadane datoteke u ignorisani backups/laptop-import-20261031; ponovno hashiranje, bez prepisivanja razlicitih postojecih kopija.
2. Preimenovanje stare razvojne baze i eventualne test_wiki_groblje, uz jedinstveni datum/vrijeme/mikrosekunde. Samo razvojne veze se terminiraju. Postojeca test_wiki_laptop_dev se ne dira. Ako test_wiki_groblje ima aktivne veze i rename ne uspije, skripta staje bez terminiranja tih veza.
3. Kreiranje dvije trazene baze iz template0 s UTF8, libc i izricitim bosanskim locale vrijednostima, PostGIS i cetiri Unicode provjere. Svaka greska staje bez alternativnog localea ili vracanja/brisanju baza.
4. Kopija postojeceg lokalnog settings modula u ignorisani backup, zatim ciljano uskladjivanje samo TEST naziva i MEDIA_ROOT. Ne kreira se izmisljena .env i ne mijenja se produkcijski config/settings.py. Postojeci venv Python koristi se direktno, sto ne zahtijeva globalnu aktivaciju.
5. Migracije, loaddata i pet trazenih brojaca. ZIP se raspakuje u jedinstveni staging; sve putanje FileField polja provjeravaju se prije i nakon premjestanja. Postojeci projektni media se premjesta u jedinstveni rezervni folder unutar ignorisanog backups paketa. work/media ostaje sacuvan.
6. check i test --keepdb --noinput: mora se potvrditi tacno 31 test i OK. Provjerava se da razvojni brojevi ostaju jednaki i poslije testova.

Skripta tokom buduceg izvrsavanja ispisuje samo administrativne provjere i agregate, te cuva sanitizovano stanje faza i rezultata u restore-state-<timestamp>.json. Ne ispisuje tajne ni sadrzaj korisnickih zapisa, niti sirove Django fixture tracebacks. Nazivi rezervnih baza i media upisuju se odmah nakon izvrsene promjene. Poslije greske nema automatskog ponovnog pokretanja ili rollbacka.

## Validacija i granice

PowerShell parser i ast.parse ugradjenog Python programa prosli su bez izvrsavanja njihove logike. Zbog sandbox blokade nema tvrdnje da je obnova runtime provjerena. Migracije, loaddata, ZIP ekstrakcija, check i testovi NISU izvrseni. Paket nije kopiran; nijedna baza niti media direktorij nisu preimenovani. Rezervna imena jos ne postoje jer skripta nije pokrenuta.

Nema pristupa produkciji, commita, pusha, brisanja, instaliranja ili promjene PostgreSQL klastera.

## Razlozi odluka

Korisnik izricito zahtijeva fallback i zaustavljanje prije izvrsavanja ako sandbox ne moze pristupiti PostgreSQL-u. Poznata greska 10013 ispunjava taj uslov. Zato nisu trazene ACL promjene niti su pokusavani alternativni serveri, portovi, admin uloge ili locale vrijednosti. Stvarna lokalna konfiguracija i njena odstupanja navedeni su otvoreno.

## Povezani izvjestaji

- [Provjeren USB paket](00104_verify_usb_transfer_package.md)
- [Read-only dijagnostika laptopa](00101_readonly_laptop_diagnostics.md)
- [Pocetno lokalno okruzenje](00100_setup_laptop_environment.md)
- Nema naknadnih izvjestaja u trenutku pisanja.
