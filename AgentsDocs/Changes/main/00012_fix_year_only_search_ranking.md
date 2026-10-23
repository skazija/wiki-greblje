# 00012 - Ispravka rangiranja upita koji sadrži samo godinu

- Vrijeme izvršenja prompta: `2026-10-22T15:02:06+02:00` (`Europe/Sarajevo`)
- Git grana: `main`

## Originalni prompt

```text
na žalost imamo grešku na 1919: ValueError at /pretraga/
An empty Q() can't be used as a When() condition.
Request Method:	GET
Request URL:	http://127.0.0.1:8000/pretraga/?q=1919
Django Version:	6.0.5
Exception Type:	ValueError
Exception Value:
An empty Q() can't be used as a When() condition.
Exception Location:	C:\wiki-groblje\venv\Lib\site-packages\django\db\models\expressions.py, line 1609, in __init__
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
Server time:	Thu, 22 Oct 2026 13:00:14 +0000
```

## Opis zadatka

Ispraviti grešku rangiranja koja se pojavljuje kada javni upit sadrži samo numeričku godinu i zato nema nijedan tekstualni token imena. Potvrditi ispravku stvarnim lokalnim HTTP zahtjevima, uključujući korisnikove ranije potvrđene primjere.

## Uzrok

- Za upit `1919` lista tekstualnih tokena imena je prazna.
- Prva varijanta rangiranja koristila je prazne `Q()` objekte kao početne akumulatore za uslove punog imena.
- Django ne dozvoljava da prazan `Q()` bude uslov objekta `When`, zbog čega je razvojni server podigao `ValueError`.

## Promjene napravljene za prompt

- Uklonjeni su svi prazni `Q()` akumulatori iz rangiranja osoba.
- Pojedinačni neprazni uslovi prvo se skupljaju u liste, zatim se spajaju počevši od prvog stvarnog uslova.
- `When` objekti kreiraju se samo kada postoji najmanje jedna tekstualna varijanta imena.
- Ako upit sadrži samo godinu, `Case/When` se uopće ne gradi; queryset dobiva konstantni `search_rank=4` preko tipiziranog `Value` izraza.
- Logika filtriranja, dijakritike, godina, javnih statusa i rangiranja tekstualnih upita nije promijenjena.
- Modeli, migracije, predložak, konfiguracija i podaci nisu mijenjani.
- Nije kreirana nova arhiva jer sigurnosna kopija neposredno prije cijele etape rangiranja postoji kao `backups/search-ranking-before-20261022-145552.zip`.

## Provjera

- Python sintaksa je ispravna.
- `python manage.py check` završio je bez sistemskih grešaka.
- Stvarni lokalni zahtjevi `1919`, `Nezir 1919`, `Hadzimejlic 1919`, `Hadžimejlić 1919`, `Numanagic` i `NUMANAGIC RASIMA` vratili su HTTP 200.
- Svaki od prva četiri upita vratio je jednu očekivanu osobu iz lokalne baze.
- `Numanagic` je vratio tri osobe s pravilno sortiranim rangovima, a `NUMANAGIC RASIMA` jednu osobu s najvišim rangom 0.
- Sve provjere baze bile su samo za čitanje.
- Namjenski Django test runner nije korišten jer konfigurirani PostgreSQL korisnik nema dozvolu kreirati testnu bazu.

## Razlozi za implementacijsku odluku

- Potpuno izbjegavanje praznog `Q()` uklanja zabranjeno stanje umjesto da ga pokušava naknadno prepoznati.
- Upit koji sadrži samo godinu nema tekstualni signal za rangiranje imena, pa je konstantan rang semantički ispravan i jednostavniji od praznog `Case` izraza.
- Postojeći sekundarni abecedni poredak ostaje stabilan kada više osoba ima istu godinu.

## Povezani izvještaji

- [00009 - Pretraga numeričkih godina](./00009_search_numeric_years.md)
- [00010 - Procjena kontekstualnih rezultata grobova](./00010_review_contextual_grave_results.md)
- [00011 - Rangiranje rezultata pretrage](./00011_rank_search_results.md)
- Naknadni izvještaji: nema ih u trenutku nastanka ovog dokumenta.
