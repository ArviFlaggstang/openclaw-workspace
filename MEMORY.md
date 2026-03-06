# MEMORY.md — Langtidsminne

_Updated: 2026-03-06_

## Trym — Hvem du er
- **Navn:** Trym Johnsen
- **Prosjekt:** Selge AI-assistenter til bedrifter/enkeltpersoner
- **Lokasjon:** Norge (CET/CEST)
- **Teknisk nivå:** Kyndig, jobber i terminalen
- **Server:** Hetzner, 4GB RAM, Ubuntu 24.04

## Prosjekt: AI-Assistent-Salg

### Status
- [ ] Definert målgruppe
- [ ] Prissetting på plass
- [ ] Første kunde
- [ ] Nettside/landing page

### Hva vi har prøvd
| Dato | Ting | Resultat | Lærdom |
|------|------|----------|--------|
| 2026-03-05 | Leads i Trondheim/Alta | Måtte gjøres manuelt | Trenger web search for effektiv research |
| 2026-03-05 | BraveSearch-oppsett | Fikk det til etter restart + config | API key alene er ikke nok, må whiteliste tool |

### Hva som funker
- Å restarte gateway etter config-endringer
- Å spørre meg om verktøylisten for å sjekke at ting er på plass

### Hva som ikke funker
- Å anta at API key = tool er tilgjengelig
- Å bruke meg til live business research uten web search

### Neste steg
1. [ ] Ferdigstill BraveSearch-oppsett
2. [ ] Bygg leads-liste for Trondheim
3. [ ] Lag mal for AI-assistent-forslag per bransje

## Konfigurasjon som funker

### OpenClaw
```bash
# Etter endringer i config:
openclaw gateway restart

# Sjekk tools:
openclaw tools list
```

### Minne-filer
- Daglige logger: `memory/YYYY-MM-DD.md` (auto)
- Kuratert minne: `MEMORY.md` (denne filen)
- Verktøy-notater: `TOOLS.md`

## Tryms preferanser og forutsetninger

### Salgskomfort
- **Telefonsalg:** Ikke superkomfortabel, MEN kan gjøre det med god forberedelse og tro på produktet
- **Viktig:** Må ha full tro på det jeg sier — da er jeg villig til å ringe

### Produktkrav
- **Kvalitet:** Fullstendig trygt for kunden — ingen halvveis løsninger
- **Leveranse:** Klart produkt og måte å levere på
- **Pris:** Gjerne billig i starten, men ikke FOR billig (verdsetting)
- **Tidsramme:** Ikke hast — vil gjøre det ordentlig
- **Læring:** Villig til å lære tekniske ting hvis det er verdt det

### Tryms unike salgsargumenter (USPs)
- **Lokal i Trondheim** — kjenner byen, kan møtes fysisk
- **Altaværing** — lokal tilknytning til Finnmark også
- **Billig** — student, lavere overhead enn byråer
- **Datateknologi student** — spesialiserer i AI og programvareutvikling
- **Personlig service** — ikke et stort byrå, faktisk bryr seg

## Forretningsstrategi (vedtatt 2026-03-06)

### Målgruppe
**Primær:** Håndverkere (VVS, elektrikere, rørleggere) i Trondheim
**Sekundær:** Håndverkere i Alta (lokal tilknytning)

### Produkt: "AI Resepsjonist for Håndverkere"
**Start enkelt:** Én god funksjon som fungerer solid, ikke alt på en gang
**Pris:** 4.500 kr/mnd + 8.000 kr oppsett (6 mnd minimum)
**Verdi:** 24/7 leads, aldri miste kundehenvendelser

### Salgsstrategi
- ✅ Telefon-outreach er OK — jeg kan ringe med god forberedelse
- ✅ Gratis pilot til første kunde (for case study)
- ✅ Test på kjent bedrift først (mors bedrift)

### Fase 1: Demo & Validering (før salg)
1. [ ] Bygg fungerende demo av AI-resepsjonist
2. [ ] Test på mors bedrift (case study)
3. [ ] Identifiser én solid funksjon som skaper mest verdi
4. [ ] Første gratis pilot-kunde

### Fase 2: Salg & Skalering
1. [ ] Finne leads i Trondheim og Alta
2. [ ] Lage outreach scripts
3. [ ] Bygge enkel CRM for pipeline
4. [ ] Konvertere pilot til betalende kunde

### Arvis rolle
- Finne leads i Trondheim OG Alta
- Hjelpe med å bygge demo
- Lage outreach scripts
- Bygge enkel CRM for pipeline tracking
- Research: Hvilken ÉN funksjon skaper mest verdi for håndverkere?

### Prinsipper
- Start enkelt, én ting som fungerer bra
- Ordentlig kvalitet først, skalering etterpå
- Ingen hast — vil gjøre det riktig
- Bruke lokal tilknytning (Trondheim + Alta) som fordel

## Viktige avklaringer som mangler
- [x] Hvilke bransjer er primærmål? ✅ Håndverkere
- [x] Hva koster en AI-assistent? ✅ 4.500 kr/mnd + 8.000 kr oppsett
- [x] Hva inkluderes? ✅ Starter med én solid funksjon (avklares)
- [x] Hvilken salgskanal? ✅ Telefon + email, med demo først
