#!/usr/bin/env python3
"""
Sjekker om bedrifter faktisk har nettside.
Noen bedrifter har nettside selv om den ikke er registrert i Brønnøysund.
"""

import json
import requests
from pathlib import Path
from urllib.parse import urlparse
import time

def load_filtered_data():
    """Laster filtrerte data."""
    data_file = Path(__file__).parent / "data" / "filtered" / "frisor_bedrifter_filtered.json"
    
    if not data_file.exists():
        print(f"Fant ikke {data_file}")
        print("Kjør først: python filter_bedrifter.py")
        return None
    
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)

def check_website(url):
    """
    Sjekker om en URL er tilgjengelig.
    Returnerer True hvis nettsiden finnes og svarer.
    """
    if not url:
        return False
    
    # Legg til https:// hvis det mangler
    if not url.startswith("http"):
        url = "https://" + url
    
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def search_google_for_website(bedrift_navn, orgnr):
    """
    Søker etter bedriftens nettside via Google.
    Dette er en placeholder - krever Google Custom Search API.
    """
    # TODO: Implementer med Google Custom Search API
    # API-nøkkel kreves: https://developers.google.com/custom-search/v1/overview
    return None

def check_bedrifter(bedrifter, max_checks=50):
    """
    Sjekker nettside for bedrifter.
    Begrens til max_checks for å unngå å bli blokkert.
    """
    resultater = []
    
    print(f"Sjekker nettside for opptil {max_checks} bedrifter...")
    
    for i, bedrift in enumerate(bedrifter[:max_checks]):
        orgnr = bedrift.get("orgnr")
        navn = bedrift.get("navn")
        registrert_hjemmeside = bedrift.get("hjemmeside")
        
        print(f"\n[{i+1}/{min(max_checks, len(bedrifter))}] {navn}")
        
        # Sjekk registrert hjemmeside først
        if registrert_hjemmeside:
            print(f"  Registrert hjemmeside: {registrert_hjemmeside}")
            har_nettside = check_website(registrert_hjemmeside)
            print(f"  Nettside fungerer: {har_nettside}")
        else:
            print(f"  Ingen hjemmeside registrert")
            har_nettside = False
        
        # Lagre resultat
        resultater.append({
            **bedrift,
            "har_nettside": har_nettside,
            "nettside_sjekket": True
        })
        
        time.sleep(1)  # Vær snill med servere
    
    return resultater

def save_final_data(bedrifter):
    """Lagrer endelig liste med nettsidesjekk."""
    data_dir = Path(__file__).parent / "data" / "final"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = data_dir / "frisor_bedrifter_final.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(bedrifter, f, ensure_ascii=False, indent=2)
    
    print(f"\nLagret {len(bedrifter)} bedrifter til {output_file}")

def export_to_csv(bedrifter):
    """Eksporterer til CSV for import i Excel/Google Sheets."""
    import csv
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "frisorer_uten_nettside.csv"
    
    # Filtrer kun de uten nettside
    uten_nettside = [b for b in bedrifter if not b.get("har_nettside")]
    
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Org.nr", "Navn", "Organisasjonsform", "Adresse", "Postnr", "Poststed",
            "Telefon", "E-post", "Hjemmeside (registrert)", "Har nettside"
        ])
        
        for bedrift in uten_nettside:
            adresse = bedrift.get("forretningsadresse", {})
            writer.writerow([
                bedrift.get("orgnr", ""),
                bedrift.get("navn", ""),
                bedrift.get("organisasjonsform", ""),
                adresse.get("adresse", ""),
                adresse.get("postnummer", ""),
                adresse.get("poststed", ""),
                "",  # Telefon (må hentes fra annen kilde)
                "",  # E-post (må hentes fra annen kilde)
                bedrift.get("hjemmeside", ""),
                "Nei"
            ])
    
    print(f"Eksportert {len(uten_nettside)} bedrifter uten nettside til {output_file}")

def main():
    print("Laster filtrerte data...")
    bedrifter = load_filtered_data()
    
    if not bedrifter:
        return
    
    print(f"Lastet {len(bedrifter)} bedrifter")
    
    # Sjekk nettside for et utvalg
    resultater = check_bedrifter(bedrifter, max_checks=50)
    
    save_final_data(resultater)
    export_to_csv(resultater)
    
    # Statistikk
    med_nettside = sum(1 for b in resultater if b.get("har_nettside"))
    uten_nettside = len(resultater) - med_nettside
    
    print("\n=== RESULTAT ===")
    print(f"Totalt sjekket: {len(resultater)}")
    print(f"Med nettside: {med_nettside}")
    print(f"Uten nettside: {uten_nettside}")
    print(f"\n✓ CSV-fil klar for cold emailing!")

if __name__ == "__main__":
    main()
