# 00002 - Pregled ciljeva i realizacije projekta

- Vrijeme izvršenja prompta: `2026-10-21T15:52:02+02:00` (`Europe/Sarajevo`)
- Git grana: `main`
- Vrsta rada: pregled i objedinjavanje postojeće projektne dokumentacije

## Originalni prompt

```text
u folderu docs imaš dokumentaciju u vezi sa oviom projektom. Pregledaj dokumentaciju sa ciljevima i relaizacijom projekta. Sve što saznaš u vezi projekta upiši u AgentsDocs
```

## Opis zadatka

Pregledati sve tekstualne dokumente i vizuelne reference u `docs/`, povezati deklarisane ciljeve sa evidentiranom realizacijom i sačuvati samostalan pregled projekta u granski direktorij `AgentsDocs/Changes/main/`.

Ovaj izvještaj je sinteza dokumentacije. Nije nezavisna revizija izvornog koda, baze, Git historije niti trenutno aktivne produkcije. Izrazi **potvrđeno**, **implementirano**, **na čekanju** i **planirano** u nastavku prenose nivo sigurnosti koji navode projektni dokumenti.

## Pregledani izvori

- `docs/MANIFEST.md`
- `docs/README.txt`
- `docs/STATUS_2026-10-14.md`
- `docs/TODO.md`
- `docs/ROADMAP.md`
- `docs/SPRINTS.md`
- `docs/IDEAS.md`
- `docs/CHANGELOG.md`
- `docs/DECISIONS.md`
- `docs/DEPLOYMENT.md`
- `docs/DESIGN-PRINCIPLES.md`
- `docs/DESIGN.md`
- `docs/DESIGN_SYSTEM.md`
- `docs/UI_GUIDELINES.md`
- `docs/WGDS.md`
- `docs/WGDS/WG-PERSON-001.md`
- `docs/screenshots/Sprint1/s1-d.png`
- `docs/screenshots/Sprint1/s1-t.png`
- `docs/screenshots/Sprint1/s1-m.png`

## Sažetak projekta

Wiki Greblje je digitalni arhiv kulturne i sepulkralne baštine Bosne i Hercegovine. Njegov smisao nije samo evidentiranje podataka o grobljima, grobovima, osobama, fotografijama i natpisima, nego očuvanje priča pojedinačnih života i sjećanja za buduće generacije. Osnovna vrijednosna poruka je da kulturna i sepulkralna baština pripada svima i da se čuva zajedničkim, postepenim doprinosima.

Projekat se namjerno ne oblikuje kao društvena mreža, administrativni panel ili hladna baza podataka. Korisnik treba imati osjećaj da upoznaje priču, a ne da pregledava tabelu zapisa. Interfejs zato treba biti miran, dostojanstven i nenametljiv, dok fotografije i historijski sadržaj imaju prednost nad dekoracijom.

## Razvojni proces

Dokumentovani slijed rada je:

1. razgovor o ideji;
2. definisanje cilja;
3. dizajn korisničkog iskustva;
4. dizajn interfejsa;
5. implementacija;
6. testiranje;
7. dokumentovanje;
8. Git commit;
9. deployment.

Dokumentacija konsolidovana 14.10.2026. zasniva se na sačuvanim bilješkama i potvrđenim radnim sesijama. Oznake poput „otvoreno“, „provjeriti“ i „nije potvrđeno“ ne znače da je funkcija implementirana. Numeričke oznake verzija 1.0, 1.1 i 2.0 predstavljaju ciljne grupe funkcionalnosti, a ne automatsku potvrdu izdanja.

## Ciljevi proizvoda

### Verzija 1.0

- digitalizacija grobalja;
- evidencija grobova;
- fotografije;
- osobe;
- komentari;
- historija izmjena.

### Verzija 1.1

- napredna pretraga;
- QR kodovi na lokaciji;
- poboljšan prikaz fotografija.

### Verzija 2.0

- interaktivna vremenska linija;
- porodična stabla;
- AI pomoć pri čitanju natpisa;
- mobilna PWA aplikacija.

### Dodatne ideje

