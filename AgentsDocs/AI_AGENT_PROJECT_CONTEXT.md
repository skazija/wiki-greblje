# Wiki Greblje - kontekst projekta za AI agente

## Svrha dokumenta

Ovaj dokument je početna tačka za AI agenta koji radi na projektu Wiki Greblje. Objedinjuje ciljeve i rezultate do sada evidentiranog rada na osnovu dokumentacije u [`docs/`](../docs/), ali ne zamjenjuje izvorne specifikacije, statusne dokumente ni operativne upute.

Prije projektne izmjene agent treba pročitati:

1. [`AGENTS.md`](../AGENTS.md) zbog stalnih pravila rada i indeksa dokumentacije;
2. ovaj dokument radi brzog razumijevanja projekta;
3. izvorni dokument vezan za područje koje mijenja;
4. najnoviji izvještaj u [`AgentsDocs/Changes/<grana>/`](Changes/) radi konteksta nedavnog rada.

## Kako tumačiti stanje

Ovaj pregled razlikuje četiri nivoa sigurnosti:

- **Potvrđeno** - dokumentacija bilježi završenu implementaciju ili izvršenu provjeru.
- **Implementirano, čeka provjeru** - funkcija je evidentirana u kodu/deploymentu, ali potpuni produkcijski ili vizuelni test nije dokumentovan.
- **Djelimično** - postoji osnovni tok ili prototip, ali cilj nije potpuno završen.
- **Planirano** - ideja ili roadmap stavka bez potvrđene implementacije.

Referentni konsolidovani status projekta nosi datum **14.10.2026.** Kasniji agent ne smije pretpostaviti da je tada otvorena stavka završena bez novijeg izvještaja ili vlastite provjere. Verzije 1.0, 1.1 i 2.0 u roadmapu predstavljaju ciljeve, a ne automatski potvrđena izdanja.

## Identitet i svrha projekta

Wiki Greblje je digitalni arhiv kulturne i sepulkralne baštine Bosne i Hercegovine. Projekat čuva tragove pojedinačnih života kroz groblja, grobove, osobe, fotografije i natpise.

Temeljni cilj nije izgradnja baze podataka radi same tehnologije, nego očuvanje priča i sjećanja za buduće generacije. Projekat polazi od uvjerenja da kulturna i sepulkralna baština pripada svima i da se čuva zajedničkim doprinosima, korak po korak.

Korisnik ne treba imati osjećaj da koristi administrativni sistem ili društvenu mrežu. Treba imati osjećaj da upoznaje historijski zapis i ljudsku priču. Iz toga proizlaze sva glavna pravila proizvoda, moderacije i dizajna.

Izvori: [Manifest](../docs/MANIFEST.md), [UI smjernice](../docs/UI_GUIDELINES.md), [Design System](../docs/DESIGN_SYSTEM.md).

## Razvojni princip

Dokumentovani redoslijed razvoja je:

1. razgovor o ideji;
2. definisanje cilja;
3. dizajn korisničkog iskustva;
4. dizajn interfejsa;
5. implementacija;
6. testiranje;
7. dokumentovanje;
8. Git commit;
9. deployment.

Agent treba zadržati ovaj slijed u mjeri koju zahtijeva zadatak i ne proglašavati plan ili implementaciju završenom bez odgovarajuće provjere.

Izvor: [Development workflow](../docs/README.txt).

## Ciljevi i ostvareni rezultati

### 1. Vizuelni i tehnički temelj javnog interfejsa

**Cilj:** Izgraditi prepoznatljivu, responsive početnu stranicu i zajednički vizuelni jezik koji sadržaj stavlja ispred interfejsa.

**Ostvareno:**

- Sprint 1, Foundations, dokumentovan je kao završen u julu 2026.
- Implementirani su responsive početna stranica, navigacija, hero, kartice fotografija i grobova, footer i Bootstrap Icons.
- Uspostavljeni su komponentni UI pristup, Git workflow, projektna dokumentacija i produkcijski deployment.
- Desktop, tablet i mobilne reference potvrđuju prilagodljivi raspored hero akcija, pretrage i statističkih kartica.
- Hero fotografija prihvaćena je kao dio identiteta projekta.

**Status:** **Potvrđeno.** Brojevi prikazani na starim Sprint 1 ekranima predstavljaju historijsku vizuelnu referencu, ne trenutno stanje baze.

