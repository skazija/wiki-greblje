# Unos mezara, osobe i OCR

## Cilj procesa

Unos mezara treba biti jedinstven, dostojanstven terenski tok koji obuhvata osnovne podatke, lokaciju, fotografije, osobe, natpis i klasifikaciju prema ulozi korisnika. Mezar mora moći postojati bez poznate osobe.

Izvor razgovora: [MapTiler admin nastavak](https://chatgpt.com/share/6ad8c598-22d0-83ed-b6f6-c8ec82bc4561).

## Dokumentovani tok

- `PublicGraveForm` je centralna javna forma.
- Prijava korisnika je obavezna za dodavanje groba.
- Groblje se bira samo među odobrenim grobljima.
- Podržani su višestruki upload fotografija, glavna fotografija, GPS/lokacija, natpis i podaci o osobi.
- Urednik dobija osnovnu klasifikaciju, Stručnjak naprednu; obični korisnik nije opterećen tim poljima.
- Predloženi grob i pripadajući sadržaj ulaze u moderacijski tok.

Detalji podjele uloga su u [Uloge, dozvole i klasifikacija](ROLES_PERMISSIONS_AND_CLASSIFICATION.md).

## Poslovno pravilo: mezar bez poznate osobe

Stari nišan ili mezar može biti evidentiran bez ijednog podatka o ukopanoj osobi. Informacija se može dopuniti kasnije, između ostalog kroz komentare i prijedloge izmjena. Sistem zato ne smije izmišljati prazan `Person` zapis samo da bi grob postojao.

Ako postoji makar jedan stvarni podatak o osobi, zapis je legitiman i može biti kreiran kao nepoznata osoba na čekanju.

## Regresija prazne osobe

Problematična logika računala je:

```python
is_unknown = not first_name and not last_name
if first_name or last_name or is_unknown:
    Person.objects.create(...)
```

Kada su ime i prezime prazni, `is_unknown` je `True`, pa se osoba uvijek kreirala, čak i bez drugih podataka.

## Ispravka

U `PublicGraveForm.save()` uvedena je provjera `has_person_data`. `Person` se kreira samo ako postoji barem jedan od ovih podataka:

- ime;
- prezime;
- godina rođenja;
- godina smrti;
- spol;
- fotografija osobe;
- napomena o osobi.

Nisu mijenjani modeli, statusi, foto workflow ni moderacijska pravila.

## Funkcionalna verifikacija

Kroz stvarni lokalni obrazac napravljena su dva unosa:

| Unos | Rezultat groba | Rezultat osobe |
| --- | --- | --- |
| Mezar bez podataka o osobi | kreiran, na čekanju | osoba nije kreirana |
| Nepoznata osoba samo s godinom smrti 1890 | kreiran, na čekanju | jedna osoba kreirana, na čekanju |

Admin pregled je pokazao dva groba na čekanju i samo jednu osobu. To je prihvaćeno kao ručna funkcionalna potvrda.

Automatski regresijski test je razmatran, ali nije završen. Postojeći `graves/tests.py` je standardni Django fajl i nije ga kreirala dijagnostička komanda.

## Commit i deploy status

- Commit: `be3a0ec Fix empty person creation when submitting graves`
- Poslan na `origin/main`.
- Lokalni working tree bio je čist.
- Na završetku razgovora commit nije bio na DELL-u; namjerno je ostavljen za grupni deployment.

Ne tvrditi da produkcija sadrži ovu ispravku bez novijeg dokaza.

## OCR

OCR je pomoćni tok za čitanje natpisa s fotografije, ne zamjena za ljudsku provjeru.

Razgovor bilježi stvarni produkcijski test na starijem nišanu nakon deploya `7eed1b8`: korisnik je naveo da je prepoznavanje bilo relativno dobro. To potvrđuje praktičnu vrijednost prototipa, ali nije mjerenje tačnosti niti dokaz pouzdanosti na izblijedjelim, oštećenim ili različitim pismima.

Status ostaje:

- funkcionalni prototip postoji;
- jedan realni primjer je dao dobar rezultat;
- sistematska evaluacija i poboljšanje tačnosti ostaju otvoreni.

## Obavezni naredni testovi

- Automatski test: forma bez podataka o osobi ne stvara `Person`.
- Automatski test: samo godina smrti stvara jednu osobu.
- Test ostalih pojedinačnih signala: spol, fotografija i napomena.
- Produkcijska provjera nakon stvarnog deploya `be3a0ec`.
- OCR skup stvarnih natpisa različite starosti, kontrasta, oštećenja i pisma, uz ručnu ocjenu rezultata.

Povezano: [`docs/STATUS_2026-10-14.md`](../../docs/STATUS_2026-10-14.md), [`docs/TODO.md`](../../docs/TODO.md), [Deployment](DEPLOYMENT_AND_ENVIRONMENT.md).
