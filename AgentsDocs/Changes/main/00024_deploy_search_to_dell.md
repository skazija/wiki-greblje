# 00024 - Deployment napredne pretrage na DELL

- Vrijeme izvršenja prompta: `2026-10-23T18:38:39+02:00` (`Europe/Sarajevo`)
- Git grana: `main`

## Originalni prompt

```text
može
```

## Opis zadatka

Kontrolisano prenijeti commit `09dc911` sa GitHuba na produkcijski DELL, uz backup, zaštitu lokalnih postavki, provjere baze i migracija, osvježavanje statičkih datoteka, restart i javni smoke test.

## Promjene napravljene za prompt

- Početno je potvrđeno da je DELL na `2f94d59`, servis aktivan, baza `wiki_groblje`, DB korisnik `wiki_user`, a jedine poznate lokalne stavke produkcijski `config/settings.py`, direktorij starih backupa i stari SQLite backup.
- Napravljen je puni PostgreSQL custom-format backup `/home/wikiadmin/wiki-groblje-backups/wiki-groblje-full-20261023-160400.dump`, veličine 303908 bajtova.
- `pg_dump` je završio statusom 0, `pg_restore --list` statusom 0, a potvrđeni su podaci ključnih tabela groblja, grobova i osoba.
- SHA-256 backupa je `e70e6abde6ec8451b2c7d96c3b2b5973eb87f7e5c34c407e00a695a2f09d6407`.
- Produkcijski `settings.py` kopiran je u `/home/wikiadmin/wiki-groblje-backups/settings.py-before-09dc911-20261023-160400`; `cmp` je potvrdio identičnost.
- Ciljano je stashovan samo `config/settings.py`; stash commit `04d91e9307ac8265f15a5b87b32a8a67c2a9ed85` zadržan je nakon uspješnog vraćanja.
- Izvršen je fast-forward sa `2f94d59` na `09dc911`, uključujući raniji commit `be3a0ec`.
- Produkcijske postavke vraćene su bez konflikta, uključujući novu zaštitu `TEST_DB_NAME`.
- Migracije nisu pokretane jer su svih 27 `graves` migracija već označene kao primijenjene, a `migrate --plan` je vratio `No planned migration operations`.
- `collectstatic` je kopirao 1 datoteku uz 250 neizmijenjenih.
- Korisnik je izvršio `sudo systemctl restart wiki-greblje.service`.

## DNS incident

- Sistemski resolver i klasični upiti prema `1.1.1.1` i `8.8.8.8` vraćali su `0.0.0.0` za `github.com`, zbog čega je lokalni server vraćao certifikat `wikigreblje.ba`.
- DNS-over-HTTPS upit prema `1.1.1.1` vratio je `140.82.121.3`; TLS provjera na toj adresi potvrdila je certifikat `CN=github.com`.
- `git fetch` je uspješno izvršen jednokratnim parametrom `http.curloptResolve=github.com:443:140.82.121.3`.
- Nisu mijenjani `/etc/hosts`, sistemski DNS ni Git SSL provjera.

## Završna provjera

- DELL `HEAD`, `origin/main` i `origin/HEAD`: `09dc911`.
- `python manage.py check`: bez sistemskih grešaka.
- Aktivna baza: `wiki_groblje`; produkcijski brojevi prije restarta: 12 groblja, 55 grobova i 40 osoba.
- Produkcijske HTTPS i secure-cookie postavke ostale su aktivne; MapTiler ključ je konfiguriran.
- `wiki-greblje.service`: `active (running)` nakon restarta.
- Lokalni HTTP vraća očekivani 301 prema HTTPS-u.
- Javna početna stranica i pretraga vraćaju HTTP 200.
- HTML javne pretrage sadrži napredne filtere, sekciju pronađenih osoba i sekciju pronađenih grobova.
- Journal pregled posljednjih deset minuta nije sadržavao warning/error zapise.
- Stari `db.sqlite3.backup-2026-08-24`, raniji stash-evi i produkcijske lokalne postavke nisu brisani.

## Privremeni pristup

- Za automatizaciju radnji bez `sudo` korišten je jednokratni ED25519 ključ sa SSH opcijom `restrict`.
- Ključ je uklonjen iz aktivnog `authorized_keys`, a naknadni pokušaj prijave završio je statusom 255, čime je opoziv potvrđen.
- Korisnik je zatim uklonio neaktivnu DELL kopiju `authorized_keys` i lokalni Windows privremeni direktorij s privatnim ključem; `Test-Path` je vratio `False`.
- Privremeni pristup i njegove kopije više ne postoje.

## Otvorene stavke

- Produkcijski `DEBUG=True` je zatečeno stanje. Nije mijenjano u ovom deploymentu i treba ga zasebno postaviti na `False` nakon provjere.
- Potrebno je ispraviti DNS/UDM pravilo koje vraća `0.0.0.0` za `github.com`.
- Preporučen je korisnički smoke test pretrage u pregledniku.

## Razlozi za implementacijske odluke

- Puni dump izvršen je kao PostgreSQL administratorski korisnik kako bi obuhvatio sve sheme i izbjegao raniji problem dozvole na shemi `tiger`.
- Stash je primijenjen, ali nije obrisan, kako bi ostala dodatna tačka povrata produkcijskih postavki.
- Prazan migracijski plan znači da promjena već primijenjene migracije `0027` služi novim instalacijama i ne treba se nasilno ponavljati na produkciji.
- Jednokratni Git DNS override zadržao je TLS provjeru i izbjegao trajnu mrežnu promjenu.

## Povezani izvještaji

- [00020 - Provjera PostGIS testne baze i regresijskih testova](./00020_verify_postgis_test_database.md)
- [00022 - Priprema paketa napredne pretrage za commit](./00022_prepare_search_release_commit.md)
- [00023 - Provjera ručnog Git staginga](./00023_verify_manual_git_staging.md)
- Naknadni izvještaji: nema ih u trenutku nastanka ovog dokumenta.