Izvori: [Sprint history](../docs/SPRINTS.md), [Changelog](../docs/CHANGELOG.md), [Decisions](../docs/DECISIONS.md), [desktop](../docs/screenshots/Sprint1/s1-d.png), [tablet](../docs/screenshots/Sprint1/s1-t.png), [mobile](../docs/screenshots/Sprint1/s1-m.png).

### 2. Dostojanstven i pregledan prikaz groba

**Cilj:** Pretvoriti detalj groba u čitljivu priču, s fotografijom i logičnim redoslijedom informacija, umjesto pretrpanog zapisa.

**Ostvareno:**

- Sprint 2, Grave Detail v2, dokumentovan je kao završen.
- Uvedeni su hero, galerija, osobe, natpis, lokacija, najbliži grobovi, povezane osobe, komentari i historija izmjena.
- Sekcije koriste Content Cards radi konzistentnosti i lakšeg čitanja.
- Potvrđeni principi su: manje je više, fotografija mora biti velika, redoslijed informacija važniji je od količine i komponente trebaju biti ponovo upotrebljive.

**Status:** **Potvrđeno.** Daljnje promjene Grave Detail v2 zamišljene su kao završno dotjerivanje nakon ostalih modula.

Izvori: [Sprint history](../docs/SPRINTS.md), [Changelog](../docs/CHANGELOG.md), [Decisions](../docs/DECISIONS.md), [Ideas](../docs/IDEAS.md).

### 3. Jednostavan terenski proces digitalizacije groba

**Cilj:** Napraviti ugodan i dostojanstven proces digitalizacije, a ne samo tehnički obrazac za unos.

**Ostvareno:**

- Jedinstvena stranica sadrži sekcije za grob, lokaciju, fotografije, osobe i natpis.
- Jedna stranica je svjesno odabrana umjesto wizard toka jer terenski rad traži često vraćanje između različitih dijelova zapisa.
- Podržani su višestruki upload fotografija i izbor glavne fotografije.
- Uveden je pomoćni OCR tok za fotografiju natpisa.
- Uloge `Urednici` i `Stručnjaci` utiču na dostupnost stručnih klasifikacijskih polja.
- Izbor groblja u obrascu ograničen je na odobrena groblja.

**Status:** **Djelimično.** Osnovni tok je implementiran. OCR postoji kao funkcionalni prototip, ali preciznost na stvarnim natpisima nije potvrđena. Daljnje dorade procesa ostaju otvorene.

Izvori: [Sprint history](../docs/SPRINTS.md), [Decisions](../docs/DECISIONS.md), [Status](../docs/STATUS_2026-10-14.md), [TODO](../docs/TODO.md).

### 4. Evidencija stručnih karakteristika spomenika

**Cilj:** Omogućiti strukturirano bilježenje vrste i kulturnog konteksta spomenika te njegovog fizičkog stanja.

**Ostvareno:**

- Implementirane su tipologija spomenika, tradicije i motivi.
- Implementirani su stanje očuvanosti, obrasci degradacije i položaj spomenika.
- Dokumentacija realizaciju veže za potvrđene migracije `0018`-`0025` iz perioda august-septembar 2026.

**Status:** **Potvrđeno prema evidenciji migracija.**

Izvori: [Changelog](../docs/CHANGELOG.md), [Sprint history](../docs/SPRINTS.md), [TODO](../docs/TODO.md).

### 5. Kontrolisana objava korisničkog sadržaja

**Cilj:** Zaštititi kvalitet, odgovornost i privatnost javnog arhiva tako da novi sadržaj ne postane javno vidljiv prije uredničke provjere.

**Ostvareno:**

- Fotografije imaju statuse `pending`, `approved` i `rejected`.
- Javni prikazi filtriraju samo odobrene fotografije i groblja.
- Prijavljeni korisnici mogu predložiti novo groblje i fotografije.
- Groblje čuva status i autora prijedloga.
- Urednici mogu odobriti ili odbiti groblje.
- Groblje i njegove fotografije odobravaju se nezavisno; odobreno groblje ne objavljuje automatski njegove fotografije.
- Obrazac za grob nudi samo odobrena groblja.
- Korisniku treba jasno prikazati da prijedlog čeka pregled.

**Status:** **Implementirano, čeka provjeru.** Commit `2f94d59` (`Add cemetery proposal and moderation workflow`) i migracije `0026`/`0027` evidentirani su na DELL produkciji, ali potpuni end-to-end korisnički test nije dokumentovan kao završen.

