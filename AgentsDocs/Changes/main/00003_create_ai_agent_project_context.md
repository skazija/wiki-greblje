# 00003 - Kreiranje AI agent projektnog konteksta

- Vrijeme izvršenja prompta: `2026-10-21T15:58:52+02:00` (`Europe/Sarajevo`)
- Git grana: `main`

## Originalni prompt

```text
izgeneriši dokumentaciju za AI agenta u AgentsDocs folderu koja će saržati ciljeve svega urađenog u projektu na osnovu dokumentacije u docs folderu. Uveži sa AGENTS.md fajlom. Napomena: Uveži dokumentaciju koju ćeš izgenerisati u AgentsDocs.
```

## Opis zadatka

Kreirati trajni dokument u `AgentsDocs/` koji budućem AI agentu objašnjava svrhu projekta, ciljeve svih dokumentovanih realizovanih cjelina, stepen njihove potvrđenosti, trenutno tehničko i produkcijsko stanje, otvorene provjere i ograničenja. Novi dokument direktno povezati s korijenskim `AGENTS.md` indeksom.

## Promjene napravljene za ovaj prompt

- Kreiran je [`AgentsDocs/AI_AGENT_PROJECT_CONTEXT.md`](../../AI_AGENT_PROJECT_CONTEXT.md).
- Za svaku glavnu projektnu cjelinu povezani su cilj, ostvareni rezultat, status i relevantni izvorni dokumenti.
- Dodane su sekcije o misiji, razvojnom procesu, dizajnerskim pravilima, tehničkom okruženju, sigurnom deploymentu, backup ograničenjima, prioritetnim testovima i neimplementiranom backlogu.
- Dodana je mapa autoritativnih izvora kako bi budući agent brzo pronašao detaljnu dokumentaciju za svoj zadatak.
- U [`AGENTS.md`](../../../AGENTS.md) dodana je sekcija `AI Agent Context` s direktnim linkom na novi dokument.
- Kreiran je ovaj obavezni change report s narednim indeksom `00003`.
- Aplikacijski kod, baza, konfiguracija i produkcija nisu mijenjani.

## Razlozi za implementacijske odluke

- Stabilni agent kontekst smješten je direktno u `AgentsDocs/`, odvojeno od hronoloških izvještaja, jer treba služiti kao dugoročna početna tačka, a ne kao zapis samo jednog zadatka.
- Dokument razlikuje potvrđeno, implementirano ali neprovjereno, djelimično i planirano kako budući agent ne bi roadmap ili commit pogrešno predstavio kao produkcijski potvrđenu funkciju.
- Uz svako područje dodani su relativni linkovi na izvorne dokumente, čime sinteza ostaje provjerljiva i povezana s autoritativnim detaljima.
- `AGENTS.md` dobio je poseban link umjesto oslanjanja samo na link direktorija change reporta, jer je novi dokument namijenjen obaveznom uvodnom čitanju.
- Novi dokument povezuje i relevantne change reporte, pa veza postoji u oba smjera: iz centralnog indeksa prema agent kontekstu i iz konteksta prema historiji rada.
- Aktivna grana je potvrđena čitanjem `.git/HEAD` jer `git` izvršna datoteka nije dostupna na `PATH` u ovoj sesiji.

## Povezani izvještaji

- [00001 - Create AGENTS.md and Project Documentation Index](./00001_create_agents_md.md)
- [00002 - Pregled ciljeva i realizacije projekta](./00002_review_project_documentation.md)
- Naknadni izvještaji: nema ih u trenutku nastanka ovog dokumenta.
