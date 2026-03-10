#!/usr/bin/env python3
"""
Henter frisørbedrifter fra Brønnøysundregistrene (Enhetsregisteret).
NACE-kode: 96.02 (Frisør og annen skjønnhetspleie)
"""

import requests
import json
import time
from pathlib import Path

# API-endepunkt
BRREG_API = "https://data.brreg.no/enhetsregisteret/api/enheter"

# Søkeord for frisør
# Disse dekker de vanligste navnene på frisørsalonger
SOKEORD = [
    "frisør",      # Standard stavemåte
    "frisor",      # Uten æ/ø/å
    "salong",      # Mange heter "Salong [Navn]"
    "hårstudio",   # Hårstudio
    "harstudio",   # Uten æ/ø/å
    "hårsenter",   # Hårsenter
    "harsenter",   # Uten æ/ø/å
    "klipp",       # Klipp & [noe]
    "barber",      # Barbershop
    "frisørsalong",# Noen bruker dette
    "frisorsalong",# Uten æ/ø/å
]

def fetch_frisor_bedrifter():
    """
    Henter alle frisørbedrifter fra Brønnøysundregistrene.
    Bruker søk på navn siden naeringskode-parameteret ikke fungerer.
    """
    bedrifter = []
    sett_navn = set()  # For å unngå duplikater
    
    print("Henter frisørbedrifter fra Brønnøysundregistrene...")
    
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
                    
                    bedrifter.append({
                        "orgnr": orgnr,
                        "navn": navn,
                        "organisasjonsform": enhet.get("organisasjonsform", {}).get("kode"),
                        "registreringsdato": enhet.get("registreringsdatoEnhetsregisteret"),
                        "naeringskode": enhet.get("naeringskode1", {}).get("kode"),
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

def save_raw_data(bedrifter):
    """Lagrer rå data til JSON-fil."""
    data_dir = Path(__file__).parent / "data" / "raw"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = data_dir / "frisor_bedrifter_raw.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(bedrifter, f, ensure_ascii=False, indent=2)
    
    print(f"\nLagret {len(bedrifter)} bedrifter til {output_file}")

def main():
    bedrifter = fetch_frisor_bedrifter()
    
    if bedrifter:
        save_raw_data(bedrifter)
        print(f"\n✓ Hentet totalt {len(bedrifter)} frisørbedrifter")
    else:
        print("\n✗ Ingen bedrifter funnet")

if __name__ == "__main__":
    main()