- 3D modeli stećaka;
- historijske fotografije;
- „Danas u historiji“;
- virtualna šetnja grobljem;
- glasovno pretraživanje;
- digitalna izložba.

Ideje nisu potvrđene implementacije. Nakon završetka Grave Detail v2 zabilježeno je da se dodatna poboljšanja tog prikaza rade samo kao završno dotjerivanje nakon ostalih modula.

## Evidentirana realizacija

### Sprint 1 - Foundations, juli 2026.

Status je dokumentovan kao završen. Uspostavljeni su:

- responsive početna stranica;
- hero sekcija i hero pozadinska fotografija;
- responsive navigacija;
- osnovne UI komponente;
- Bootstrap Icons;
- kartice fotografija i grobova;
- footer;
- komponentni vizuelni pristup;
- Git workflow, projektna dokumentacija i produkcijski deployment.

Vizuelne reference prikazuju tamnu gornju navigaciju, veliki fotografski hero, akcije „Pretraži“ i „Dodaj grob“, centralnu pretragu i statističke kartice. Desktop raspored ima statistike u jednom redu; uži prikazi sklapaju navigaciju u hamburger i prelamaju/statističke kartice, dok telefon prebacuje hero akcije i polja pretrage u vertikalni tok. Brojevi na starim Sprint 1 snimcima (4 groblja, 22 groba, 20 osoba, 29 fotografija i 4 korisnika) historijska su vizuelna referenca, ne trenutno stanje.

### Sprint 2 - Grave Detail v2, juli 2026.

Status je dokumentovan kao završen. Obuhvaćeni su:

- hero;
- galerija;
- osobe;
- natpis;
- lokacija;
- najbliži grobovi;
- povezane osobe;
- komentari;
- historija izmjena.

Zaključci sprinta su da je manje više, fotografija mora biti velika, redoslijed informacija važniji je od količine i ista komponenta treba biti ponovo upotrebljiva na više mjesta. Grave Detail je preuređen kroz jedinstvene Content Cards.

### Sprint 3 - Digitalizacija groba

Osnovni tok je implementiran, ali su daljnje dorade otvorene. Cilj nije bio samo napraviti formu nego osmisliti jednostavan, dostojanstven i ugodan terenski proces digitalizacije.

Dokumentovana realizacija uključuje:

- jedinstvenu stranicu umjesto višekoračnog wizard obrasca;
- sekcije za grob, lokaciju, fotografije, osobe i natpis;
- višestruki upload fotografija;
- izbor glavne fotografije;
- pomoćni OCR tok za fotografiju natpisa;
- uloge `Urednici` i `Stručnjaci`, koje utiču na dostupnost stručnih klasifikacijskih polja;
- ograničavanje izbora groblja na odobrena groblja.

Jedna stranica odabrana je zato što terenski unos traži često vraćanje između GPS podataka, fotografija, osoba i natpisa.

### Klasifikacija spomenika i očuvanosti, august-septembar 2026.

Prema potvrđenim migracijama `0018`-`0025`, implementirani su:

- tipologija spomenika;
- tradicije;
- motivi;
- stanje očuvanosti;
- obrasci degradacije;
- položaj spomenika;
- pripadajući standardni podaci i stručna polja.

### Fotografije i moderacija

Implementirani su statusi `pending`, `approved` i `rejected`. Javni prikazi filtriraju samo odobrene zapise. Fotografija se tretira kao historijski dokument, a ne dekoracija. Direktna zaštita URL-ova fotografija na čekanju ostaje predmet provjere u skladu s budućim zahtjevima privatnosti.

### Prijedlog i moderacija groblja, oktobar 2026.

Dokumentovan je implementiran tok u commitu `2f94d59` (`Add cemetery proposal and moderation workflow`):

- prijavljeni korisnici mogu predložiti groblje i njegove fotografije;
- groblje ima status i autora prijedloga;
- urednici mogu odobriti ili odbiti prijedlog;
- odobravanje groblja i odobravanje njegovih fotografija dva su nezavisna postupka;
- javne liste i detalji prikazuju samo odobrena groblja i fotografije;
- obrazac za grob nudi samo odobrena groblja;
- javni obrazac koristi Leaflet mapu s MapTiler podlogom;
- marker se može postaviti i pomjeriti, a koordinate su opcionalne;
- korisniku treba jasno objasniti da prijedlog čeka pregled i prikazati jednostavnu potvrdu slanja.