**Otvorene sigurnosne provjere:**

- pregled admin akcija koje mijenjaju status putem GET zahtjeva;
- provjera direktnog pristupa URL-ovima fotografija na čekanju;
- potvrda da se nijedan neodobreni zapis ne pojavljuje na javnim karticama, listama ili galerijama.

Izvori: [Decisions](../docs/DECISIONS.md), [Status](../docs/STATUS_2026-10-14.md), [TODO](../docs/TODO.md), [Design principles](../docs/DESIGN-PRINCIPLES.md).

### 6. Uredničke dozvole

**Cilj:** Omogućiti urednicima pregled i promjenu prijedloga groblja bez nepotrebnog širenja stručnih prava.

**Ostvareno:**

- Podatkovna migracija `0027` grupi `Urednici` daje `view_cemetery` i `change_cemetery`.
- Na DELL-u je zabilježeno i postojeće pravo `add_cemetery`, ali ono nije rezultat namjene ove migracije.
- Grupa `Stručnjaci` nije proširena ovom odlukom.

**Status:** **Potvrđeno.**

Izvori: [Decisions](../docs/DECISIONS.md), [Status](../docs/STATUS_2026-10-14.md).

### 7. Lokacija i karte

**Cilj:** Omogućiti unos i prikaz geografskog konteksta bez potiskivanja glavnog historijskog sadržaja.

**Ostvareno:**

- U obrascu prijedloga groblja koristi se Leaflet mapa s MapTiler podlogom.
- Marker se može postaviti i pomjeriti; koordinate su opcionalne.
- MapTiler je zamijenio preostale OpenStreetMap tile slojeve.
- Dizajnersko pravilo nalaže da mapa bude pomoćni sadržaj, ne prva stvar koju korisnik vidi.

**Status:** **Potvrđeno prema dokumentaciji.**

Izvori: [Design notes](../docs/DESIGN.md), [Changelog](../docs/CHANGELOG.md), [UI guidelines](../docs/UI_GUIDELINES.md).

### 8. Sprečavanje praznih zapisa osobe

**Cilj:** Ne kreirati praznu osobu kada korisnik prijavi mezar bez podataka o osobi, ali sačuvati legitimne djelimične podatke.

**Ostvareno:**

- `PublicGraveForm.save()` kreira `Person` samo ako postoji stvarni podatak: ime/prezime, godina rođenja/smrti, spol, fotografija ili napomena.
- Samo jedan stvarni podatak, npr. godina smrti, dovoljan je da se kreira nepoznata osoba koja čeka odobrenje.
- Ručna provjera kroz javni obrazac i admin potvrdila je dva mezara na čekanju i samo jednu osobu, onu s unesenom godinom smrti 1890.
- Ispravka je commitovana kao `be3a0ec` (`Fix empty person creation when submitting graves`) i poslana na `origin/main`.

**Status:** **Lokalno potvrđeno, produkcijski deploy nije potvrđen.** Prema statusu od 14.10.2026. commit je namjerno ostavljen za naredni grupni DELL deployment. Automatski regresijski test nije dodat.

Izvori: [Status](../docs/STATUS_2026-10-14.md), [TODO](../docs/TODO.md), [Changelog](../docs/CHANGELOG.md).

### 9. Dizajn sistem i ponovna upotreba komponenti

**Cilj:** Održati konzistentan, tih i proširiv interfejs kroz zajedničke komponente i modularni CSS.

**Ostvareno:**

- Uveden je WG Card i `wg-` prefiks za zajedničke komponente.
- Zajednički CSS je razdvojen na komponente, module i stranice.
- Content Card v1 koristi se na detaljima groblja, groba i osobe.
- Cemetery Card v1 koristi se na listi grobalja.
- Grave Card v1 koristi se na početnoj i detalju groblja.
- Hero v1 koristi se na početnoj.
- Person Entry i Record Card zabilježeni su kao migrirani na WG Card.

**Status:** **Djelimično.** Design System postoji i primjenjuje se, ali Gallery Card, Location Card i Login Card bile su otvorene u Sprintu 3.1. Nije potvrđeno da je cijeli WGDS katalog završen.

Izvori: [Design System](../docs/DESIGN_SYSTEM.md), [Design notes](../docs/DESIGN.md), [UI guidelines](../docs/UI_GUIDELINES.md).

