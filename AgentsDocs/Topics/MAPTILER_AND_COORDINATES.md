# MapTiler i obrada koordinata

## Cilj

Zamijeniti direktne OpenStreetMap tile pozive MapTiler podlogom, zadržati Leaflet interakcije i satelitski sloj te osigurati da koordinate rade u bosanskoj lokalizaciji na admin i javnim stranicama.

Izvor razgovora: [MapTiler admin nastavak](https://chatgpt.com/share/6ad8c598-22d0-83ed-b6f6-c8ec82bc4561).

## Standardni obrazac implementacije

- MapTiler ključ se čita iz `settings.MAPTILER_API_KEY`, a tajna ostaje u `.env` i ne ide u Git.
- View šalje `maptiler_api_key` u template context.
- Template koristi `{{ maptiler_api_key|escapejs }}`.
- Provjereni tile URL u razgovoru koristi `streets-v4/256/{z}/{x}/{y}.png`.
- Leaflet layer koristi `crossOrigin: true` kada je potreban CORS način zahtjeva.
- Esri satelitski sloj ostao je zaseban i nije bio uzrok MapTiler kvarova.
- Server-renderovane decimalne koordinate moraju koristiti `{% load l10n %}` i `|unlocalize` prije ulaska u JavaScript ili URL.

## Admin mape

`GraveAdminForm` je dobio MapTiler ključ kroz `data-maptiler-key` atribut jednog od koordinatnih widgeta. Postojeća logika koja iz longitude/latitude pravi GIS `Point(lon, lat, srid=4326)` nije mijenjana.

Pravi admin JavaScript izvori su:

- `graves/static/admin/js/cemetery_location_editor.js`
- `graves/static/admin/js/grave_location_editor.js`

Razgovor je potvrdio da ih `admin.py` zaista učitava i da su već koristili MapTiler. Kasnije pronađene kopije u `graves/static/js/` i korijenskom `static/graves/js/` nisu bile aktivni admin izvori.

## Javni prikazi

Prva MapTiler cjelina obuhvatila je Cemetery i Grave prikaze, uz rješavanje lokalizacije koordinata. Zatim su pronađene preostale direktne OSM reference na stranicama:

- Search mapa;
- Add Grave mapa;
- Suggest Grave Location mapa.

Za te stranice su odgovarajući viewovi dopunjeni MapTiler ključem, templatei su prebačeni na provjereni MapTiler obrazac, a Search marker koordinate dobile su `|unlocalize`.

## Commit i deployment tragovi

### `81eee43` - klasifikacija i početna MapTiler migracija

Commit je u razgovoru zabilježen kao `Add monument classification system and migrate to MapTiler`. Sadržavao je migracije `0018`-`0025`, MapTiler rad i uklanjanje `.env` iz Git praćenja. Prenesen je na DELL, gdje su migracije primijenjene i MapTiler ključ vraćen kroz produkcijski `.env`.

### `7eed1b8` - preostali OSM slojevi

Commit `Replace remaining OSM tile layers with MapTiler`:

- prebacuje Search, Add Grave i Suggest Grave Location;
- uklanja četiri legacy JS kopije koje nisu bile aktivni source;
- ne sadrži migracije;
- prenesen je na DELL;
- nakon deploya potvrđeni su servis, produkcijske mape, unos novog groblja, dva mezara i OCR test.

### `8e60660` - dodatna lokalizacija koordinata

Commit `Fix coordinate localization in cemetery maps and Google Maps links`:

- dodaje `|unlocalize` koordinatama grobnih markera u `cemetery_detail.html`;
- dodaje `|unlocalize` Google Maps linku u `grave_detail.html`;
- poslan je na GitHub, a kasnije je stigao na DELL u grupnom deployu do `2f94d59`.

## Incidenti i naučene lekcije

### Decimalni zarez

Django lokalizacija može `43.975...` renderovati kao `43,975...`. U JavaScript nizu to mijenja broj elemenata i Leaflet dobija pogrešan `LatLng`, često uz greške poput `Cannot read properties of null (reading 'lat')`.

Ovaj kvar nije uticao samo na mapu. U `cemetery_detail.html` raniji JavaScript prekid dogodio se prije inicijalizacije galerije, pa klik na galeriju nije radio iako su HTML/CSS elementi bili prisutni. Dodavanje `|unlocalize` na marker koordinate popravilo je i galeriju.

### `crossOrigin`

Na novom obrascu prijedloga groblja isti ključ i endpoint su davali različit rezultat jer zahtjev nije imao isti CORS način kao postojeća funkcionalna mapa. `crossOrigin: true` je bio završni popravak. Ovo nije univerzalni odgovor za svaku 403 grešku; prvo treba porediti stvarne Network zahtjeve.

### JavaScript navodnici

`${maptilerKey}` radi samo unutar template literala s obrnutim navodnicima. U običnom stringu browser šalje doslovni tekst `${maptilerKey}`.

### Template blokovi

`base.html` ima `extra_head`, ali razgovor je zabilježio pokušaj stavljanja Leaflet CSS-a u nepostojeći `extra_css` blok. Posljedica je bila siva/nepravilno stilizovana mapa i pogrešno pozicioniran Leaflet natpis.

### Duplikati static fajlova

Prije izmjene provjeriti:

1. šta `admin.py`/template stvarno učitava;
2. šta Git prati;
3. postoji li `STATICFILES_DIRS`;
4. razlikovati app source `graves/static/` od `STATIC_ROOT=staticfiles/` i neaktivnog korijenskog `static/` sadržaja.

Ne uređivati rezultat `collectstatic` kao source.

### Dijagnostički redoslijed

1. `manage.py check` i browser Console.
2. View Page Source: da li je ključ zaista renderovan, bez objave njegove vrijednosti.
3. Network: uporediti URL, status, origin i CORS način funkcionalnog i nefunkcionalnog zahtjeva.
4. Provjeriti markere/koordinate prije zaključka da je tile servis kriv.
5. Provjeriti da nije pokrenuto više lokalnih Django instanci sa starim kodom.
6. Pretražiti sve direktne `tile.openstreetmap.org` reference i utvrditi stvarni source svake.

## Trenutni dokumentovani status

Prema razgovoru i [`docs/CHANGELOG.md`](../../docs/CHANGELOG.md), preostali direktni OSM tile slojevi zamijenjeni su MapTilerom, a produkcija je prošla funkcionalni test. Ipak, svaka nova mapa mora ponoviti isti provjereni obrazac za ključ, CORS i lokalizaciju koordinata.

Povezano: [Deployment i okruženje](DEPLOYMENT_AND_ENVIRONMENT.md), [Fotografije i galerija](PHOTOS_AND_GALLERY.md).
