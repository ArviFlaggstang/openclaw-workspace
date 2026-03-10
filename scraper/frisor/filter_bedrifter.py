#!/usr/bin/env python3
"""
Filtrerer frisørbedrifter fra Brønnøysundregistrene.
Beholder kun små bedrifter (ENK, AS med få ansatte) og fjerner konkurs/under avvikling.
"""

import json
from pathlib import Path

def load_raw_data():
    """Laster rå data fra fetch_brreg.py."""
    data_file = Path(__file__).parent / "data" / "raw" / "frisor_bedrifter_raw.json"
    
    if not data_file.exists():
        print(f"Fant ikke {data_file}")
        print("Kjør først: python fetch_brreg.py")
        return None
    
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)

def filter_bedrifter(bedrifter):
    """
    Filtrerer bedrifter etter kriterier:
    - Ikke konkurs
    - Ikke under avvikling
    - Små bedrifter (ENK, AS med 1-10 ansatte)
    - Ikke under tvangsavvikling
    """
    filtrerte = []
    
    for bedrift in bedrifter:
        # Hopp over hvis konkurs eller under avvikling
        if bedrift.get("konkurs"):
            continue
        if bedrift.get("under_avvikling"):
            continue
        if bedrift.get("under_tvangsavvikling"):
            continue
        
        # Sjekk organisasjonsform
        org_form = bedrift.get("organisasjonsform", "")
        
        # Behold ENK (enkeltpersonforetak) alltid
        if org_form == "ENK":
            filtrerte.append(bedrift)
            continue
        
        # Behold AS med få ansatte (1-10)
        if org_form == "AS":
            ansatte = bedrift.get("antall_ansatte")
            if ansatte is None or (1 <= ansatte <= 10):
                filtrerte.append(bedrift)
                continue
        
        # Behold ANS, DA, m.fl. med få ansatte
        if org_form in ["ANS", "DA", "KS"]:
            ansatte = bedrift.get("antall_ansatte")
            if ansatte is None or (1 <= ansatte <= 10):
                filtrerte.append(bedrift)
                continue
    
    return filtrerte

def save_filtered_data(bedrifter):
    """Lagrer filtrerte data til JSON-fil."""
    data_dir = Path(__file__).parent / "data" / "filtered"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = data_dir / "frisor_bedrifter_filtered.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(bedrifter, f, ensure_ascii=False, indent=2)
    
    print(f"Lagret {len(bedrifter)} filtrerte bedrifter til {output_file}")

def print_stats(bedrifter):
    """Skriver ut statistikk om bedriftene."""
    org_forms = {}
    for bedrift in bedrifter:
        org_form = bedrift.get("organisasjonsform", "Ukjent")
        org_forms[org_form] = org_forms.get(org_form, 0) + 1
    
    print("\n=== STATISTIKK ===")
    print(f"Totalt antall bedrifter: {len(bedrifter)}")
    print("\nOrganisasjonsformer:")
    for org_form, count in sorted(org_forms.items(), key=lambda x: x[1], reverse=True):
        print(f"  {org_form}: {count}")
    
    # Sjekk hvor mange som har hjemmeside registrert
    med_hjemmeside = sum(1 for b in bedrifter if b.get("hjemmeside"))
    uten_hjemmeside = len(bedrifter) - med_hjemmeside
    
    print(f"\nHjemmeside registrert i Brønnøysund:")
    print(f"  Med hjemmeside: {med_hjemmeside}")
    print(f"  Uten hjemmeside: {uten_hjemmeside}")

def main():
    print("Laster rå data...")
    bedrifter = load_raw_data()
    
    if not bedrifter:
        return
    
    print(f"Lastet {len(bedrifter)} bedrifter")
    print("\nFiltrerer...")
    
    filtrerte = filter_bedrifter(bedrifter)
    
    save_filtered_data(filtrerte)
    print_stats(filtrerte)
    
    print(f"\n✓ Filtrert fra {len(bedrifter)} til {len(filtrerte)} bedrifter")

if __name__ == "__main__":
    main()
