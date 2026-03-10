#!/bin/bash

# Kjør alle scraper-skript i rekkefølge

echo "=========================================="
echo "Frisør Scraper - Brønnøysundregistrene"
echo "=========================================="
echo ""

# Sjekk om Python er installert
if ! command -v python3 &> /dev/null; then
    echo "Python3 er ikke installert. Installer det først:"
    echo "  sudo apt-get install python3 python3-pip"
    exit 1
fi

# Sjekk om requests er installert
if ! python3 -c "import requests" 2>/dev/null; then
    echo "Installerer nødvendige Python-pakker..."
    pip3 install requests
fi

echo "Steg 1: Henter frisørbedrifter fra Brønnøysundregistrene..."
python3 fetch_brreg.py
if [ $? -ne 0 ]; then
    echo "Feil ved henting av data"
    exit 1
fi

echo ""
echo "Steg 2: Filtrerer bedrifter..."
python3 filter_bedrifter.py
if [ $? -ne 0 ]; then
    echo "Feil ved filtrering"
    exit 1
fi

echo ""
echo "Steg 3: Sjekker nettsider (begrenset til 50 bedrifter)..."
python3 check_website.py
if [ $? -ne 0 ]; then
    echo "Feil ved nettsidesjekk"
    exit 1
fi

echo ""
echo "=========================================="
echo "Ferdig!"
echo "=========================================="
echo ""
echo "Resultater ligger i:"
echo "  - data/final/frisor_bedrifter_final.json"
echo "  - output/frisorer_uten_nettside.csv"
echo ""
