# Tematski indeks projektnog razgovora

## Izvor

- Naslov razgovora: **MapTiler admin nastavak**
- Javni snapshot: [ChatGPT shared conversation](https://chatgpt.com/share/6ad8c598-22d0-83ed-b6f6-c8ec82bc4561)
- Datum pregleda za ovu dokumentaciju: `2026-10-21`
- Obim pročitanog zapisa: 919 tekstualnih stavki, od čega 169 korisničkih, 295 asistentskih i 455 alatnih poruka.

Snapshot obuhvata razvojne i produkcijske sesije koje su dovele do stanja konsolidovanog u `docs` 14.10.2026. Share snapshot je historijski izvor i ne ažurira se naknadnim porukama. Priložene slike i ZIP datoteke opisane u razgovoru nisu sačuvane u ovom repozitoriju; zaključci su zato ograničeni na tekst razgovora i rezultate koji su u njemu zabilježeni.

## Pravilo autoriteta

Koristi ovaj redoslijed kada se izvori razlikuju:

1. trenutno provjeren kod, migracije, testovi i aktivno okruženje;
2. najnoviji dokumenti pod [`docs/`](../../docs/);
3. [`AI_AGENT_PROJECT_CONTEXT.md`](../AI_AGENT_PROJECT_CONTEXT.md);
4. tematski dokumenti iz ovog direktorija;
5. sam razgovor i njegove historijske pretpostavke.

Razgovor sadrži i prijedloge koji su kasnije ispravljeni. U tematske dokumente uneseni su završni zaključci, potvrđeni rezultati i korisne greške, ne svaki međukorak.

## Teme

### [MapTiler i koordinate](MAPTILER_AND_COORDINATES.md)

Migracija sa direktnih OpenStreetMap tile slojeva na MapTiler, prenos API ključa, `unlocalize`, `crossOrigin`, stvarni static source fajlovi, uklanjanje legacy kopija i commit/deploy tragovi.

### [Udaljeni pristup i server](REMOTE_ACCESS_AND_SERVER.md)

UniFi WireGuard, preklapanje mrežnih opsega, SSH pristup fizičkom Windows serveru i Ubuntu VM-u, korisnik za održavanje i lokacija produkcijskog repozitorija.

### [Deployment i okruženje](DEPLOYMENT_AND_ENVIRONMENT.md)

Tri dokumentovane produkcijske etape, zaštita `settings.py`, `.env` incident i oporavak, PostgreSQL/PostGIS backup ograničenja, migracije, `collectstatic` i restart servisa.

### [Uloge, dozvole i klasifikacija](ROLES_PERMISSIONS_AND_CLASSIFICATION.md)

Razdvajanje uredničke, stručne i administratorske odgovornosti, uzrok autocomplete 403 greške, podjela klasifikacijskih polja, admin/frontend ponašanje i commit `2112f2a`.

### [Prijedlozi i moderacija grobalja](CEMETERY_PROPOSALS_AND_MODERATION.md)

Javni obrazac, model statusa, zasebno odobravanje groblja i fotografija, zaštita javnih upita, migracije `0026`/`0027`, UI i commit `2f94d59`.

### [Fotografije i galerija](PHOTOS_AND_GALLERY.md)

Dozvole za `CemeteryPhoto`, statusi fotografija, javno filtriranje, incident galerije izazvan koordinatama i neriješeno pitanje direktnog pristupa media datotekama.

### [Unos mezara, osobe i OCR](GRAVE_ENTRY_PERSON_AND_OCR.md)

Jedinstveni obrazac, unos bez poznate osobe, regresija praznog `Person` zapisa, ručni test ispravke, commit `be3a0ec` i realni ali još nedovoljno izmjeren OCR rezultat.

## Povezani izvori u repozitoriju

- [Konsolidovani status](../../docs/STATUS_2026-10-14.md)
- [TODO](../../docs/TODO.md)
- [Changelog](../../docs/CHANGELOG.md)
- [Odluke](../../docs/DECISIONS.md)
- [Deployment vodič](../../docs/DEPLOYMENT.md)
- [Prethodni objedinjeni pregled](../Changes/main/00002_review_project_documentation.md)
