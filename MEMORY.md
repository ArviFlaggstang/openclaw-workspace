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

## Viktige avklaringer som mangler
- [ ] Hvilke bransjer er primærmål? (håndverk, restauranter, etc.)
- [ ] Hva koster en AI-assistent? (fastpris/månedlig?)
- [ ] Hva inkluderes? (oppsett, drift, support?)