Migracije `0026` i `0027` primijenjene su na produkcijskom DELL računaru. Migracija `0027` grupi `Urednici` daje `view_cemetery` i `change_cemetery`; na DELL-u je zabilježeno i postojeće `add_cemetery`, ali to pravo nije rezultat namjene nove migracije. Grupa `Stručnjaci` nije proširena ovom odlukom.

### Karte

MapTiler je uveden za prikaz karata i zamijenio je preostale OpenStreetMap tile slojeve. Mapa je pomoćni sadržaj i prema UI pravilima ne treba biti prva stvar koju korisnik vidi.

### Ispravka kreiranja prazne osobe, 14.10.2026.

`PublicGraveForm.save()` je ispravljen tako da kreira `Person` samo kada postoji stvarni podatak o osobi: ime ili prezime, godina rođenja ili smrti, spol, fotografija ili napomena. Djelimični podatak, npr. samo godina smrti, i dalje stvara zapis nepoznate osobe koji čeka odobrenje.

Ispravka je ručno provjerena kroz javni obrazac i admin: dva testna mezara bila su na čekanju, ali samo jedna osoba, ona s godinom smrti 1890. Commit `be3a0ec` (`Fix empty person creation when submitting graves`) poslan je na `origin/main`. Automatski regresijski test još nije dodat, a commit u trenutku posljednjeg statusa nije prenesen na DELL jer je planiran grupni deployment s narednim promjenama.

## Posljednje dokumentovano tehničko i produkcijsko stanje

Presjek stanja nosi datum 14.10.2026.

- Posljednja potvrđena produkcijska cjelina je commit `2f94d59`.
- DELL `main` i GitHub `main` bili su usklađeni na tom commitu.
- Migracije `0026` i `0027` bile su označene kao primijenjene.
- Django `check` nije prijavio sistemske greške.
- `collectstatic` je prijavio 1 kopiranu i 250 neizmijenjenih datoteka.
- Restart i javna dostupnost nisu potkrijepljeni sačuvanim HTTP komandnim izlazima; korisnik je naknadno naveo da „izgleda da je sve ok“.
- Commit `be3a0ec` je noviji deploy-ready rad na GitHubu, ali prema posljednjem statusu nije bio na DELL-u.

## Evidentirano stanje sadržaja

Na dostavljenom snimku stranice Doprinosi dokumentovano je:

- 203 odobrena doprinosa;
- 49 evidentiranih grobova;
- 23 evidentirane osobe;
- 69 fotografija;
- 4 korisnika u odjeljku najaktivnijih doprinositelja.

Ovo su brojevi prikazani na tadašnjoj stranici, a ne historijska suma, audit baze ili trenutno garantovano stanje.

## Dizajnerska filozofija i pravila

### Opći karakter

- Interfejs treba biti miran, pregledan i dostojanstven.
- Sadržaj je važniji od dizajna; dizajn treba pomagati istraživanju i ne smije ga zasjeniti.
- Izbjegavaju se agresivne/jarke boje i nepotrebne animacije.
- Koristi se mnogo praznog prostora, manje linija i okvira.
- Liste prikazuju količinu podataka koju korisnik može pregledati bez zamora; ostatak ide kroz „Prikaži sve“ ili paginaciju.
- Heritage ilustracije predstavljaju kulturno-historijski kontekst i period, a ne pojedince ili stereotipe.

### Vizuelni jezik

