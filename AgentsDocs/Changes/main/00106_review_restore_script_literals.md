# 00048 - Pregled literalnih tajni u skripti za obnovu

- Vrijeme: 2026-10-31 15:27:21 CET, Europe/Sarajevo (UTC+01:00).
- Grana prema posljednjoj provjeri: main.

## Originalni prompt

```text
Nemoj izvršavati niti mijenjati skriptu.

Pročitaj outputs/Obnovi-Wiki-Greblje-Laptop.ps1 i prvo provjeri sadrži li doslovno upisane lozinke, API ključeve ili druge tajne.

- Ne prikazuj nijednu stvarnu tajnu.
- Ako postoji doslovna tajna, samo je u prikazanoj kopiji zamijeni oznakom <REDACTED_LITERAL>; originalnu datoteku ne mijenjaj.
- Prikaži SHA-256 originalne skripte.
- Zatim prikaži kompletan sanitizovan sadržaj skripte, bez skraćivanja, u PowerShell code blokovima.
- Ako je sadržaj predugačak, podijeli ga na numerisane dijelove, ali nemoj izostaviti nijednu liniju.
- Navedi i sve vanjske skripte ili Python module koje ona izvršava, osim datoteka koje sadrže tajne.
- Ništa ne pokreći i ne mijenjaj baze, media, servis, USB niti ACL dozvole.
```

## Zadatak i rezultat

Skripta je procitana kao tekst i analizirana staticki, ukljucujuci AST ugradjenog Python programa; nije izvrsena niti izmijenjena. Nisu nadjene literalne lozinke, API kljucevi, tokeni ili privatni kljucevi. Lozinke se ucitavaju iz datoteka u memoriju. SHA-256 konstante su kontrolni zbirovi transfer datoteka, ne tajne. Redakcija prikazane kopije nije potrebna.

Originalni SHA-256: 9FC22D58E576135FB205CBEBC3C21270691F229171381AB2A8D6D1DCC568D196.

Skripta poziva projektni .venv/Scripts/python.exe, git, pg_ctl.exe status, pg_isready.exe i projektni manage.py (migrate, loaddata, check, test). Direktno uvozi standardne Python module os, sys, json, hashlib, shutil, zipfile, stat, subprocess, re, traceback, pathlib, datetime, zoneinfo, collections; eksterne psycopg2 i django podmodule conf, apps, db, db.models. django.setup ucitava lokalni wiki_local_settings, konfiguraciju config.settings, registrovane aplikacije i njihove tranzitivne zavisnosti. Potpuna lista dinamickih tranzitivnih importa ne tvrdi se bez izvrsavanja.

## Promjene i razlozi

Jedina izmjena je ovaj obavezni AGENTS izvjestaj. Originalna skripta nije izmijenjena; baze, media, servis, USB i ACL nisu dirani. Datoteke s tajnama nisu citane. Nema komandi obnove, starta/stopa, SQL-a, migracija, testova, commita ili pusha. Kompletan pregledani tekst prikazuje se korisniku bez skracivanja.

## Povezani izvjestaji

- [Priprema skripte](00105_prepare_laptop_restore_fallback.md)
- Naknadnih izvjestaja nema u trenutku pisanja.
