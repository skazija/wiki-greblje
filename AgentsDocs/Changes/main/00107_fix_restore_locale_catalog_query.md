# 00049 - Ciljana zamjena locale upita u pripremljenoj skripti

- Vrijeme: 2026-10-31 15:33:36 CET, Europe/Sarajevo (UTC+01:00).
- Grana prema posljednjoj provjeri: main.

## Originalni prompt

```text
Ne izvršavaj skriptu.

Prvo potvrdi da SHA-256 postojeće skripte još uvijek glasi:

9FC22D58E576135FB205CBEBC3C21270691F229171381AB2A8D6D1DCC568D196

U outputs/Obnovi-Wiki-Greblje-Laptop.ps1 pronađi tačno ovaj Python blok:

cur.execute('SHOW server_encoding'); encoding = cur.fetchone()[0]
cur.execute('SHOW lc_ctype'); ctype = cur.fetchone()[0]
cur.execute('SHOW lc_collate'); collate = cur.fetchone()[0]
cur.execute('SELECT datlocprovider FROM pg_database WHERE datname=current_database()')
provider = cur.fetchone()[0]

Zamijeni ga tačno ovim blokom:

cur.execute(
    'SELECT pg_encoding_to_char(encoding), datcollate, datctype, datlocprovider '
    'FROM pg_database WHERE datname=current_database()'
)
row = cur.fetchone()
require(row is not None, 'Nisu pronadjene postavke tekuce baze.')
encoding, collate, ctype, provider = row

Razlog: PostgreSQL na ovom laptopu ne podržava SHOW lc_ctype i SHOW lc_collate, ali vrijednosti postoje u pg_database.

Ne mijenjaj ništa drugo.

Nakon izmjene:

1. Potvrdi da je stari blok potpuno uklonjen i da novi postoji tačno jednom.
2. Ponovi provjeru PowerShell sintakse i sintakse ugrađenog Python programa bez izvršavanja.
3. Prikaži novi SHA-256 skripte.
4. Prikaži samo tačan diff izmjene s nekoliko okolnih linija.
5. Potvrdi da skripta, baze, media, settings, USB i servisi nisu pokrenuti ili mijenjani, osim same ispravke skripte i obaveznog AGENTS.md izvještaja.
6. Zatim stani.
```

## Zadatak, promjena i razlog

Prije pisanja potvrđen je originalni SHA-256. Binarno je zamijenjen iskljucivo zadani blok, uz ocuvanje postojece Python uvlake i svih ostalih bajtova. Koristi se trazeni pg_database katalog upit umjesto SHOW locale naredbi; razlog je korisnikova prijavljena nepodrzanost SHOW lc_ctype/lc_collate na laptopu. Nije izvrsavana provjera te tvrdnje nad bazom.

## Rezultati provjera

- Prethodni SHA-256: 9FC22D58E576135FB205CBEBC3C21270691F229171381AB2A8D6D1DCC568D196 — odgovara zahtjevu.
- Novi SHA-256: 0E8C9DAB73277408FE17A164CBCC0E8271792880FF996AF5CF1FDE6DF327D7F2.
- Stari blok: 0 pojavljivanja. Novi blok: 1 pojavljivanje.
- Potvrdjeno da je rezultat identican originalu uz samo jednu zadanu zamjenu.
- Python ast.parse: prolazi bez izvrsavanja.
- PowerShell Language.Parser.ParseFile: prolazi bez izvrsavanja.
- Diff je jedna izmjena oko linije 282, prikazana korisniku.

Skripta nije izvrsena. Baze, media, settings, USB i servisi nisu pokretani ili mijenjani. Nema SQL-a, starta/stopa, izmjena ACL-a, brisanja, migracija, testova, commita ili pusha. Jedine izmjene su ciljana ispravka outputs/Obnovi-Wiki-Greblje-Laptop.ps1 i ovaj obavezni izvjestaj.

## Povezani izvjestaji

- [Pregled originalne skripte](00106_review_restore_script_literals.md)
- [Priprema skripte](00105_prepare_laptop_restore_fallback.md)
- Naknadnih izvjestaja nema u trenutku pisanja.
