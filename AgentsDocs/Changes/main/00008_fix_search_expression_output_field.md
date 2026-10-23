# 00008 - Ispravka tipa normalizacijskog izraza

- Vrijeme izvršenja prompta: `2026-10-22T14:38:34+02:00` (`Europe/Sarajevo`)
- Git grana: `main`

## Originalni prompt

```text
imamo grešku: FieldError at /pretraga/
Expression contains mixed types: TextField, CharField. You must set output_field.
Request Method:	GET
Request URL:	http://127.0.0.1:8000/pretraga/?q=numanagic
Django Version:	6.0.5
Exception Type:	FieldError
Exception Value:
Expression contains mixed types: TextField, CharField. You must set output_field.
Exception Location:	C:\wiki-groblje\venv\Lib\site-packages\django\db\models\expressions.py, line 366, in _resolve_output_field
Raised during:	graves.views.search
Python Executable:	C:\wiki-groblje\venv\Scripts\python.exe
Python Version:	3.14.5
Python Path:
['c:\\wiki-groblje',
 'C:\\Python314\\python314.zip',
 'C:\\Python314\\DLLs',
 'C:\\Python314\\Lib',
 'C:\\Python314',
 'C:\\wiki-groblje\\venv',
 'C:\\wiki-groblje\\venv\\Lib\\site-packages',
 'C:\\Users\\Administrator/.EasyOCR//user_network']
Server time:	Thu, 22 Oct 2026 12:36:40 +0000
```

## Opis zadatka

Dijagnosticirati i ispraviti `FieldError` koji se javio pri stvarnom izvršavanju pretrage nakon uvođenja normalizacije dijakritike te potvrditi ispravku izvršavanjem problematičnog lokalnog HTTP zahtjeva.

## Promjene napravljene za prompt

- U `graves/views.py` je uvezen Django `TextField`.
- Svaki ugniježđeni `Replace` izraz u `_normalized_search_expression()` sada eksplicitno koristi `output_field=TextField()`.
- Time svi nivoi normalizacijskog izraza imaju jednoznačan povratni tip bez obzira na to da li izvorno polje modela koristi `CharField` ili `TextField`.
- Modeli, migracije, predložak, testni podaci i produkcijski podaci nisu mijenjani.
- Nije kreirana nova arhiva jer sigurnosna kopija neposredno prije cijele etape dijakritike već postoji kao `backups/search-diacritics-before-20261022-143334.zip` i sadrži poznato funkcionalno stanje prije te etape.

## Uzrok

- Prethodna implementacija je na istu funkciju primjenjivala i `CharField` polja, poput imena i naslova, i `TextField` polje `inscription`.
- Django `Replace` je pokušao automatski odrediti izlazni tip iz izvornog izraza i `Value` argumenata tipa `CharField`.
- Greška se nije pojavila prilikom samog sastavljanja queryset Python objekta, nego tek kada je Django pri izvršavanju upita razriješio puni tip izraza.

## Provjera

- Python sintaksa je ispravna.
- `python manage.py check` završio je bez sistemskih grešaka.
- Stvarni lokalni zahtjev `GET /pretraga/?q=numanagic` izvršen je preko Django klijenta nad lokalnom bazom i vratio je HTTP 200.
- Izvršeni su i upiti `Numanagic`, `Numanagič`, `Numanagić` i `NUMANAGIC RASIMA`; svaki je vratio HTTP 200 i u rezultatima sadržavao osobu `Rasim Numanagić`.
- Provjere su bile isključivo čitanje; baza nije mijenjana.

## Razlozi za implementacijsku odluku

- Postavljanje `output_field` direktno na svaki `Replace` uklanja uzrok greške na najnižem nivou izraza i jednako radi za kratka i duga tekstualna polja.
- Korištenje zajedničkog `TextField` izlaza ne mijenja spremljene vrijednosti; utiče samo na tip izračunate SQL anotacije korištene tokom pretrage.
- Nije mijenjana logika normalizacije ni opseg rezultata jer je prijavljena greška bila isključivo problem Django tipizacije izraza.

## Povezani izvještaji

- [00006 - Tokenizacija javne pretrage](./00006_tokenize_public_search.md)
- [00007 - Normalizacija dijakritike u pretrazi](./00007_normalize_search_diacritics.md)
- [00009 - Pretraga numeričkih godina](./00009_search_numeric_years.md)
