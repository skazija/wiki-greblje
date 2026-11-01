# 00046 - Read-only provjera USB transfer paketa

- Vrijeme: 2026-10-31 15:16:19 CET, Europe/Sarajevo (UTC+01:00).
- Hostname: MININT-B5ME0EV; radna putanja: C:\Users\Administrator\Documents\Codex\2026-10-31\nalazim-se-na-novom-laptopu-i.
- Grana prema prethodnoj provjeri: main. Indeks 00046 slijedi najveci lokalno prisutni 00045.

## Originalni prompt

```text
Radiš na laptopu MININT-B5ME0EV. Pročitaj AGENTS.md.

Za sada izvrši samo provjeru paketa u D:\backup, bez raspakivanja, uvoza baze, pokretanja ili zaustavljanja PostgreSQL-a i bez izmjene postojećih podataka.

Provjeri da postoje:

1. wiki_groblje_appdata_utf8.json
   Očekivani SHA-256:
   BD2E9D073C7E563BDDA8F9E29CD17ADE818958BFC2843DB5278DBCF372D36BBA

2. wiki_groblje_media.zip
   Očekivani SHA-256:
   642EF3156E4D64A1964D3D8567F405BF8437543FA43FC6176E3BEA4E752F641A

3. TRANSFER_README.md

Sigurno parsiraj JSON bez prikazivanja korisničkih podataka i potvrdi da sadrži 478 objekata. Provjeri sadržaj ZIP arhive bez raspakivanja i potvrdi da sadrži 211 datoteka pod media/ putanjom.

Datoteke wiki_groblje_pg18.dump i wiki_groblje_appdata.json su nepotpune i ne smiju se koristiti.

Prikaži samo rezultate provjere, veličine, kontrolne zbirove i eventualne greške. Osim obaveznog AGENTS.md izvještaja, ništa ne mijenjaj. Zatim stani i čekaj sljedeću naredbu.
```

## Zadatak i rezultati

Procitan AGENTS.md i potvrđen hostname/radna putanja. Datoteke iz D:\backup otvorene su iskljucivo za citanje. SHA-256 izracunat streaming citanjem; JSON parsiran standardnim json parserom uz odbijanje nestandardnih konstanti, bez izvrsavanja sadrzaja ili ispisa korisnickih podataka. ZIP pregledan preko centralnog direktorija bez raspakivanja i bez ispisa naziva medijskih datoteka.

| Datoteka | Velicina (bajtova) | SHA-256 | Rezultat |
|---|---:|---|---|
| wiki_groblje_appdata_utf8.json | 213228 | BD2E9D073C7E563BDDA8F9E29CD17ADE818958BFC2843DB5278DBCF372D36BBA | Poklapa se |
| wiki_groblje_media.zip | 532509518 | 642EF3156E4D64A1964D3D8567F405BF8437543FA43FC6176E3BEA4E752F641A | Poklapa se |
| TRANSFER_README.md | 2032 | 18CE59B24556B1152315BB26C77542DFF6569BB67898D70122BD62BEA8E5BC4E | Postoji; referentni hash nije zadan |

- JSON je validan; korijen je niz sa tacno 478 elemenata, svi elementi su objekti.
- ZIP sadrzi tacno 211 datoteka, svih 211 pod media/; nema datoteka izvan media/, duplih naziva ili detektovanih nesigurnih putanja/simbolickih linkova.
- Nije radjen poseban CRC test dekompresijom; SHA-256 cijele arhive odgovara dostavljenoj referenci.
- Nema prijavljenih gresaka.
- wiki_groblje_pg18.dump i wiki_groblje_appdata.json nisu otvarani niti koristeni.

## Promjene i razlozi odluka

Jedina izmjena je ovaj obavezni izvjestaj. Nista nije raspakovano, kopirano ili uvezeno. Nije pristupano bazi, pokretan/zaustavljan PostgreSQL, mijenjan kod, konfiguracija, ACL ili postojeci podaci. Nema commita, pusha, brisanja ili pristupanja produkciji. Hash provjera i pregled metapodataka dovoljni su za trazeni opseg bez ekstrakcije arhive ili otkrivanja licnih podataka.

## Povezani izvjestaji

- [Read-only dijagnostika laptopa](00101_readonly_laptop_diagnostics.md)
- [Prethodna priprema kontrolisanog testa](00103_revise_manual_start_cleanup.md)
- Nema naknadnih izvjestaja u trenutku pisanja.
