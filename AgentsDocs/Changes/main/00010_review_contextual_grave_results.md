# 00010 - Procjena kontekstualnih rezultata grobova

- Vrijeme izvršenja prompta: `2026-10-22T14:52:20+02:00` (`Europe/Sarajevo`)
- Git grana: `main`

## Originalni prompt

```text
super. Kralj si. Provjerio sam 1919, Nezir 1919, Hadzimejlic 1919, Hadžimejlić 1919 sve radi i to kako treba. Ono što sam dodatno primjetio je da se pri pretrazi Numanagić pojavljuju i grobovi koji se nalaze  u blizini turbeta šejh ef. Numanagić, odnosno groba. Da li bi to trebali ostaviti tako ili ih isključiti iz pretrage, šta ti misliš?
```

## Opis zadatka

Provjeriti zašto pretraga `Numanagić` vraća grobove opisane kao obližnje turbeta šejh ef. Numanagića te preporučiti treba li takve rezultate zadržati ili programski isključiti. Evidentirati i korisnikovu ručnu potvrdu prethodno uvedene pretrage godina.

## Izvršene provjere

- Lokalni javni zahtjev za `Numanagić` vratio je šest grobova.
- Provjereno je koje polje uzrokuje svako podudaranje: direktni zapisi podudaraju naslov i/ili natpis, dok grobovi ID 4 i ID 5 odgovaraju isključivo preko polja `inscription`.
- Grob ID 4 u `inscription` sadrži opis da se lokacija nalazi uz turbe šejh ef. Numanagića.
- Grob ID 5 u `inscription` sadrži opis da se nalazi u blizini turbeta, dok je tekst koji izgleda kao stvarni natpis zabilježen u `notes`.
- Geografska udaljenost se ne koristi u metodi `search()` i nije uzrok ovih rezultata.
- Sve provjere baze bile su samo za čitanje; kod i podaci nisu mijenjani.

## Zaključak i preporuka

- Ne uvoditi programsko isključivanje svih grobova koji se podudaraju samo preko natpisa. Stvarni epitaf može legitimno spominjati drugu osobu ili porodicu i predstavlja vrijedan arhivski rezultat.
- Dva uočena rezultata su prvenstveno problem klasifikacije sadržaja: opis položaja je spremljen u polje namijenjeno natpisu.
- Kratkoročno treba urednički premjestiti lokacijske opise iz `inscription` u odgovarajuće bilješke ili buduće strukturirano polje za prostorni kontekst, a stvarni tekst natpisa evidentirati u `inscription` gdje je poznat.
- Srednjoročno treba uvesti rangiranje: direktno podudaranje osobe ili naslova ispred podudaranja pronađenog samo unutar dužeg natpisa. Po potrebi se sekundarni rezultati mogu označiti kao „spominje traženi izraz“, umjesto da budu potpuno skriveni.
- Ne preporučuje se filtriranje po frazama poput „u blizini“ ili „uz turbe“ jer bi bilo krhko, zavisilo od formulacije i moglo ukloniti legitimne rezultate.

## Razlozi za odluku

- Pretraga natpisa je osnovna arhivska funkcija Wiki Greblja i ne treba je oslabiti zbog nekoliko pogrešno klasifikovanih zapisa.
- Ispravka izvornog podatka uklanja konkretan neželjeni rezultat bez skrivenih pravila i bez gubitka historijskih veza.
- Rangiranje zadržava kontekstualnu vrijednost spominjanja, ali korisniku prvo prikazuje ono što je vjerovatno namjeravao pronaći.

## Promjene napravljene za prompt

- Aplikacijski kod, baza i podaci nisu mijenjani.
- Izvještaj `00009` dopunjen je korisnikovom ručnom potvrdom pretrage godina i vezom na ovaj nalaz.

## Povezani izvještaji

- [00007 - Normalizacija dijakritike u pretrazi](./00007_normalize_search_diacritics.md)
- [00008 - Ispravka tipa normalizacijskog izraza](./00008_fix_search_expression_output_field.md)
- [00009 - Pretraga numeričkih godina](./00009_search_numeric_years.md)
- [00011 - Rangiranje rezultata pretrage](./00011_rank_search_results.md)
