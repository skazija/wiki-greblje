# TODO — Wiki Greblje

Ažurirano: 23.10.2026.

## Završeno (potvrđeno)
- [x] Sprint 1: responsive početna i osnovni vizuelni sistem.
- [x] Sprint 2: Grave Detail v2.
- [x] Osnovni jedinstveni obrazac za digitalizaciju groba (lokacija, fotografije, osobe, natpis).
- [x] Višestruki upload fotografija i izbor glavne fotografije.
- [x] Moderacija fotografija i filtriranje javnih prikaza.
- [x] Klasifikacija spomenika i stanja očuvanosti (`0018–0025`).
- [x] Korisnički prijedlog groblja, status/autor, odvojena moderacija fotografija (`0026–0027`).
- [x] Commit `2f94d59` na GitHubu i kod/migracije na DELL-u.
- [x] Napredna javna pretraga: tokeni, godine, normalizacija dijakritike, rangiranje, rezultati groblja i kombinovani filteri.
- [x] Odvojena lokalna PostgreSQL/PostGIS testna baza i 31 prolazni regresijski test.

## Provjeriti sljedeće
- [ ] Produkcijski test cijelog toka: prijedlog groblja → fotografija → odobravanje → prijedlog mezara.
- [ ] Potvrditi HTTP status i funkcionalnost svih relevantnih javnih stranica nakon restarta.
- [ ] Pregledati admin akcije koje mijenjaju status putem GET zahtjeva.
- [ ] Provjeriti politiku pristupa direktnim URL-ovima fotografija na čekanju.
- [ ] Testirati povrat PostgreSQL/PostGIS backupa u izdvojenu bazu.
- [ ] Nastaviti rad na OCR preciznosti i pregledati WGDS komponente koje su još u razvoju.

## Backlog (nije potvrđeno kao implementirano)
- [ ] QR kodovi.
- [ ] Približna podudaranja i OCR greške pomoću `pg_trgm`, nakon mjerenja stvarnih upita.
- [ ] Full-text pretraga za duže natpise, nakon mjerenja stvarnih upita.
- [ ] Ograničiti maksimalnu i razmotriti minimalnu dužinu tekstualnog upita.
- [ ] PWA.
- [ ] AI pomoć pri čitanju natpisa (poboljšanje postojećeg OCR toka).
- [ ] Porodična stabla, historijski slojevi karte, timeline groblja.

## Promjene spremne za naredni grupni deploy
- [x] Ispravka praznih osoba lokalno testirana i poslana na GitHub (`be3a0ec`).
- [x] Napredna pretraga i testna infrastruktura lokalno provjerene sa 31 testom.
- [ ] Commitovati i poslati paket napredne pretrage na GitHub.
- [ ] Prenijeti `be3a0ec` i paket napredne pretrage na DELL u jednom kontrolisanom deployu (backup, zaštita `config/settings.py`, provjere).
- [ ] Naknadno dodati regresijski test za unos mezara bez osobe i s djelimičnim podacima.
