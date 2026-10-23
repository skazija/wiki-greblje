# 00005 - Pregled javne pretrage

- Vrijeme izvršenja prompta: `2026-10-22T14:12:19+02:00` (`Europe/Sarajevo`)
- Git grana: `main`

## Originalni prompt

```text
Možeš li provjeriti trenutnu metodu za pretragu koja se nalazi u views.py u folderu graves i vidjeti koje su mogućnosti poboljšanja za potrebe aplikacije wiki-greblje?
```

## Opis zadatka

Pregledati javnu metodu `search()` u `graves/views.py` u kontekstu povezanih modela, predloška, URL-a, postojećih testova, PostgreSQL/PostGIS okruženja i projektnih ciljeva te utvrditi prednosti, nedostatke i prioritetne mogućnosti poboljšanja. Zadatak je analiza; implementacija promjena nije tražena.

## Promjene napravljene za prompt

- Pregledana je implementacija `search()` i javni predložak `graves/search.html`.
- Pregledani su modeli `Cemetery`, `Grave` i `Person`, uključujući javne statuse i polja koja se mogu pretraživati.
- Pregledani su `person_list()`, projektni PostgreSQL/PostGIS backend, postojeći testovi i dokumentovani cilj napredne pretrage.
- Utvrđeno je da trenutna pretraga ispravno ograničava rezultate na odobrene osobe, grobove i groblja, koristi parametrizovane Django ORM upite, sigurno obrađuje nevažeće brojeve stranica i uklanja duple grobove sa mape.
- Utvrđeni su glavni funkcionalni nedostaci: višerječni upit se tretira kao jedna fraza u svakom pojedinačnom polju; numeričke godine se ne traže u `birth_year` i `death_year`; nema pretrage bez dijakritike ni tolerancije na OCR/tipografske greške; podudaranje naziva groblja vraća sve njegove grobove umjesto zasebnog rezultata groblja; nema rangiranja po relevantnosti; stručna klasifikacija i lokacijski filtri nisu obuhvaćeni.
- Utvrđeno je da `icontains` upiti nad više neindeksiranih tekstualnih polja neće dobro skalirati s rastom arhiva te da za javnu pretragu nema namjenskih regresijskih testova u `graves/tests.py`.
- Predložen je fazni pristup: prvo popraviti semantiku upita, godine, rezultate groblja, rangiranje i testove; zatim dodati napredne filtre; tek nakon mjerenja stvarnog opterećenja uvesti PostgreSQL trigram/full-text indeksiranje i normalizovana polja.
- Aplikacijski kod, modeli, migracije, konfiguracija, baza i produkcija nisu mijenjani.

## Razlozi za implementacijske odluke

- Analiza je zadržana bez izmjene aplikacijskog koda jer je prompt tražio provjeru i mogućnosti poboljšanja, ne implementaciju.
- Preporuke daju prednost ponašanju koje direktno odgovara načinu korištenja arhiva: puno ime i prezime, godina, groblje/lokacija, natpis i strukturirane osobine spomenika.
- Zadržavanje javnih statusnih filtera tretirano je kao obavezno pravilo zbog dokumentovane politike moderacije.
- Hibridna PostgreSQL pretraga preporučena je kao kasnija faza: trigrami su korisni za imena, dijakritiku i OCR greške, dok full-text rangiranje bolje odgovara dužim natpisima i bilješkama. Uvođenje oba mehanizma bez testova relevantnosti i mjerenja podataka bilo bi preuranjeno.
- Zasebna normalizovana polja preporučena su prije indeksiranja izraza s normalizacijskim funkcijama kako bi ponašanje i održavanje indeksa ostali predvidljivi.

## Povezani izvještaji i dokumenti

- Direktno povezani raniji ili naknadni izvještaji: nema ih u trenutku nastanka ovog dokumenta.
- Povezani plan: [TODO - Napredna pretraga](../../../docs/TODO.md)
- Povezani cilj: [Roadmap - Verzija 1.1](../../../docs/ROADMAP.md)
- Projektni kontekst: [AI agent project context](../../AI_AGENT_PROJECT_CONTEXT.md)
