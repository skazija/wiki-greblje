# Deployment i historija okruženja

## Svrha

Ovaj dokument objašnjava kako su stvarni incidenti iz razgovora oblikovali sadašnji siguran deployment postupak. Za izvršavanje deploymenta autoritativna kontrolna lista ostaje [`docs/DEPLOYMENT.md`](../../docs/DEPLOYMENT.md).

Izvor razgovora: [MapTiler admin nastavak](https://chatgpt.com/share/6ad8c598-22d0-83ed-b6f6-c8ec82bc4561).

## Produkcijska osnova

- Put: `/opt/wiki-greblje`
- Operativni sistem VM-a: Ubuntu 24.04
- Servisni korisnik: `wikiadmin`
- Virtualno okruženje: `/opt/wiki-greblje/venv`
- Servis: `wiki-greblje.service`
- Gunicorn bind: `127.0.0.1:8000`
- Aktivna baza: PostgreSQL 16/PostGIS, baza `wiki_groblje`
- Aplikacijski DB korisnik: `wiki_user`
- Environment fajl koji systemd očekuje: `/opt/wiki-greblje/.env`
- Produkcijski `config/settings.py`: lokalno prilagođen hostovima, HTTPS-u, CSRF-u, secure cookies i proxy SSL headeru.

## Etapa 1 - commit `81eee43`

Commit `Add monument classification system and migrate to MapTiler` obuhvatio je:

- klasifikaciju i migracije `0018`-`0025`;
- početnu MapTiler migraciju;
- admin katalog CSS;
- uklanjanje `.env` iz Git praćenja.

### Incident s `.env`

Nakon pulla je servis i dalje očekivao `/opt/wiki-greblje/.env`. Kopiran je backup `/home/wikiadmin/.env_wiki_groblja`, ali je sadržavao `DB_USER=wikiadmin`. Taj korisnik nije imao pravo čitanja `django_migrations`, dok je tabela pripadala `wiki_user`.

Uzrok nije bio PostgreSQL kvar ni potreba za novim grantovima, nego pogrešan environment fajl. Ispravni raniji `.env` je pronađen u Git historiji commita `10fa1ef`, vraćen je `DB_USER=wiki_user`, a MapTiler linija je prenesena bez prikazivanja ključa.

Nakon oporavka:

- Django je vidio MapTiler ključ;
- migracije `0018`-`0025` su prikazane kao neprimijenjene, zatim uspješno primijenjene;
- `collectstatic` je prijavio 5 kopiranih i 248 neizmijenjenih fajlova;
- produkcijske HTTPS postavke su ručno vraćene iz stasha bez prepisivanja novog MapTiler settinga;
- `manage.py check` je prošao;
- servis je postao `active (running)`;
- HTTP zahtjev je pravilno vraćao 301 na HTTPS.

### Lekcija

Uklanjanje tajne iz Git praćenja je ispravno, ali deployment mora unaprijed osigurati da lokalni `.env` ostaje na putanji koju systemd očekuje. Backup env fajl nije automatski autoritativan; provjeriti samo nazive i identitet DB korisnika bez ispisivanja tajnih vrijednosti.

## Etapa 2 - commit `7eed1b8`

Commit `Replace remaining OSM tile layers with MapTiler` nije imao migracije. Deployment je izveden ovako:

- pregledan je DELL status i lokalni diff `settings.py`;
- `settings.py` je ciljano stashovan;
- korišten je `git pull --ff-only` sa `81eee43` na `7eed1b8`;
- vraćen je tačno novi stash, ne nasumični stariji stash;
- pokrenuti su `manage.py check`, `collectstatic`, restart i provjera servisa;
- produkcija je testirana kroz Search, Add Grave i Suggest Grave Location mape;
- dodatno su uneseni novo groblje i dva mezara, a OCR je testiran na starijem nišanu.

Stash i backup nisu obrisani odmah nakon deploya.

## Etapa 3 - commit `2f94d59`

DELL je prije deploya bio na `7eed1b8`. Pull do `2f94d59` uključio je i ranije GitHub commitove `2112f2a` (uloge/klasifikacija) i `8e60660` (lokalizacija koordinata), uz novu funkcionalnost prijedloga groblja.

### Backup

Prvi pokušaj punog `pg_dump` završio je greškom `permission denied for schema tiger`. Iako je arhiva postojala i `pg_restore -l` je mogao čitati dio sadržaja, ona nije prihvaćena kao cjelovit backup.

Zatim je napravljen backup samo sheme `public`:

- `backups/wiki-greblje-public-20261010-182840.dump`
- približno 164 KB prema terminalu;
- popis aplikacijskih tabela potvrđen kroz `pg_restore -l`;
- restore nije testiran;
- ostaje ograničenje da to nije backup svih shema.

### Kod i konfiguracija

- Lokalni commit je prvo poslan na GitHub.
- Produkcijski `settings.py` kopiran je izvan repozitorija.
- Samo `config/settings.py` je stashovan.
- `git pull --ff-only` je prenio DELL sa `7eed1b8` na `2f94d59`.
- Stash je vraćen bez konflikta; stari stash-evi i SQLite backup nisu brisani.
- `manage.py check` je prošao.
- Migracije `0026` i `0027` su primijenjene.
- Potvrđene su uredničke dozvole i `collectstatic` rezultat 1 kopirana / 250 neizmijenjenih datoteka.
- Servis je restartovan; korisnik je naveo da izgleda uredno, ali puni end-to-end test nije tada dokumentovan komandnim izlazom.

## Etapa 4 - commit `be3a0ec`

Ispravka prazne osobe:

- lokalno ručno testirana;
- poslana na `origin/main`;
- lokalni working tree je bio čist;
- prema završetku razgovora nije prenesena na DELL, jer je planiran grupni deployment s narednim promjenama.

Ovo ograničenje i dalje važi dok ga noviji dokaz ne poništi.

## Etapa 5 - commit `09dc911`

Napredna javna pretraga i regresijska infrastruktura prenesene su na DELL 23.10.2026:

- prije promjene napravljen je puni PostgreSQL custom-format backup izvan repozitorija i potvrđen pomoću `pg_restore --list`;
- sačuvana je identična kopija produkcijskog `config/settings.py`;
- `config/settings.py` je ciljano stashovan, izvršen je fast-forward sa `2f94d59` na `09dc911`, a tačno novi stash je vraćen bez konflikta i zadržan;
- Django `check` je prošao, svih 27 `graves` migracija bilo je primijenjeno, a `migrate --plan` nije pokazao operacije;
- `collectstatic` je kopirao 1 datoteku uz 250 neizmijenjenih;
- servis je restartovan i potvrđen kao aktivan, bez novih upozorenja u desetominutnom journal pregledu;
- početna stranica i javna pretraga vratile su HTTP 200; novi filteri te odvojene sekcije osoba i grobova potvrđeni su u odgovoru;
- baza je prije restarta imala 12 groblja, 55 grobova i 40 osoba.

Tokom deploymenta poslovni DNS/UDM vraćao je `0.0.0.0` za `github.com`, čak i za klasične upite prema javnim resolverima. Stvarna GitHub adresa pribavljena je DNS-over-HTTPS upitom i potvrđena TLS certifikatom za `github.com`; `git fetch` je zatim izvršen jednokratnim `http.curloptResolve` parametrom. DNS konfiguracija i SSL provjera nisu mijenjani.

Zatečeno je `DEBUG=True` uz aktivne HTTPS/cookie zaštite. To nije mijenjano u sklopu pretrage i ostaje zaseban sigurnosni zadatak.

## Siguran obrazac za buduće deploye

1. Lokalno provjeriti kod, testove, `git diff --check`, tačan commit i čist status.
2. Na DELL-u prije pulla provjeriti branch, commit, status, servis i aktivnu bazu.
3. Napraviti novi backup i potvrditi exit status; ne vjerovati samo postojanju fajla.
4. Sačuvati produkcijski `settings.py` izvan repozitorija.
5. Stashovati samo poznatu tracked konfiguraciju.
6. Koristiti `git pull --ff-only`.
7. Vratiti tačno imenovani stash i pregledati diff.
8. Provjeriti `.env` na stvarnoj systemd putanji, bez otkrivanja tajni.
9. Pokrenuti `check`, `showmigrations`, `migrate --plan`; migrirati samo uz potvrđen backup.
10. Pokrenuti `collectstatic`, restart, status, logove i HTTP/funkcionalni test.
11. Ne brisati stare stash-eve ili nepoznate fajlove bez pregleda.

## Poznate zamke

- `source venv/bin/activate` je Linux oblik; `venv\Scripts\activate` je Windows oblik.
- Stari `db.sqlite3` nije aktivna produkcijska baza.
- Postojanje dump fajla ne znači da je `pg_dump` uspješno završio.
- `stash pop` bez pregleda opasan je kada postoji više stash-eva.
- Produkcijski `settings.py` je namjerno dirty u Git statusu; ne resetovati ga naslijepo.
- `.env` nikada ne vraćati u Git samo zato što ga servis očekuje na lokalnom disku.

Povezano: [Udaljeni pristup](REMOTE_ACCESS_AND_SERVER.md), [MapTiler](MAPTILER_AND_COORDINATES.md), [`docs/STATUS_2026-10-14.md`](../../docs/STATUS_2026-10-14.md).
