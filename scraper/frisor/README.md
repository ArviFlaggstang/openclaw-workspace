# Frisør Scraper

Henter frisørbedrifter fra Brønnøysundregistrene og filtrerer etter:
- NACE-kode 96.02 (Frisør og annen skjønnhetspleie)
- Små bedrifter (ENK, AS med 1-5 ansatte)
- Manglende nettside

## API-endepunkt

Brønnøysundregistrene (Enhetsregisteret):
- Base URL: `https://data.brreg.no/enhetsregisteret/api/enheter`
- Dokumentasjon: https://data.brreg.no/enhetsregisteret/api/docs/

## NACE-koder

- **96.02** - Frisør og annen skjønnhetspleie
- **96.020** - Frisør og annen skjønnhetspleie

## Filstruktur

```
scraper/frisor/
├── README.md           # Denne filen
├── fetch_brreg.py      # Henter data fra Brønnøysund
├── filter_bedrifter.py # Filtrerer og beriker data
├── check_website.py    # Sjekker om bedrifter har nettside
├── data/
│   ├── raw/            # Rå data fra API
│   ├── filtered/       # Filtrerte bedrifter
│   └── final/          # Endelig liste klar for bruk
└── output/
    └── frisorer_uten_nettside.csv
```

## Fremgangsmåte

1. **Hent fra Brønnøysund** - Alle med NACE 96.02
2. **Filtrer** - Fjern store bedrifter, behold ENK/små AS
3. **Berik** - Hent telefon/adresse fra 1881/Gulesider
4. **Sjekk nettside** - Automatisk sjekk om de har hjemmeside
5. **Eksporter** - CSV klar for cold emailing

## Begrensninger

- Brønnøysundregistrene oppdateres daglig
- Rate limiting: Vær snill med API-et
- Ikke alle bedrifter har registrert nettside (selv om de har en)
