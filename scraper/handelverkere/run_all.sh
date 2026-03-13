#!/bin/bash
# Kjør alle steg for håndverker-scraping

echo "======================================"
echo "HÅNDVERKER SCRAPER - KOMPLETT KJØRING"
echo "======================================"
echo ""

# Steg 1: Hent data fra Brønnøysundregistrene
echo "Steg 1: Henter håndverkerbedrifter fra Brønnøysundregistrene..."
python3 fetch_brreg.py

if [ $? -ne 0 ]; then
    echo "Feil ved henting av data"
    exit 1
fi

echo ""
echo "Steg 2: Sjekker nettsider (valgfritt, tar tid)..."
read -p "Vil du sjekke nettsider? Dette tar flere minutter. (j/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Jj]$ ]]; then
    python3 check_website.py
fi

echo ""
echo "Steg 3: Filtrerer og sorterer bedrifter..."
python3 filter_bedrifter.py

echo ""
echo "======================================"
echo "FERDIG!"
echo "======================================"
echo ""
echo "Resultater ligger i:"
echo "  - data/raw/haandverker_bedrifter_raw.json (alle data)"
echo "  - data/analyzed/haandverker_analysert.json (med nettside-analyse)"
echo "  - data/filtered/haandverkere_top100.csv (topp 100)"
echo "  - data/filtered/haandverkere_all.csv (alle)"
echo ""
echo "Neste steg:"
echo "  1. Åpne haandverkere_top100.csv"
echo "  2. Søk opp bedrifter på Facebook/Google for å finne e-poster"
echo "  3. Oppdater E-post-kolonnen"
echo ""