- Projektna primarna boja je tamnozelena.
- Pozadine su vrlo svijetle, kartice bijele, akcenti diskretni.
- Sve kartice imaju radius od 12 px.
- Koriste se Hero Card, Content Card, Gallery Card, Person Card i Record Block.
- Bootstrap Icons su standard; uz naslov ide najviše jedna ikona.
- Naslovi su izraženi, osnovni tekst miran, a natpis treba izgledati kao dokument.
- Fotografije trebaju biti dovoljno velike i ne svoditi se na malu sličicu bez potrebe.
- Prazna stanja trebaju biti ljudska i kontekstualna, npr. „Za ovaj grob još nema fotografija“, a ne generičko „No data“.
- Status moderacije ne treba dominirati javnim dizajnom; neodobreni zapisi se ne prikazuju javno.
- Stare stavke o osnovnom fontu, bojama i razmacima nisu numerički potvrđene dok se stvarne vrijednosti ne provjere u CSS-u.

Moto UI smjernica je: „Ne digitalizujemo podatke. Digitalizujemo sjećanja.“

### CSS i komponente

Dokumentovana je modularna organizacija CSS-a:

- zajedničke komponente: `wg-card.css`, `forms.css`, `buttons.css`, `badges.css`, `hero.css`;
- moduli: `person.css`, `gallery.css`, `cemetery.css`, `grave.css`, `login.css`;
- stranice: `home.css`, `grave-entry.css`;
- za stranice grobalja naveden je `graves/static/graves/css/modules/cemetery.css`.

Zajedničke WG komponente koriste prefiks `wg`, npr. `.wg-card` i `.wg-card-title`. U baznu WG Card komponentu smiju ići samo svojstva koja dijele sve kartice.

Content Card v1 koristi se na Cemetery Detail, Grave Detail i Person Detail; Cemetery Card v1 na Cemetery List; Grave Card v1 na Home i Cemetery Detail; Hero v1 na Home.

Sprint 3.1 bilježi uvođenje WG Card i migraciju Person Entry i Record Card, dok su Gallery Card, Location Card i Login Card u toj evidenciji ostali nezavršeni.

## WG-PERSON-001 - Heritage Person Panel

Komponenta je standardni prikaz osobe povezane s grobom i treba biti referentni izgled gdje god se prikazuje osoba. Inspiracija su arhivska dokumentacija, stari foto-albumi, muzejski katalozi i historijske publikacije.

Pravila komponente:

- fotografija je primarni vizuelni element;
- ime je primarni tekstualni element;
- godine života su sekundarne;
- bilješke su tercijarne;
- dekoracije i broj boja ostaju minimalni;
- Heritage okvir treba podsjećati na staru arhivsku fotografiju;
- komponenta mora imati dovoljno praznog prostora;
- desktop i tablet zadržavaju fotografiju lijevo i podatke desno;
- tek ispod 480 px prelazi se u jednu kolonu.

Predviđeni dijelovi su Photo, Header, Metadata i Notes. Predviđena stanja su originalna fotografija, heritage portret, bez bilješki i bez fotografije. Buduća proširenja obuhvataju porodične veze, historijske izvore, galeriju, timeline, vojnu službu, zanimanje, nagrade i dokumente.

I `docs/WGDS.md` i `docs/WGDS/WG-PERSON-001.md` zadržavaju status **In Development**. Nije dokumentovana potpuna vizuelna i responsive provjera svih stanja, pa komponentu ne treba predstavljati kao završenu.

## Arhitektura i produkcijsko okruženje poznati iz dokumentacije

- Aplikacija koristi Django.
- Aktivna produkcijska baza je PostgreSQL 16 s PostGIS-om, ne lokalni `db.sqlite3`.
- Lokalni razvojni put je `C:/wiki-groblje` na Windows/Git Bash okruženju.
- Produkcijski put je `/opt/wiki-greblje` na DELL/Linux računaru.
- Python virtualno okruženje je `venv`.
- Aplikaciju poslužuje Gunicorn servis `wiki-greblje.service`.
- Dokumentovana domena je `wikigreblje.ba`.
- Produkcijski `config/settings.py` sadrži lokalne HTTPS, host i CSRF prilagodbe.
- `.env` sadrži tajne i parametre baze te se ne smije objavljivati.

## Siguran deployment postupak

