# Version 1.0

## Added

- Novo sučelje za digitalizaciju grobova
- Galerija fotografija
- Povezane osobe
- Komentari
- Historija izmjena

## Changed

- Potpuno redizajniran Grave Detail
- Novi sistem Content Cards

## Fixed

- Responsive prikaz
- Optimizacija mapa

## Dopune historije — juli–oktobar 2026.

> Evidencija zasnovana na sačuvanim projektnim bilješkama i potvrđenim radnim sesijama. Nije potpuna Git historija; datumi ispod označavaju potvrđene etape, ne nužno datum svakog commita.

### Juli 2026. — interfejs i digitalizacija
- Završeni Sprint 1 (responsive početna, navigacija, hero, kartice, footer) i Sprint 2 (Grave Detail v2: galerija, osobe, natpis, lokacija, povezani sadržaj, komentari i historija izmjena).
- Uspostavljen WG Design System i modularna organizacija CSS-a; počet rad na jedinstvenom obrascu za digitalizaciju groba.

### August–septembar 2026. — unos i klasifikacija
- Obrazac za digitalizaciju groba proširen fotografijama, izborom glavne fotografije, OCR pomoćnim tokom i podacima o osobama/lokaciji.
- Uvedena moderacija fotografija (`pending` / `approved` / `rejected`), uz filtriranje javnih prikaza na odobrene zapise.
- Dodana klasifikacija spomenika i stanja očuvanosti; migracije `0018–0025`, uključujući podatke standarda i polja za stanje, degradaciju i položaj spomenika.
- Uveden MapTiler za prikaz karata; zamijenjeni preostali OSM tile slojevi.

### Oktobar 2026. — prijedlozi grobalja i produkcija
- Commit `2f94d59` (*Add cemetery proposal and moderation workflow*): prijedlog groblja za prijavljene korisnike, statusi groblja, autor prijedloga, zasebno odobravanje fotografija i uredničke admin akcije.
- Javne liste i detalji prikazuju samo odobrena groblja; obrazac za dodavanje groba ograničen je na odobrena groblja.
- Migracije `0026` (status/autor groblja) i `0027` (dozvole uredničke grupe) primijenjene na DELL-u; `collectstatic` prijavio 1 kopiranu i 250 neizmijenjenih datoteka.
- GitHub i DELL usklađeni na `2f94d59`; produkcijske HTTPS postavke sačuvane. Završni korisnički end-to-end test predlaganja groblja i mezara na produkciji ostaje za potvrdu.

### Evidencija doprinosa — snimak ekrana, 14.10.2026.
- 203 odobrena doprinosa, 49 evidentiranih grobova, 23 evidentirane osobe, 69 fotografija i 4 korisnika prikazana u odjeljku najaktivnijih doprinositelja.
- Brojevi su stanje prikazano na dostavljenoj slici, ne trajni zbir ni revizija baze.

### 14. oktobar 2026. — ispravka kreiranja prazne osobe
- Ispravljeno automatsko kreiranje `Person` bez ikakvih podataka pri prijavi mezara.
- Ako postoje djelimični podaci (npr. samo godina smrti), osoba se i dalje kreira kao nepoznata i čeka odobrenje.
- Lokalno provjereno kroz stvarni unos i admin; commit `be3a0ec` na GitHubu. Produkcijski DELL deploy odgođen.

### 22–23. oktobar 2026. — napredna javna pretraga
- Višerječni upiti zahtijevaju podudaranje svakog tokena, uz podršku za puno ime, oba redoslijeda imena i numeričke godine.
- Bosanski dijakritički znakovi normalizuju se za pretragu, uključujući `č/ć/c`, `š/s`, `ž/z` i `đ/dj`.
- Dodani su zasebni, rangirani rezultati groblja, osoba i grobova te odvojeni markeri na mapi.
- Dodani su filteri za groblje, grad ili selo, raspone rođenja i smrti te osnovnu stručnu klasifikaciju.
- U odvojenoj lokalnoj PostgreSQL/PostGIS bazi prolazi svih 31 regresijski test; razvojna baza ostaje nepromijenjena.
- Migracija `0027` osposobljena je za potpuno praznu bazu tako što sigurno kreira potrebni tip sadržaja i uredničke dozvole.
