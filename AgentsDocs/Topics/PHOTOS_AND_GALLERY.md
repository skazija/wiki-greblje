# Fotografije i galerija

## Cilj

Fotografije su historijski dokumenti, ne dekoracija. Sistem mora omogućiti uredničko održavanje, spriječiti javnu objavu neodobrenih fotografija i pouzdano otvoriti galeriju na svim grobljima.

Izvor razgovora: [MapTiler admin nastavak](https://chatgpt.com/share/6ad8c598-22d0-83ed-b6f6-c8ec82bc4561).

## Model moderacije

`CemeteryPhoto` je prije implementacije prijedloga groblja već imao:

- status `pending`, `approved` ili `rejected`;
- `uploaded_by`;
- `is_primary`.

Fotografije se odobravaju odvojeno od groblja. Odobreno groblje može imati fotografiju koja još čeka i ta fotografija ne smije biti javna.

`Cemetery.primary_photo` je izmijenjen tako da bira samo među odobrenim fotografijama. Detalj groblja i javna galerija također koriste samo odobrene fotografije.

## Uredničke dozvole

Korisnik `skazija` kao član `Urednici` prvobitno nije mogao dodavati fotografije kroz `CemeteryPhotoInline`. Uzrok nisu bili inline kod ili upload, nego nedostatak `view/add/change` dozvola za `CemeteryPhoto` u grupi.

Nakon dodjele dozvola urednički upload je proradio. Poslovno pravilo je:

- Urednik održava fotografije groblja.
- Stručnjak ne dobija foto-prava samo zbog stručne uloge.
- Obični korisnik prilaže fotografije kroz moderirani javni workflow.
- Administrator zadržava sistemsku kontrolu.

Za potpuno novo okruženje provjeriti da li se cijela matrica foto-dozvola provisionira automatski ili je dio ranijeg ručnog setupa.

## Incident: galerija se ne otvara

Simptom:

- glavna fotografija je bila vidljiva;
- klik na nekim grobljima nije otvarao lightbox/listanje;
- na drugim grobljima isti kod je radio;
- admin je otvarao sve fotografije;
- Console nije odmah prikazivao očiglednu galerijsku grešku.

Dijagnostika je potvrdila:

- dugme, lightbox i image elementi postoje;
- ručno dodavanje `is-open` prikazuje okvir;
- programski klik ne otvara galeriju;
- skripta karte, pretrage i galerije nalazi se u zajedničkom `DOMContentLoaded` toku.

## Stvarni uzrok

U `cemetery_detail.html` koordinate pojedinačnih grobnih markera bile su ubačene bez `|unlocalize`. Groblja s odgovarajućim grobovima mogla su renderovati decimalni zarez, nakon čega je Leaflet JavaScript pukao prije registracije galerijskog klika.

Ispravka:

- `{% load l10n %}` gdje je potrebno;
- `grave.location.y|unlocalize`;
- `grave.location.x|unlocalize`.

Galerija je odmah proradila. Dodatno je isti princip primijenjen na Google Maps link u `grave_detail.html`.

Commit: `8e60660 Fix coordinate localization in cemetery maps and Google Maps links`.

## Lekcije

- Kvar galerije može nastati u ranijem, nepovezanom dijelu istog JavaScript bloka.
- Prisustvo HTML elemenata i ispravan CSS ne znače da je event listener registrovan.
- `undefined` povrat `.click()` nije sam po sebi greška.
- Porediti groblje koje radi s onim koje ne radi i provjeravati podatke koji se renderuju u skriptu.
- Server-renderovane brojeve uvijek normalizovati za JavaScript/URL.

## Otvoreno pitanje privatnosti

Javni queryseti i galerije filtriraju pending fotografije. Ipak, direktan URL media datoteke može zaobići view-level filtriranje ako web server služi fajl bez autorizacije. [`docs/TODO.md`](../../docs/TODO.md) zato i dalje traži provjeru politike direktnog pristupa fotografijama na čekanju.

Ovo treba rješavati tek nakon odluke o privatnosti i storage arhitekturi; nije potvrđeno kao završen problem.

Povezano: [Prijedlozi grobalja](CEMETERY_PROPOSALS_AND_MODERATION.md), [MapTiler i koordinate](MAPTILER_AND_COORDINATES.md).