1. Lokalno pokrenuti `python manage.py check`, testove i `git diff --check`, pregledati promjene i commitovati ih.
2. Poslati commit na GitHub `main`, ili pregledati i spojiti radnu granu, pa potvrditi hash.
3. Na DELL-u provjeriti Git stanje, zadnji commit, servis i aktivnu bazu.
4. Prije migracija napraviti svjež backup aktivnog PostgreSQL/PostGIS-a, potvrditi uspjeh `pg_dump` i sadržaj arhive te kopirati produkcijski `settings.py` izvan repozitorija.
5. Sačuvati lokalne izmjene `config/settings.py`, koristiti fast-forward-only pull i pažljivo vratiti stash; stati ako nastane konflikt.
6. Pokrenuti Django provjeru, `showmigrations`, `migrate --plan` i pregled plana.
7. Migrirati tek nakon potvrđenog backupa i plana.
8. Pokrenuti `collectstatic --noinput`.
9. Restartovati servis, provjeriti status i po potrebi logove.
10. Provjeriti HTTP odgovore, javne stranice, prijavu, urednička prava i puni tok predlaganja/odobravanja te zabilježiti rezultat.

Stari stash-evi i nepoznate lokalne datoteke ne smiju se brisati bez pregleda. Tipični problemi su pogrešna Python/venv putanja ili `.env`, preskočen `collectstatic`, browser cache, promjene na pogrešnoj grani, neprimijenjene migracije, nerestartovan Gunicorn te greške dozvola ili pogrešna baza pri backupu.

## Backup stanje i ograničenja

Pokušaj cijelog `pg_dump` pod korisnikom `wiki_user` prijavio je `permission denied for schema tiger`, zbog čega nastali dump nije cjelovit i ne smije se tretirati kao valjan puni backup.

Ponovljeni backup samo sheme `public` uspješno je napravljen kao `backups/wiki-greblje-public-20261010-182840.dump`; terminal je prikazao veličinu 164 KB, a `pg_restore -l` je prikazao aplikacijske tabele. Ograničenja:

- nije backup svih shema/cijele baze;
- nije potvrđen stvarnim restore testom;
- prije ozbiljnih promjena treba osigurati i provjeriti cjelovit postupak oporavka.

## Otvorene provjere najvišeg prioriteta

Prvi sljedeći test treba proći cijeli produkcijski tok:

1. prijavljeni korisnik predlaže novo groblje i fotografiju;
2. potvrđuje se da nijedno nije javno prije odobrenja;
3. urednik odobrava groblje, ali ostavlja fotografiju na čekanju;
4. potvrđuje se nezavisnost statusa i potom odobrava fotografija;
5. korisnik predlaže mezar u odobrenom groblju i potvrđuje da neodobreno groblje nije ponuđeno;
6. pregledaju se logovi i greške nakon testa.

Dodatno treba:

- potvrditi HTTP statuse i funkcionalnost relevantnih javnih stranica nakon restarta;
- pregledati admin akcije koje mijenjaju status putem GET zahtjeva;
- provjeriti direktne URL-ove fotografija na čekanju;
- izvršiti test povrata PostgreSQL/PostGIS backupa u izdvojenu bazu;
- dodati regresijske testove za unos mezara bez osobe i s djelimičnim podacima;
- poboljšavati OCR i provjeriti preciznost na stvarnim natpisima;
- pregledati nezavršene WGDS komponente i sva stanja WG-PERSON-001.

## Backlog i djelimično realizovane cjeline

### Djelimično ili nepotpuno potvrđeno

- OCR pomoć pri unosu natpisa postoji kao funkcionalni prototip, ali stvarna preciznost nije potvrđena.
- Osnovni tok Sprinta 3 radi, ali daljnje dorade ostaju otvorene.
- WG Design System postoji i koristi se, ali katalog komponenti nije potpuno završen ni vizuelno verificiran.
- Novi tok prijedloga/moderacije je prenesen na DELL, ali potpuni produkcijski korisnički test nije dokumentovan.
- Produkcijska dostupnost nakon posljednjeg restarta ima samo korisničku potvrdu, bez sačuvanog HTTP izlaza.

### Planirano bez potvrde implementacije

