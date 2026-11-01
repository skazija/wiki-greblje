# Pregled read-only dijagnostike laptopa

## Vrijeme izvršenja

2026-10-31 12:29:08 +01:00 (Europe/Sarajevo)

## Originalni prompt

> Read-only dijagnostika je završena. Ništa nisam mijenjao, pokretao, zaustavljao niti brisao.
>
> **Git — tačan izlaz:**
>
> ```text
> ## main...origin/main
> ?? AgentsDocs/Changes/main/00025_setup_laptop_environment.md
>
> 181956c Document DELL search deployment
>
> origin  https://github.com/skazija/wiki-greblje.git (fetch)
> origin  https://github.com/skazija/wiki-greblje.git (push)
> ```
>
> **PostgreSQL klaster:**
>
> ```text
> pg_ctl: no server running
> ```
>
> Klaster nisam ponovo pokretao.
>
> Pokušaj izvršavanja četiri tražena SQL upita na `127.0.0.1:55432`, baza `wiki_laptop_dev`, završio je greškom:
>
> ```text
> psql: error: connection to server at "127.0.0.1", port 55432 failed:
> Permission denied (0x0000271D/10013)
> ```
>
> Zato **nema rezultata** za `server_encoding`, `lc_ctype`, `lc_collate` niti izraze `lower`/`replace`. Ne zaključujem njihove vrijednosti iz ranijih parametara inicijalizacije.
>
> **Šest neuspješnih slučajeva iz `work\django-tests.log`:**
>
> Svi pripadaju klasi `graves.tests.SearchViewTests` i završavaju na `self.assertEqual` u `graves/tests.py`.
>
> | # | Test i parametar | Linija | Završna assertion poruka |
> |---|---|---:|---|
> | 1 | `test_cemetery_and_location_filters_work_without_text_query`, `location='Zivinice'` | 145 | `AssertionError: Lists differ: [] != [<Cemetery: Staro groblje>]` |
> | 2 | `test_cemetery_search_matches_name_city_and_village`, `query='Zivinice'` | 66 | `AssertionError: Lists differ: [] != [<Cemetery: Staro groblje>]` |
> | 3 | `test_cemetery_search_matches_name_city_and_village`, `query='Serici'` | 66 | `AssertionError: Lists differ: [] != [<Cemetery: Staro groblje>]` |
> | 4 | `test_person_search_normalizes_s_and_z_diacritics` | 323 | `AssertionError: Lists differ: [] != [<Person: Šaćir Žunić>]` |
> | 5 | `test_person_search_treats_d_stroke_as_dj`, `query='Djordje Djuric'` | 343 | `AssertionError: Lists differ: [] != [<Person: Đorđe Đurić>]` |
> | 6 | `test_person_search_treats_d_stroke_as_dj`, `query='Đorđe Đurić'` | 343 | `AssertionError: Lists differ: [] != [<Person: Đorđe Đurić>]` |
>
> Svaki traceback dodatno navodi da očekivana lista sadrži jedan zapis, dok je stvarni rezultat `[]`. Dakle, riječ je o **šest neuspješnih slučajeva u četiri različite testne metode**.
>
> **ACL dozvole:**
>
> Obje datoteke imaju iste dozvole:
>
> - `work\local-secrets.json`
> - `work\postgres-dev\admin-password.txt`
>
> Vlasnik je `MININT-B5ME0EV\Administrator`. Nasljeđivanje je uključeno (`AreAccessRulesProtected: False`), a svi navedeni unosi su naslijeđeni:
>
> | Identitet | Dozvole |
> |---|---|
> | `MININT-B5ME0EV\CodexSandboxUsers` | `ReadAndExecute, Synchronize` |
> | `NT AUTHORITY\SYSTEM` | `FullControl` |
> | `BUILTIN\Administrators` | `FullControl` |
> | `MININT-B5ME0EV\Administrator` | `FullControl` |
>
> Sadržaj tajnih datoteka nije prikazan. ACL potvrđuje da grupa `CodexSandboxUsers` ima pravo čitanja obje datoteke.
>
> Trenutno je Git konfiguracija potvrđena, klaster nije pokrenut, a SQL dijagnostika nije izvršena. Neuspjesi testova uključuju pretragu dijakritika, ali uzrok još nije potvrđen. Daljnje radnje sam zaustavio.

## Opis zadatka

Pregledati rezultate dodatne laptop dijagnostike, procijeniti stanje PostgreSQL klastera, testova i zaštite lokalnih tajni te odrediti sljedeći siguran korak.

## Izvršene provjere i promjene

- Potvrđeno je da je laptop na ispravnom commitu `181956c`, grani `main` i remoteu, uz samo jedan neprateni izvještaj.
- Potvrđeno je da PostgreSQL klaster trenutno ne radi; SQL dijagnostika zato nije dala podatke o localeu ili normalizaciji.
- Greška socket-a `10013` nije dokaz neispravnog SQL-a jer veza nije uspostavljena.
- Svih šest neuspješnih slučajeva grupisano je oko uklanjanja bosanske dijakritike: `Živinice`, `Šerići`, `Šaćir Žunić` i `Đorđe Đurić`. To snažno podržava, ali još ne dokazuje, hipotezu pogrešnog database localea.
- Desktop kontrolna baza koristi locale `Bosnian (Latin)_Bosnia & Herzegovina.1250` i pravilno vraća `djordje` za provjereni SQL izraz.
- Potvrđeno je da `CodexSandboxUsers` ima pravo čitanja obje lokalne datoteke s tajnama. Sadržaj nije pročitan niti prikazan.
- Nisu mijenjani laptop, desktop aplikacijski kod, baze ni konfiguracija. Dodat je samo ovaj izvještaj.

## Razlozi za odluke

- Bazu ne treba ponovo kreirati dok se njene stvarne locale vrijednosti ne očitaju iz pokrenutog klastera.
- Klaster mora dobiti stabilan način pokretanja izvan životnog vijeka pojedinačne Codex komandne sesije.
- Administratorska lozinka baze ne treba dugoročno ostati čitljiva cijeloj sandbox grupi; korekcija slijedi nakon stabilizacije baze, uz očuvanje potrebnog pristupa.
- Neuspjesi se trenutno tretiraju kao problem okruženja, a ne izmjena aplikacijskog koda, jer isti commit i testovi prolaze na desktop bazi.

## Povezani izvještaji

- [Pregled izvještaja o postavljanju laptopa](00029_review_laptop_setup_report.md)
- [Objašnjenje sadržaja baze na laptopu](00030_explain_laptop_database_content.md)