### 10. Heritage Person Panel (`WG-PERSON-001`)

**Cilj:** Standardizovati dostojanstven prikaz osobe povezane s grobom, inspirisan arhivima, starim foto-albumima, muzejskim katalozima i historijskim publikacijama.

**Planirana svojstva:**

- fotografija kao primarni vizuelni element;
- ime kao primarni tekst, godine kao sekundarni i bilješke kao tercijarni;
- Heritage okvir fotografije;
- minimalne boje i dekoracije, uz dovoljno praznog prostora;
- dvije kolone na desktopu i tabletu;
- jedna kolona tek ispod 480 px;
- stanja: originalna fotografija, heritage portret, bez bilješki i bez fotografije.

**Status:** **Djelimično / In Development.** Potpuna vizuelna i responsive verifikacija svih stanja nije dokumentovana. Agent ne smije komponentu proglasiti završenom samo zato što postoji specifikacija.

Izvori: [WGDS overview](../docs/WGDS.md), [WG-PERSON-001](../docs/WGDS/WG-PERSON-001.md).

## Funkcionalni obim koji dokumentacija smatra implementiranim

Konsolidovani roadmap kao implementirano ili potvrđeno navodi:

- osnovnu evidenciju grobalja;
- evidenciju grobova;
- evidenciju osoba;
- fotografije;
- komentare;
- historiju izmjena;
- responsive prikaze;
- moderaciju fotografija;
- korisnički prijedlog groblja i uredničko odobravanje;
- klasifikaciju spomenika i stanja očuvanosti;
- MapTiler prikaze.

Ovo znači da je jezgro prvobitnog cilja verzije 1.0 uglavnom realizovano. Ipak, status pojedinačne funkcije treba provjeriti u najnovijem dokumentu i kodu prije promjene ili produkcijske tvrdnje.

Izvor: [Roadmap](../docs/ROADMAP.md).

## Vizuelna pravila koja agent mora očuvati

- Interfejs je miran, pregledan i dostojanstven.
- Sadržaj je uvijek važniji od dizajna.
- Primarna boja je tamnozelena; pozadina vrlo svijetla; kartice bijele; akcenti diskretni.
- Ne koristiti jarke boje, agresivne efekte ni nepotrebne animacije.
- Sve kartice koriste radius od 12 px.
- Koristiti više praznog prostora, manje linija i manje okvira.
- Bootstrap Icons su standard; uz naslov se koristi najviše jedna ikona.
- Fotografija je dokument, ne dekoracija, i treba biti dovoljno velika.
- Natpis treba vizuelno djelovati kao dokument.
- Mapa je pomoćni sadržaj.
- Prazno stanje mora biti ljudsko i kontekstualno, ne generičko „No data“.
- Liste prikazuju samo količinu informacija koju korisnik može pregledati bez zamora; koristiti „Prikaži sve“ ili paginaciju za ostatak.
- Heritage ilustracije predstavljaju kulturno-historijski kontekst i period, ne stvarne pojedince ni stereotipe.
- Statusi moderacije ne dominiraju javnim dizajnom; neodobreni sadržaj se ne prikazuje javno.
- Ne izmišljati numeričke vrijednosti fonta, boja ili razmaka koje nisu potvrđene u CSS-u.

Moto interfejsa: **„Ne digitalizujemo podatke. Digitalizujemo sjećanja.“**

Izvori: [UI guidelines](../docs/UI_GUIDELINES.md), [Design principles](../docs/DESIGN-PRINCIPLES.md), [Design notes](../docs/DESIGN.md), [Decisions](../docs/DECISIONS.md).

## Poznato tehničko i produkcijsko okruženje

- Aplikacija koristi Django.
- Aktivna produkcijska baza je PostgreSQL 16 s PostGIS-om, ne lokalni SQLite.
- Lokalni razvojni put je `C:/wiki-groblje` na Windows/Git Bash okruženju.
- Produkcija je u `/opt/wiki-groblje` na DELL/Linux računaru.
- Python virtualno okruženje je `venv`.
- Gunicorn servis je `wiki-greblje.service`.
- Dokumentovana domena je `wikigreblje.ba`.
- Produkcijski `config/settings.py` sadrži lokalne HTTPS, host i CSRF postavke.
- `.env` sadrži tajne i parametre baze i ne smije biti objavljen.

