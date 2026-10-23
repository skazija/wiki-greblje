# Deployment — Wiki Greblje (DELL)

**Ažurirano: 14.10.2026.** Ovo je kontrolna lista, ne komanda za automatsko izvršavanje.

## Okruženje
- Lokalni razvoj: `C:/wiki-groblje` (Windows/Git Bash).
- Produkcija: `/opt/wiki-greblje` (DELL/Linux), Python virtualno okruženje `venv`.
- Django + PostgreSQL 16/PostGIS, Gunicorn servis `wiki-greblje.service`; domena `wikigreblje.ba`.
- Produkcijski `config/settings.py` ima lokalne HTTPS/host/CSRF postavke. `.env` sadrži tajne i DB parametre: **ne objavljivati**.

## Siguran postupak
1. Lokalno: `python manage.py check`, testovi, `git diff --check`, pregled promjena i commit.
2. Push na GitHub `main` (ili radna grana → pregled/merge u `main`); provjeriti hash commita.
3. DELL: `git status --short`, `git log -1 --oneline`, provjeriti servis i aktivnu bazu.
4. Prije migracija napraviti **svjež backup aktivnog PostgreSQL/PostGIS-a** i provjeriti uspjeh `pg_dump` i sadržaj arhive. Kopirati produkcijski `settings.py` izvan repozitorija. Ne oslanjati se na stari `db.sqlite3`.
5. Sačuvati lokalne izmjene `config/settings.py` (npr. ciljanim `git stash push -- config/settings.py`), `git pull --ff-only origin main`, zatim pažljivo vratiti stash. U slučaju konflikta stati.
6. `./venv/bin/python manage.py check`, `showmigrations`, `migrate --plan` i pregled očekivanih operacija.
7. `./venv/bin/python manage.py migrate` tek nakon potvrđenog backupa i plana.
8. `./venv/bin/python manage.py collectstatic --noinput`.
9. `sudo systemctl restart wiki-greblje.service`; `sudo systemctl status wiki-greblje.service --no-pager -l`; po potrebi pregledati logove.
10. Provjeriti HTTP odgovore, javne stranice, prijavu, prava urednika i tok predlaganja/odobravanja. Zabilježiti rezultat.

## Važna iskustva iz oktobra 2026.
- `pg_dump` za cijelu bazu pod korisnikom `wiki_user` prijavio je `permission denied for schema tiger`; nastao je **nepotpun dump** koji se ne smije tretirati kao backup.
- Ponovljeni `pg_dump -Fc -n public` uspješno je kreirao arhivu i `pg_restore -l` prikazao aplikacijske tabele. **Ograničenje:** to je backup sheme `public`, ne kompletne baze niti provjeren test povrata. Prije ozbiljnih promjena poželjno je osigurati i provjeriti cjelovit postupak oporavka.
- Za commit `2f94d59` migracije `0026` i `0027` primijenjene su; uredničke dozvole i `collectstatic` potvrđeni. Korisnički produkcijski test još nije dokumentovan kao završen.
- Stari stash-evi i nepoznate lokalne datoteke ne brišu se bez pregleda.

## Tipični problemi
- Pogrešna Python/venv putanja ili `.env`.
- `collectstatic` preskočen, browser cache.
- Promjene ostale na drugoj Git grani.
- Neprimijenjene migracije, neosvježen Gunicorn.
- Greške dozvola pri backupu, ili backup pogrešne baze.
