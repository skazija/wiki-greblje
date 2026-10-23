# 00004 - Tematska dopuna iz podijeljenog razgovora

- Vrijeme izvršenja prompta: `2026-10-21T16:11:03+02:00` (`Europe/Sarajevo`)
- Git grana: `main`
- Vanjski izvor: [ChatGPT razgovor „MapTiler admin nastavak“](https://chatgpt.com/share/6ad8c598-22d0-83ed-b6f6-c8ec82bc4561)

## Originalni prompt

```text
https://chatgpt.com/share/6ad8c598-22d0-83ed-b6f6-c8ec82bc4561 na ovom linku se nalazi konverzacija razgovora u vezi ovog projekta. Nadopuni AgentsDocs dokumentaciju na osnovu ovog razgovora. Rastavi različite tematike na različite fajlove.
```

## Opis zadatka

Pregledati cijeli javno podijeljeni razgovor o projektu Wiki Greblje, izdvojiti potvrđene rezultate, odluke, incidente i operativne lekcije koje nisu potpuno zastupljene u postojećoj dokumentaciji te ih podijeliti u zasebne tematske dokumente pod `AgentsDocs/`. Nove dokumente povezati s centralnim agent indeksom i postojećim projektnim kontekstom.

## Pregled izvora

- ChatGPT web prikaz je pri prvom pokušaju završio timeoutom.
- Direktni javni HTTP odgovor bio je dostupan i sadržavao je naslov „MapTiler admin nastavak“ i ugrađeni linearni zapis razgovora.
- Obrađeno je 919 tekstualnih stavki: 169 korisničkih, 295 asistentskih i 455 alatnih poruka.
- Razgovor je sadržavao opise priloženih slika, ZIP-ova i terminalskih rezultata; same historijske priloge ovaj zadatak nije kopirao u repozitorij.
- Iz sinteze su izostavljeni prolazni pogrešni prijedlozi kada je kasniji dio razgovora utvrdio drugačiji uzrok ili konačno rješenje.

## Promjene napravljene za prompt

### Novi tematski dokumenti

- Kreiran je [tematski indeks](../../Topics/README.md) sa izvorom, granicama pouzdanosti i redoslijedom autoriteta.
- Kreiran je [MapTiler i koordinate](../../Topics/MAPTILER_AND_COORDINATES.md): standard implementacije, `unlocalize`, `crossOrigin`, static source putanje, incidenti i commitovi `81eee43`, `7eed1b8`, `8e60660`.
- Kreiran je [Udaljeni pristup i server](../../Topics/REMOTE_ACCESS_AND_SERVER.md): WireGuard, preklapanje subnet-a, Windows/Ubuntu uloge, SSH provjere i operativna pravila.
- Kreiran je [Deployment i okruženje](../../Topics/DEPLOYMENT_AND_ENVIRONMENT.md): produkcijske etape, `.env` incident, DB korisnik `wiki_user`, backup ograničenja, migracije i status `be3a0ec`.
- Kreiran je [Uloge, dozvole i klasifikacija](../../Topics/ROLES_PERMISSIONS_AND_CLASSIFICATION.md): autocomplete 403, kombinabilne grupe, podjela osnovnih i stručnih polja, admin/frontend testovi i commit `2112f2a`.
- Kreiran je [Prijedlozi i moderacija grobalja](../../Topics/CEMETERY_PROPOSALS_AND_MODERATION.md): migracije `0026`/`0027`, obrazac, javna zaštita, odvojeno odobravanje i commit `2f94d59`.
- Kreiran je [Fotografije i galerija](../../Topics/PHOTOS_AND_GALLERY.md): `CemeteryPhoto` dozvole/statusi, javno filtriranje, galerijski incident i otvoreno pitanje media URL-ova.
- Kreiran je [Unos mezara, osobe i OCR](../../Topics/GRAVE_ENTRY_PERSON_AND_OCR.md): pravilo mezara bez osobe, regresija, ručna provjera, commit `be3a0ec` i OCR status.

### Povezivanje dokumentacije

- `AGENTS.md` je proširen direktnim linkovima na tematski indeks i svih sedam dokumenata.
- `AgentsDocs/AI_AGENT_PROJECT_CONTEXT.md` je dopunjen sekcijom s tematskim dokumentima, novim unosom u mapi izvora i linkom na ovaj izvještaj.
- Svaki tematski dokument povezuje relevantne postojeće `docs` dokumente i druge tematske fajlove.
- Aplikacijski kod, konfiguracija, baza i produkcija nisu mijenjani.

## Razlozi za implementacijske odluke

- Različite teme su odvojene jer razgovor obuhvata razvoj aplikacije, mrežu, produkciju, dozvole, moderaciju i regresije; jedan veliki dokument bi otežao pronalazak operativnog konteksta.
- Kreiran je poseban indeks kako bi budući agent mogao vidjeti obim izvora, granice dokaza i izabrati samo relevantnu temu.
- Razgovor je tretiran kao historijski sekundarni izvor. Noviji kod, migracije i dokumenti iz `docs` imaju prednost kada postoji razlika.
- Tajne nisu kopirane. Dokumentovani su nazivi environment varijabli i obrasci provjere, ali ne API ključevi ili passwordi.
- Privatne LAN adrese su zadržane samo kao jasno označen historijski operativni kontekst; nisu predstavljene kao trajna konfiguracija.
- Commit hashovi i rezultati provjera sačuvani su jer omogućavaju agentu da poveže funkcionalne cjeline s Git/deploy historijom.
- Poznati pogrešni međuzaključci nisu dokumentovani kao činjenice; zadržane su samo lekcije kada objašnjavaju važnu dijagnostičku zamku.

## Povezani izvještaji

- [00001 - Create AGENTS.md and Project Documentation Index](./00001_create_agents_md.md)
- [00002 - Pregled ciljeva i realizacije projekta](./00002_review_project_documentation.md)
- [00003 - Kreiranje AI agent projektnog konteksta](./00003_create_ai_agent_project_context.md)
- Naknadni izvještaji: nema ih u trenutku nastanka ovog dokumenta.