Posljednja potvrđena produkcijska cjelina u statusu od 14.10.2026. bila je:

- commit `2f94d59` na GitHub `main` i DELL `main`;
- primijenjene migracije `0026` i `0027`;
- Django `check` bez sistemskih grešaka;
- `collectstatic`: 1 kopirana i 250 neizmijenjenih datoteka;
- korisnička ocjena da nakon restarta „izgleda da je sve ok“, bez sačuvanog HTTP komandnog izlaza.

Zbog nedostatka dokumentovanih HTTP provjera ovo nije dovoljno za tvrdnju da je kompletan produkcijski tok verificiran.

Izvori: [Status](../docs/STATUS_2026-10-14.md), [Deployment](../docs/DEPLOYMENT.md).

## Zaštita podataka i deployment ograničenja

Produkcijski deployment mora sačuvati lokalne izmjene `config/settings.py` i `.env`. Prije migracija potreban je svjež backup aktivne PostgreSQL/PostGIS baze, pregled plana migracija, tek zatim migracija, `collectstatic`, restart servisa i funkcionalna/HTTP provjera.

Poznato backup stanje:

- pokušaj punog `pg_dump` pod `wiki_user` nije valjan backup jer je prijavio `permission denied for schema tiger`;
- backup `backups/wiki-greblje-public-20261010-182840.dump` obuhvata samo shemu `public`;
- `pg_restore -l` je prikazao aplikacijske tabele;
- arhiva je prema terminalu imala 164 KB;
- restore nije testiran;
- backup nije cjelovita kopija svih shema.

Stari stash-evi i nepoznate lokalne datoteke ne smiju se brisati bez pregleda.

Izvor i obavezna kontrolna lista: [Deployment guide](../docs/DEPLOYMENT.md).

## Najvažniji naredni test

Potpuni produkcijski tok treba provjeriti ovim redoslijedom:

1. prijavljeni korisnik predlaže novo groblje i fotografiju;
2. potvrđuje se da nijedno nije javno prije odobrenja;
3. urednik odobrava groblje, ali fotografiju ostavlja na čekanju;
4. potvrđuje se nezavisnost statusa, zatim se odobrava fotografija i provjerava javni prikaz;
5. korisnik predlaže mezar u odobrenom groblju;
6. potvrđuje se da neodobreno groblje nije ponuđeno;
7. pregledaju se logovi i greške.

Uz to treba:

- potvrditi HTTP statuse relevantnih javnih stranica nakon restarta;
- testirati restore PostgreSQL/PostGIS backupa u izdvojenoj bazi;
- dodati regresijske testove za mezar bez osobe i s djelimičnim podacima;
- poboljšati i testirati OCR preciznost;
- provjeriti preostale WGDS komponente i sva stanja `WG-PERSON-001`.

Izvori: [Status](../docs/STATUS_2026-10-14.md), [TODO](../docs/TODO.md), [Ideas](../docs/IDEAS.md).

## Evidentirano stanje sadržaja

Snimak stranice Doprinosi, zabilježen u dokumentaciji 14.10.2026, prikazivao je:

- 203 odobrena doprinosa;
- 49 evidentiranih grobova;
- 23 evidentirane osobe;
- 69 fotografija;
- 4 korisnika među najaktivnijim doprinositeljima.

Ovi brojevi su snimak prikaza u jednom trenutku. Nisu trajna suma, audit baze niti garantovano trenutno stanje.

Izvori: [Status](../docs/STATUS_2026-10-14.md), [Changelog](../docs/CHANGELOG.md).

## Planirano, ali nije potvrđeno kao implementirano

- QR kodovi;
- napredna pretraga, čiji obim treba razjasniti u odnosu na postojeću pretragu;
- mobilna PWA aplikacija;
- porodična stabla;
- interaktivna vremenska linija i timeline groblja;
- historijski slojevi karte;
- 3D modeli stećaka;
- historijske fotografije;
- „Danas u historiji“;
- virtualne šetnje;
- glasovno pretraživanje;
- digitalne izložbe;
- buduća WG-PERSON proširenja: porodične veze, historijski izvori, galerija, vojna služba, zanimanje, nagrade i dokumenti.

Agent ove stavke ne smije opisati kao postojeće funkcije bez nove provjere.

Izvori: [Roadmap](../docs/ROADMAP.md), [Ideas](../docs/IDEAS.md), [WG-PERSON-001](../docs/WGDS/WG-PERSON-001.md).

