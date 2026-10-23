2026-07

Odlučeno:

Sve kartice koriste border-radius 12 px.

Razlog:

Konzistentan dizajn.

Odlučeno:

Hero fotografija je dio identiteta projekta.

Razlog:

Vizuelno prepoznatljiv početak platforme.


"Korisnik nikada ne smije imati osjećaj da pregledava bazu podataka. Treba imati osjećaj da upoznaje priču."

Na svim listama prikazujemo samo onoliko podataka koliko korisnik može pregledati bez zamora. Za dodatne rezultate koriste se "Prikaži sve" ili paginacija.

## D-007

Datum: 2026-07-22

Naslov: Grave Detail koristi Content Cards

Razlog: Velike količine informacija bile su nepregledne.

Odluka: Sve sekcije koriste jedinstveni sistem kartica.

Status: Usvojeno.

## D-008

Datum: 2026-07-22

Naslov: Digitalizacija groba koristi jedinstvenu stranicu sa sekcijama, umjesto višekoračnog (wizard) obrasca.

Razlog: Terenski unos zahtijeva česte izmjene različitih dijelova zapisa (fotografije, GPS, osobe, natpis). Jedna stranica omogućava brz povratak na bilo koju sekciju bez prekidanja toka rada.

Status: Usvojeno.

## D-009 — Moderacija sadržaja prije javnog prikaza

Period: august–oktobar 2026.
Status: Implementirano za fotografije i groblja.

Odluka: Novi korisnički prijedlozi grobalja i pripadajuće fotografije čekaju odobrenje; odobravanje groblja ne podrazumijeva automatsko odobravanje njegovih fotografija. Javni prikazi koriste odobrene zapise.

Razlog: Kvalitet podataka, odgovornost i sprječavanje nenamjernog objavljivanja neprovjerenog sadržaja.

## D-010 — Uredničke dozvole kroz migraciju

Datum potvrde: oktobar 2026.
Status: Implementirano (`0027`).

Odluka: Grupa `Urednici` dobija prava `view_cemetery` i `change_cemetery` putem podatkovne migracije, bez proširivanja prava grupe `Stručnjaci`. Na produkciji je također zabilježeno postojeće pravo `add_cemetery`.

## D-011 — Produkcijska konfiguracija se ne pregazi pri deploymentu

Datum potvrde: oktobar 2026.
Status: Primijenjeno.

Odluka: Lokalni produkcijski `config/settings.py` i `.env` čuvaju se od prepisivanja; prije migracija pravi se svjež backup aktivne PostgreSQL/PostGIS baze. Koristiti provjere, fast-forward Git ažuriranje i provjeru servisa.
