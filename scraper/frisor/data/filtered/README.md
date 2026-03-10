# Filtrerte Leads - Frisør

Denne mappen inneholder filtrerte og bearbeidede lister over frisørbedrifter.

## Filstruktur

```
data/filtered/
├── README.md                           # Denne filen
├── combined_all.json                   # Alle bedrifter kombinert (uten duplikater)
├── filtered_small_business.json        # Kun små bedrifter (ENK, AS 1-10 ansatte)
├── filtered_no_website.json            # Uten nettside (fra Brønnøysund)
├── filtered_trondheim.json             # I Trondheim-området
├── filtered_best_leads.json            # 🎯 BESTE LEADS (alt filtrert)
└── csv/
    ├── best_leads_for_email.csv        # Klar for cold email
    └── best_leads_for_calling.csv      # Klar for oppringing (med telefon)
```

## Filtreringskriterier

### Hva vi kan filtrere på (fra Brønnøysund-data):

| Kriterie | Mulig? | Kommentar |
|----------|--------|-----------|
| **Organisasjonsform** | ✅ Ja | ENK, AS, ANS, DA |
| **Antall ansatte** | ✅ Ja | 1-10 ansatte |
| **Konkurs/avvikling** | ✅ Ja | Fjerne disse |
| **Hjemmeside registrert** | ✅ Ja | Sjekke `hjemmeside`-feltet |
| **Adresse/poststed** | ✅ Ja | Filtrere på sted |
| **Registreringsdato** | ✅ Ja | Nye vs etablerte |

### Hva vi IKKE kan filtrere på (må hentes eksternt):

| Kriterie | Mulig? | Kommentar |
|----------|--------|-----------|
| **Telefon** | ❌ Nei | Må scrapes fra 1881/Gulesider |
| **E-post** | ❌ Nei | Må scrapes fra nettside/Gulesider |
| **Faktisk nettside** | ❌ Nei | Må sjekke om URL fungerer |
| **Anmeldelser/rating** | ❌ Nei | Må hentes fra Google/Facebook |
| **Omsetning** | ❌ Nei | Kun for regnskapspliktige |

## Prioritering av leads (BESTE først):

1. **ENK (enkeltpersonforetak)** — eier = beslutningstaker
2. **Små AS (1-5 ansatte)** — enkle å selge til
3. **Uten nettside registrert** — størst behov
4. **Etablert 3+ år** — stabile, ikke startups
5. **Ikke konkurs/avvikling** — selvsagt
6. **Lokalt i Trondheim** — lettere å møtes

## Neste steg

1. Kombiner rådata → `combined_all.json`
2. Filtrer små bedrifter → `filtered_small_business.json`
3. Sjekke faktisk nettside (automatisk)
4. Filtrere beste leads → `filtered_best_leads.json`
5. Hente telefon/e-post (manuelt/automatisk)
6. Eksportere til CSV for emailing

## Cold Email vs Oppringing

| Metode | Fordeler | Ulemper |
|--------|----------|---------|
| **Cold Email** | Skalerbart, kan sende til mange | Lav svarprosent (5-10%) |
| **Oppringing** | Høyere konvertering, personlig | Tidkrevende |
| **Kombinasjon** | Email først → telefon til de som åpner | Beste av begge |

## Anbefaling

Start med **100 beste leads** i Trondheim-området:
- Kombiner filtrering
- Send cold email
- Følg opp med telefon etter 3-4 dager
- Møt de som biter

Deretter skaler til flere leads.
