# Prijedlozi i moderacija grobalja

## Cilj

Omogućiti prijavljenom korisniku da predloži novo groblje s lokacijom i fotografijama, dok urednik zasebno provjerava groblje i njegove fotografije. Neodobren sadržaj ne smije procuriti u javne liste, detalje, pretragu, statistiku ili povezane zapise.

Izvor razgovora: [MapTiler admin nastavak](https://chatgpt.com/share/6ad8c598-22d0-83ed-b6f6-c8ec82bc4561).

## Početno stanje

- `Cemetery` nije imao status ni autora prijedloga.
- `CemeteryPhoto` je već imao `pending`, `approved`, `rejected`, `uploaded_by` i `is_primary`.
- Javni `cemetery_list` je prikazivao sva groblja.
- Detalj groblja bio je dostupan po svakom postojećem ID-u.
- Galerija je već filtrirala odobrene fotografije, ali `Cemetery.primary_photo` nije nužno filtrirao status.
- Nije postojala javna forma/URL za prijedlog groblja.

## Model i migracije

### Migracija `0026`

`0026_cemetery_created_by_cemetery_status.py` dodala je:

- `Cemetery.created_by`;
- `Cemetery.status`.

Postojećih 11 grobalja nakon migracije bilo je odobreno; nijedno nije završilo na čekanju ili odbijeno.

### Migracija `0027`

`0027_cemetery_editor_permissions.py` trajno dodjeljuje grupi `Urednici` prava potrebna za pregled/promjenu groblja. Na produkciji je uz njih zabilježeno i već postojeće `add_cemetery`. Grupa `Stručnjaci` nije mijenjana.

## Javni obrazac

`CemeteryProposalForm` i `propose_cemetery` omogućavaju prijavljenom korisniku:

- naziv;
- grad;
- naselje/selo;
- vrstu groblja;
- opis;
- opcionalne GPS koordinate kroz Leaflet/MapTiler kartu;
- više fotografija.

Prijedlog groblja dobija `pending`, autora dobija iz prijavljenog korisnika, a fotografije se kreiraju kao zasebni zapisi na čekanju. Postoji posebna success stranica koja objašnjava da sadržaj ide na pregled.

Na listu grobalja dodano je dugme „Predloži novo groblje“. Stilovi obrasca i dugmadi smješteni su u postojeći `cemetery.css`; plave Bootstrap `btn-primary` akcije zamijenjene su diskretnim zelenim projektnim stilom.

## MapTiler na formi

Forma koristi isti provjereni obrazac kao postojeće mape. Tok dijagnostike je otkrio tri zamke:

- Leaflet CSS je prvobitno stavljen u nepostojeći `extra_css` block umjesto `extra_head`.
- `${maptilerKey}` je jednom bio u običnim navodnicima, pa nije interpoliran.
- isti ključ/endpoint je proradio tek uz `crossOrigin: true`.

Detalji su u [MapTiler dokumentu](MAPTILER_AND_COORDINATES.md).

## Moderacija

- Urednik može pregledati, ispraviti, odobriti ili odbiti groblje.
- Status groblja i status fotografije su nezavisni.
- Razgovor je potvrdio da je moguće posebno odobriti groblje, a posebno njegovu fotografiju.
- Odobravanje groblja ne objavljuje automatski fotografije.
- Stručnjak ne dobija dodatna prava nad ovim workflowom samo na osnovu stručne uloge.

## Zaštita javnog prikaza

Implementacija je proširena izvan same liste/detalja kako povezani odobreni zapis ne bi otkrio neodobreno groblje.

Dokumentovano filtriranje obuhvata:

- `cemetery_list`;
- `cemetery_detail` (neodobreno vraća 404);
- početnu stranicu i brojeve;
- statistiku;
- API lokacije groblja;
- detalj groba;
- javnu pretragu;
- listu osoba;
- prezimena i detalj prezimena;
- izbor groba za osobu;
- fotografije i `primary_photo`;
- `PublicGraveForm` izbor groblja, ograničen na odobrena.

Administrativna karta nije ograničena na odobrena groblja, jer urednik mora vidjeti zapise na čekanju.

## Lokalna verifikacija

U lokalnoj bazi korištena su dva groblja:

- odobreno groblje vraćalo je HTTP 200;
- groblje na čekanju vraćalo je HTTP 404.

Potvrđeno je i da:

- pending groblje nije na javnom spisku;
- pending fotografija nije glavna/javna fotografija;
- obrazac za mezar ne nudi pending groblje;
- prijedlog stiže u admin;
- odobravanje groblja i fotografije radi odvojeno.

## Commit i produkcija

- Commit: `2f94d59 Add cemetery proposal and moderation workflow`
- Obuhvat: 11 datoteka, uključujući modele, forme, admin, viewove, URL-ove, CSS, templatee i migracije `0026`/`0027`.
- Lokalno: `manage.py check`, diff provjere i navedeni funkcionalni testovi prošli.
- GitHub i DELL: commit prenesen na `main`.
- DELL: migracije `0026`/`0027` primijenjene; urednička prava provjerena; `collectstatic` 1/250.

## Preostala provjera

Iako su pojedinačne lokalne provjere prošle, dokumentacija i razgovor završavaju preporukom za puni produkcijski end-to-end test:

1. korisnik predlaže groblje i fotografiju;
2. oba su javno skrivena;
3. urednik odobrava samo groblje;
4. fotografija ostaje skrivena;
5. urednik odobrava fotografiju;
6. korisnik predlaže mezar samo u odobrenom groblju;
7. pregledaju se HTTP rezultati, logovi i greške.

Povezano: [Fotografije i galerija](PHOTOS_AND_GALLERY.md), [Uloge i dozvole](ROLES_PERMISSIONS_AND_CLASSIFICATION.md), [`docs/STATUS_2026-10-14.md`](../../docs/STATUS_2026-10-14.md).