- QR kodovi;
- napredna pretraga, čiji obim tek treba razlikovati od postojeće pretrage;
- PWA;
- porodična stabla;
- historijski slojevi karte;
- interaktivni timeline groblja;
- 3D modeli;
- virtualne šetnje;
- ostale ideje iz `IDEAS.md`.

## Ključne projektne odluke

- Kartice koriste radius 12 px radi vizuelne konzistentnosti.
- Hero fotografija je dio identiteta projekta.
- Grave Detail koristi Content Cards radi čitljivosti velikog broja informacija.
- Digitalizacija groba koristi jednu stranicu sa sekcijama radi fleksibilnog terenskog rada.
- Novi sadržaj prolazi moderaciju prije javnog prikaza radi kvaliteta, odgovornosti i zaštite od nenamjerne objave.
- Groblje i njegove fotografije odobravaju se odvojeno.
- Uredničke dozvole se dodjeljuju podatkovnom migracijom.
- Produkcijski `config/settings.py` i `.env` ne smiju biti prepisani deploymentom.
- Prije migracija obavezan je svjež i provjeren backup aktivne baze.
- Nove cjeline poslije Sprinta 3 nisu retroaktivno nazvane Sprint 4/5 bez odluke tima.

## Zaključak o odnosu ciljeva i realizacije

Jezgro ciljeva verzije 1.0 prema dokumentaciji je uglavnom realizovano: postoje evidencija grobalja, grobova, osoba i fotografija, komentari, historija izmjena, responsive javni prikazi, proces digitalizacije, moderacija i stručna klasifikacija. Projekat je otišao i dalje od prvobitnog osnovnog opsega kroz korisničke prijedloge grobalja, odvojenu moderaciju fotografija, MapTiler karte i modele stanja očuvanosti.

Najvažniji nedovršeni posao nije samo dodavanje novih funkcija nego dokazivanje pouzdanosti postojećeg toka: end-to-end produkcijski test, HTTP provjere, sigurnost statusnih admin akcija, kontrola pristupa neodobrenim fotografijama, restore test backupa i automatska regresijska pokrivenost ispravke prazne osobe.

Ciljevi verzija 1.1 i 2.0 većinom ostaju backlog. OCR je jedini jasno dokumentovan element iz naprednijeg plana koji postoji u prototipskom obliku, ali još nije dovoljno potvrđen za stvarne natpise.

## Promjene napravljene za ovaj prompt

- Pregledano je svih 16 tekstualnih dokumenata u `docs/`.
- Pregledane su sve tri Sprint 1 vizuelne reference za desktop, tablet i telefon.
- Kreiran je ovaj objedinjeni izvještaj `AgentsDocs/Changes/main/00002_review_project_documentation.md`.
- Nisu mijenjani aplikacijski kod, konfiguracija, baza, postojeća projektna dokumentacija ni produkcija.
- `AGENTS.md` nije mijenjan jer već sadrži važeći link na direktorij `AgentsDocs/Changes/`, pa dodavanjem ovog izvještaja indeks nije postao zastario.

## Razlozi za način izvedbe

- Podaci su razdvojeni na potvrđenu implementaciju, djelimično potvrđeno stanje i backlog da se plan ne bi pogrešno prikazao kao gotova funkcionalnost.
- Produkcijske tvrdnje su prenesene s istim ograničenjima koja navode izvori, posebno za HTTP provjeru, backup i commit `be3a0ec`.
- Stari brojevi sa Sprint 1 snimaka odvojeni su od novijeg snimka stranice Doprinosi jer predstavljaju različite trenutke i svrhe.
- Izvještaj je namjerno samostalan kako bi budući agent ili drugi račun mogao razumjeti projekat bez ponovnog čitanja svih izvora, ali su izvorni dokumenti i dalje autoritativni za detalje.
- Aktivna grana očitana je iz `.git/HEAD` zato što izvršna datoteka `git` nije dostupna na `PATH` u ovoj sesiji.

## Povezani izvještaji

- Prethodni: [00001 - Create AGENTS.md and Project Documentation Index](./00001_create_agents_md.md)
- Naknadni izvještaji: nema ih u trenutku nastanka ovog dokumenta.
