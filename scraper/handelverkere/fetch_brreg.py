#!/usr/bin/env python3
"""
Henter håndverkerbedrifter fra Brønnøysundregistrene (Enhetsregisteret).
NACE-koder:
- 43.220: VVS-arbeid (rørlegger)
- 43.221: Rørleggerarbeid
- 43.320: Snekkerarbeid
- 43.330: Gulvlegging
- 43.340: Malerarbeid
- 43.390: Andre bygge- og anleggsinstallasjoner
- 43.210: Elektrisk installasjonsarbeid (elektriker)
- 43.290: Andre elektrotekniske installasjoner
"""

import requests
import json
import time
from pathlib import Path

# API-endepunkt
BRREG_API = "https://data.brreg.no/enhetsregisteret/api/enheter"

# Søkeord for håndverkere (kortet ned for raskere kjøring)
SOKEORD = [
    "VVS",
    "rørlegger",
    "rorlegger",
    "elektro",
    "elektriker",
    "snekker",
    "tømrer",
    "tomrer",
    "maler",
]

# NACE-koder for håndverkere
NACE_KODER = [
    "43.220",  # VVS-arbeid
    "43.221",  # Rørleggerarbeid
    "43.320",  # Snekkerarbeid
    "43.330",  # Gulvlegging
    "43.340",  # Malerarbeid
    "43.210",  # Elektrisk installasjonsarbeid
    "43.290",  # Andre elektrotekniske installasjoner
]

def fetch_haandverker_bedrifter():
    """
    Henter alle håndverkerbedrifter fra Brønnøysundregistrene.
    Bruker søk på navn og NACE-koder.
    """
    bedrifter = []
    sett_navn = set()  # For å unngå duplikater
    
    print("Henter håndverkerbedrifter fra Brønnøysundregistrene...")
    
    for sokeord in SOKEORD:
        page = 0
        size = 100
        
        print(f"\nSøker etter '{sokeord}'...")
        
        while True:
            params = {
                "navn": sokeord,
                "size": size,
                "page": page
            }
            
            try:
                response = requests.get(BRREG_API, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                # Hent bedrifter fra denne siden
                enheter = data.get("_embedded", {}).get("enheter", [])
                
                if not enheter:
                    break
                
                for enhet in enheter:
                    orgnr = enhet.get("organisasjonsnummer")
                    navn = enhet.get("navn")
                    
                    # Unngå duplikater
                    if orgnr in sett_navn:
                        continue
                    sett_navn.add(orgnr)
                    
                    # Bestem bransje basert på NACE-kode eller navn
                    naeringskode = enhet.get("naeringskode1", {}).get("kode", "")
                    bransje = bestem_bransje(navn, naeringskode)
                    
                    bedrifter.append({
                        "orgnr": orgnr,
                        "navn": navn,
                        "bransje": bransje,
                        "organisasjonsform": enhet.get("organisasjonsform", {}).get("kode"),
                        "registreringsdato": enhet.get("registreringsdatoEnhetsregisteret"),
                        "naeringskode": naeringskode,
                        "naeringsbeskrivelse": enhet.get("naeringskode1", {}).get("beskrivelse"),
                        "forretningsadresse": enhet.get("forretningsadresse", {}),
                        "postadresse": enhet.get("postadresse", {}),
                        "hjemmeside": enhet.get("hjemmeside"),
                        "antall_ansatte": enhet.get("antallAnsatte"),
                        "konkurs": enhet.get("konkurs", False),
                        "under_avvikling": enhet.get("underAvvikling", False),
                        "under_tvangsavvikling": enhet.get("underTvangsavviklingEllerTvangsopplosning", False)
                    })
                
                print(f"  Side {page + 1}: Hentet {len(enheter)} bedrifter (totalt unike: {len(bedrifter)})")
                
                # Sjekk om det er flere sider
                if len(enheter) < size:
                    break
                
                page += 1
                time.sleep(0.5)  # Vær snill med API-et
                
            except requests.exceptions.RequestException as e:
                print(f"Feil ved henting: {e}")
                break
    
    return bedrifter

def bestem_bransje(navn, naeringskode):
    """Bestemmer bransje basert på navn og NACE-kode."""
    navn_lower = navn.lower()
    
    # Sjekk NACE-kode først
    if naeringskode in ["43.220", "43.221"]:
        return "VVS/Rørlegger"
    elif naeringskode in ["43.210", "43.290"]:
        return "Elektriker"
    elif naeringskode == "43.320":
        return "Snekker"
    elif naeringskode == "43.330":
        return "Gulvlegger"
    elif naeringskode == "43.340":
        return "Maler"
    
    # Sjekk navn hvis NACE-kode ikke matcher
    if any(word in navn_lower for word in ["vvs", "rørlegger", "rorlegger", "rørservice", "rorservice"]):
        return "VVS/Rørlegger"
    elif any(word in navn_lower for word in ["elektro", "elektriker", "el-installasjon", "el installasjon"]):
        return "Elektriker"
    elif any(word in navn_lower for word in ["snekker", "tømrer", "tomrer"]):
        return "Snekker"
    elif "maler" in navn_lower:
        return "Maler"
    elif "gulv" in navn_lower:
        return "Gulvlegger"
    elif "ventilasjon" in navn_lower:
        return "Ventilasjon"
    elif "varmepumpe" in navn_lower:
        return "Varmepumpe"
    else:
        return "Annet håndverk"

def save_raw_data(bedrifter, filename="haandverker_bedrifter_raw.json"):
    """Lagrer rå data til JSON-fil."""
    data_dir = Path(__file__).parent / "data" / "raw"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = data_dir / filename
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(bedrifter, f, ensure_ascii=False, indent=2)
    
    print(f"\nLagret {len(bedrifter)} bedrifter til {output_file}")

def save_csv(bedrifter, filename="haandverkere.csv"):
    """Lagrer filtrerte bedrifter til CSV."""
    import csv
    
    data_dir = Path(__file__).parent / "data" / "filtered"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = data_dir / filename
    
    # Filtrer: kun AS, ikke konkurs, ikke under avvikling
    filtrerte = [
        b for b in bedrifter 
        if b["organisasjonsform"] == "AS" 
        and not b["konkurs"]
        and not b["under_avvikling"]
        and not b["under_tvangsavvikling"]
    ]
    
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Navn", "Sted", "Org.nr", "Bransje", "Google-søk", "E-post", "Telefon", "Nettside"])
        
        for b in filtrerte:
            sted = b["forretningsadresse"].get("poststed", "")
            google_sok = f"https://www.google.com/search?q={b['navn'].replace(' ', '+')}+{sted}+epost"
            
            writer.writerow([
                b["navn"],
                sted,
                b["orgnr"],
                b["bransje"],
                google_sok,
                "",  # E-post (må fylles inn manuelt)
                "",  # Telefon
                b["hjemmeside"] or ""
            ])
    
    print(f"Lagret {len(filtrerte)} filtrerte AS-bedrifter til {output_file}")

def main():
    bedrifter = fetch_haandverker_bedrifter()
    
    if bedrifter:
        save_raw_data(bedrifter)
        save_csv(bedrifter)
        print(f"\n✓ Hentet totalt {len(bedrifter)} håndverkerbedrifter")
    else:
        print("\n✗ Ingen bedrifter funnet")

if __name__ == "__main__":
    main()
