# Plan postavljanja razvojnog okruženja na laptopu

## Vrijeme izvršenja

2026-10-31 11:40:56 +01:00 (Europe/Sarajevo)

## Originalni prompt

> izvini moram pitati, opve provjere što vršiš da li vršiš na ovom računaru ili na laptopu? Na laptopu nisam uspostavio ništa osim instalacija programa koji su nam neophodni. Ako je na ovom računaru, možemo ako hoćeš i na njemu prvo instalirati GUI a zatim na laptopu da mi pojasniš korak po korak kako da to odradimo. Kako da povućemo sa GIT_a i napravimo okruženje koje mogu koristiti kada sam na putu ili odmoru

## Opis zadatka

Razjasniti na kojem uređaju su prethodne provjere izvršene i pripremiti siguran postupak za kloniranje projekta sa GitHuba te izradu zasebnog lokalnog razvojnog okruženja na laptopu.

## Promjene napravljene za prompt

- Utvrđeno je da trenutna Codex sesija radi na uređaju `DESKTOP-T8ME4IM` u direktoriju `C:\wiki-groblje`.
- Ispravljen je izvještaj `00025` kako više ne bi tvrdio da je provjeren laptop.
- Definisan je fazni pristup za laptop: prvo Git i kloniranje, zatim otvaranje lokalnog projekta u Codexu, pa virtualno Python okruženje, lokalni `.env`, PostgreSQL/PostGIS baze, migracije i testovi.
- Nisu pokretani Git clone/pull, instalacije, produkcijske veze ni izmjene aplikacijskog koda.

## Razlozi za implementacijske odluke

- Codex može provjeravati samo datoteke i alate na računaru kojem je konkretna sesija dala pristup; sama tvrdnja da je korisnik na laptopu nije dovoljna da potvrdi fizički uređaj.
- Laptop treba imati vlastitu Git kopiju, virtualno Python okruženje, lokalne tajne i lokalnu bazu. Git prenosi izvorni kod i dokumentaciju, ali ne treba prenositi `.env`, aktivnu bazu, media datoteke ni sigurnosne kopije.
- Postavljanje se dijeli na kratke provjerljive faze kako bi se greška mogla zaustaviti prije rada s bazom ili produkcijom.
- Produkcijski VPN i SSH nisu dio početnog lokalnog postavljanja i ne trebaju se uključivati dok lokalne provjere ne prođu.

## Povezani izvještaji

- [Provjera trenutnog računara za razvoj](00025_verify_laptop_setup.md)
- [Provjera PostGIS testne baze](00020_verify_postgis_test_database.md)
- [Kontrolisani deployment pretrage na DELL](00024_deploy_search_to_dell.md)
