# Uloge, dozvole i klasifikacija

## Problem koji je pokrenuo rad

Korisnik `skazija` imao je staff pristup i niz direktnih dozvola, ali nije pripadao nijednoj Django grupi. Nova autocomplete polja klasifikacijskih šifarnika u adminu vraćala su `403 PermissionDenied`, pa je Select2 prikazivao generičku poruku da rezultate nije moguće učitati.

Uzrok nije bio kvar baze ili šifarnika. Django autocomplete je zahtijevao `view` dozvolu za povezani model, a direktne dozvole korisnika nisu obuhvatale nove klasifikacijske modele.

Izvor razgovora: [MapTiler admin nastavak](https://chatgpt.com/share/6ad8c598-22d0-83ed-b6f6-c8ec82bc4561).

## Prihvaćeni model uloga

Ključna odluka je da administrativna ovlaštenja nisu isto što i stručno znanje:

- **Obični korisnik** koristi javni frontend i šalje sadržaj na moderaciju.
- **Urednik** održava sadržaj: groblja, grobove, osobe, fotografije i prijedloge.
- **Stručnjak** dobija napredna stručna klasifikacijska polja.
- **Administrator** upravlja sistemom, korisnicima i konfiguracijom, ali nije automatski stručnjak.

Grupe su kombinabilne, ne strogo hijerarhijske. Korisnik koji uređuje sadržaj i radi stručnu klasifikaciju pripada grupama `Urednici` i `Stručnjaci`. Sama grupa `Stručnjaci` ne daje sva urednička prava.

## Urednička sigurnosna politika

Predložena i korištena matrica uredniku daje `view`, `add` i `change` za sadržajne modele, ali ne i opći `delete`. Obični korisnici ne dobijaju admin pristup samo zato što kroz frontend mogu kreirati prijedloge.

Approval workflow može mijenjati originalne zapise:

- `LocationSuggestion` mijenja lokaciju groba i pravi `EditHistory`;
- `PersonEditSuggestion` mijenja osobu i pravi historiju;
- `EditSuggestion` mijenja `Grave` i evidentira historiju;
- `ProblemReport` ima statusne akcije.

Zbog toga moderacijske dozvole pripadaju `Urednici`, ne običnim korisnicima.

## Podjela klasifikacijskih polja

### Osnovna klasifikacija za Urednika

- `macro_type` - Makro-tip;
- `tradition` - Tradicija;
- `monument_type` - Tip spomenika;
- `condition_classification` - Opće stanje;
- `monument_position` - Položaj spomenika.

Ova polja su procijenjena kao dovoljno jasne kontrolisane liste za uredničku katalogizaciju.

### Napredna klasifikacija za Stručnjaka

- `motifs` - motivi/ornamenti;
- `deterioration_patterns` - uočene pojave degradacije.

Ova polja traže specifičnije znanje i skrivena su korisniku koji nije član grupe `Stručnjaci`, uključujući superusera koji nije u toj grupi.

## Admin implementacija

`GraveAdmin.get_fieldsets()` dinamički uklanja stručna polja kada korisnik nije Stručnjak. Cilj je dobar UX: nedostupna polja se ne prikazuju kao prazni/neupotrebljivi autocomplete elementi.

Testovi u razgovoru potvrdili su:

1. Urednik vidi osnovna polja, ne vidi motive/degradacije.
2. Urednik + Stručnjak vidi sva polja.
3. Kada Stručnjak sačuva motive/degradacije, kasnije uređivanje istog groba kao obični Urednik ne briše skrivene vrijednosti.
4. Administrator nije automatski dobio stručna polja bez članstva u `Stručnjaci`.

## Frontend implementacija

`PublicGraveForm` je proširen klasifikacijskim poljima i dobija `user` argument. View mora proslijediti `request.user` pri GET i POST instanciranju forme.

Pravila prikaza:

- obični korisnik ne vidi klasifikaciju;
- član `Urednici` vidi osnovnu klasifikaciju;
- član `Stručnjaci` vidi stručnu klasifikaciju;
- korisnik u obje grupe vidi obje cjeline.

Model ima pet opcionalnih ForeignKey polja za osnovnu klasifikaciju, dok su `motifs` i `deterioration_patterns` ManyToMany, pa je bilo važno provjeriti stvarno spremanje, ne samo prikaz forme.

## Grupe i podaci

Grupe `Urednici` i `Stručnjaci` prvo su kreirane kao podaci u lokalnoj i produkcijskoj bazi. `skazija` je prebačen s individualnih prava na grupu `Urednici`, uz zadržavanje `is_active` i `is_staff`, bez `is_superuser`.

Važno: podaci o grupama ne putuju Gitom sami od sebe. Migracija `0027` kasnije osigurava samo dokumentovani skup prava nad `Cemetery` modelom za `Urednici` (`view_cemetery` i `change_cemetery`; `add_cemetery` je već postojao na DELL-u). Ne treba pretpostaviti da potpuno svježa baza automatski dobija cijelu ranije ručno kreiranu matricu grupa bez dodatne provjere.

## Commit i deployment

- Commit: `2112f2a Add role-based monument classification access`
- Obuhvat: `graves/admin.py`, `graves/forms.py`, Add Grave template i view; 210 dodatih i 2 uklonjene linije prema razgovoru.
- Lokalno: `manage.py check`, `git diff --check` i browser testovi uloga prošli.
- GitHub: commit poslan na `main`.
- DELL: nije deployan odmah; stigao je kasnije kao dio fast-forward ažuriranja od `7eed1b8` do `2f94d59`.

## Pravila za budući rad

- Ne koristiti `is_superuser` kao zamjenu za stručnu kvalifikaciju.
- Ne davati običnom korisniku staff/admin samo zbog javnog doprinosa.
- Pri skrivanju polja potvrditi da postojeći podaci ostaju sačuvani.
- Za autocomplete 403 prvo provjeriti `view` prava povezanog modela.
- Kod promjene matrice ažurirati i provisioning/migracije, ne samo ručne grupe u jednoj bazi.
- Provjeriti i admin i frontend, jer imaju odvojenu logiku prikaza.

Povezano: [Prijedlozi i moderacija](CEMETERY_PROPOSALS_AND_MODERATION.md), [`docs/DECISIONS.md`](../../docs/DECISIONS.md).