## Pravila za budućeg agenta

- Ne izjednačavati roadmap s implementacijom.
- Ne izjednačavati implementaciju s produkcijskom verifikacijom.
- Ne proglašavati `WG-PERSON-001` završenim bez vizuelne i responsive provjere svih stanja.
- Ne tvrditi da je commit `be3a0ec` na DELL-u bez novijeg dokaza.
- Ne tretirati backup sheme `public` kao puni i restore-testirani backup baze.
- Ne prikazivati neodobren sadržaj u javnim prikazima.
- Ne prepisivati produkcijske `settings.py` i `.env` datoteke.
- Ne mijenjati vizuelni karakter projekta u dashboard ili društvenu mrežu.
- Nakon projektne izmjene ažurirati odgovarajuću dokumentaciju i kreirati obavezni izvještaj prema [`AGENTS.md`](../AGENTS.md).

## Tematski kontekst iz projektnog razgovora

Javna podijeljena konverzacija „MapTiler admin nastavak“ sačuvala je operativne detalje koji nisu svi ušli u sažete dokumente pod `docs/`. Ti detalji su razdvojeni po temama u [`AgentsDocs/Topics/`](Topics/README.md):

- [MapTiler i koordinate](Topics/MAPTILER_AND_COORDINATES.md)
- [Udaljeni pristup i server](Topics/REMOTE_ACCESS_AND_SERVER.md)
- [Deployment i okruženje](Topics/DEPLOYMENT_AND_ENVIRONMENT.md)
- [Uloge, dozvole i klasifikacija](Topics/ROLES_PERMISSIONS_AND_CLASSIFICATION.md)
- [Prijedlozi i moderacija grobalja](Topics/CEMETERY_PROPOSALS_AND_MODERATION.md)
- [Fotografije i galerija](Topics/PHOTOS_AND_GALLERY.md)
- [Unos mezara, osobe i OCR](Topics/GRAVE_ENTRY_PERSON_AND_OCR.md)

Ovi dokumenti su historijski/operativni dodatak. Za trenutno stanje prednost imaju noviji statusni dokument, kod, migracije i provjera aktivnog okruženja.

## Mapa autoritativnih izvora

| Potreba | Prvi dokument za čitanje |
| --- | --- |
| Misija i vrijednosti | [Manifest](../docs/MANIFEST.md) |
| Najnoviji konsolidovani status | [Status 2026-10-14](../docs/STATUS_2026-10-14.md) |
| Završeno, provjere i backlog | [TODO](../docs/TODO.md) |
| Planirane verzije i status ciljeva | [Roadmap](../docs/ROADMAP.md) |
| Historija sprintova | [Sprints](../docs/SPRINTS.md) |
| Evidencija promjena | [Changelog](../docs/CHANGELOG.md) |
| Prihvaćene odluke i razlozi | [Decisions](../docs/DECISIONS.md) |
| Siguran deployment | [Deployment](../docs/DEPLOYMENT.md) |
| Vizuelna filozofija | [UI guidelines](../docs/UI_GUIDELINES.md) |
| Komponente i CSS organizacija | [Design System](../docs/DESIGN_SYSTEM.md) |
| Heritage i moderacijski principi | [Design principles](../docs/DESIGN-PRINCIPLES.md) |
| Heritage Person Panel | [WG-PERSON-001](../docs/WGDS/WG-PERSON-001.md) |
| Otvorene ideje | [Ideas](../docs/IDEAS.md) |
| Operativni detalji iz razgovora | [Conversation topic index](Topics/README.md) |
| Kontekst ranijih agent zadataka | [Change reports](Changes/) |

## Historija ovog sažetka

Dokument je prvi put generisan 21.10.2026. na osnovu kompletne dokumentacije koja je tada postojala u `docs/`. Kada se promijene ciljevi, potvrđeni status ili operativno okruženje, ovaj dokument treba ažurirati zajedno s izvornim dokumentima, a ne umjesto njih.

Povezani izvještaji:

- [00002 - Pregled ciljeva i realizacije projekta](Changes/main/00002_review_project_documentation.md)
- [00003 - Kreiranje AI agent projektnog konteksta](Changes/main/00003_create_ai_agent_project_context.md)
- [00004 - Tematska dopuna iz podijeljenog razgovora](Changes/main/00004_import_shared_conversation_topics.md)
