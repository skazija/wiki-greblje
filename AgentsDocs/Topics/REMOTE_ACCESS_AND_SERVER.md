# Udaljeni pristup i server

## Namjena

Ovaj dokument čuva operativno znanje iz razgovora o pristupu Wiki Greblje infrastrukturi. Ne predstavlja mrežnu politiku organizacije niti potvrdu da su adrese i servisi i dalje isti.

Izvor razgovora: [MapTiler admin nastavak](https://chatgpt.com/share/6ad8c598-22d0-83ed-b6f6-c8ec82bc4561).

## Dokumentovana topologija

- UniFi/UDM obezbjeđuje WireGuard VPN ulaz u poslovnu mrežu.
- Fizički server koristi Windows Server 2024 i u razgovoru je imao LAN interfejse `192.168.1.3` i `192.168.1.4`.
- Wiki Greblje produkcija radi u Ubuntu 24.04 VM-u, historijski na `192.168.1.125`.
- SSH korisnik za VM je `wikiadmin`; potvrđeno je članstvo u `sudo` grupi i `sudo -l` pristup.
- Django repozitorij je u `/opt/wiki-greblje`.
- Produkcijski proces je `wiki-greblje.service`, koji pokreće Gunicorn na `127.0.0.1:8000`.

Ovo su privatne/historijske mrežne adrese. Prije upotrebe provjeriti trenutno stanje i ne objavljivati vjerodajnice.

## Preporučeni način udaljenog rada

Dokumentovana arhitektura je:

```text
udaljeni računar
  -> WireGuard prema UDM-u
  -> poslovni LAN
  -> SSH prema Ubuntu Wiki Greblje VM-u
```

RDP je razmatran za GUI pristup Windows serveru, a SSH za svakodnevne Git/Django operacije. Portove 22 i 3389 ne treba direktno izlagati internetu kada postoji VPN.

## Preklapanje mrežnih opsega

U razgovoru su i kućna i poslovna mreža koristile `192.168.1.0/24`, dok je WireGuard klijent imao adresu `192.168.11.2/32`. To stvara preklapanje: računar ne može jednostavno znati da li je `192.168.1.x` lokalni uređaj ili udaljeni uređaj iza VPN-a.

`AllowedIPs = 0.0.0.0/0` predstavlja full tunnel i može preuzeti sav IPv4 promet, uključujući pristup lokalno mapiranim diskovima. WireGuard nema jednostavnu sintaksu „sve osim ovog subnet-a“. Dugoročno je čišće koristiti različite LAN opsege ili precizno projektovan routing/NAT; ad hoc rute treba mijenjati samo uz razumijevanje mrežnog uticaja.

## Šta je potvrđeno dijagnostikom

- WireGuard handshake je radio.
- Kroz VPN su bili vidljivi uređaji poslovne mreže i naziv `wikigreblje.local.domain`.
- Ping do Wiki Greblje servera prolazio je oko 18 ms.
- TCP problem se ponavljao i na fizičkom LAN-u, pa UDM/WireGuard nije bio glavni uzrok.
- OpenSSH na fizičkom Windows serveru prihvatio je drugog korisnika; problem s jednim nalogom bio je account/autentikacija, ne mreža.
- `ssh -vvv` je potvrdio uspješnu password autentikaciju za Windows nalog i kasnije za `wikiadmin` na VM-u.
- Direktna prijava `ssh wikiadmin@192.168.1.125` uspješno je otvorila Ubuntu shell.

## Windows OpenSSH napomena

Ugrađena Windows OpenSSH instalacija ranije nije pravilno kreirala/premještala host ključeve, nakon čega je korišten MSI instalater. U takvom stanju moguće su dvije instalacije, različiti `sshd_config` fajlovi ili servis koji koristi neočekivanu putanju.

Ako se problem ponovi, provjeriti:

- koji `sshd` servis radi;
- na kojem portu/adresi sluša;
- putanju `sshd_config` i host ključeva;
- Windows Firewall pravila;
- korisničke grupe i pravo prijave;
- Event Viewer/OpenSSH logove.

## Sigurna operativna pravila

- `ssh -vvv` koristiti samo za dijagnostiku uspostavljanja veze; nakon prijave otvoriti novu sesiju bez verbose izlaza.
- Prije Git operacija potvrditi `pwd`, lokaciju repozitorija i `git status`.
- Ne raditi `git pull` dok se ne pregledaju lokalne produkcijske izmjene.
- Ne slati password, API ključ ni sadržaj `.env` u chat ili dokumentaciju.
- Ne mijenjati UDM/WireGuard kada ping i VPN vidljivost rade, a isti TCP kvar postoji i na LAN-u; tada prvo pregledati ciljnu mašinu.
- Mrežne adrese iz ovog dokumenta tretirati kao historijske, ne garantovane.

Povezano: [Deployment i okruženje](DEPLOYMENT_AND_ENVIRONMENT.md), [`docs/DEPLOYMENT.md`](../../docs/DEPLOYMENT.md).
