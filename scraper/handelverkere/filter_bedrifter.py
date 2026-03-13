#!/usr/bin/env python3
"""
Filtrerer håndverkerbedrifter basert på kriterier.
- Kun AS (aksjeselskap)
- Ikke konkurs
- Ikke under avvikling
- Prioriterer bedrifter uten nettside eller med svak nettside
"""

import json
import csv
from pathlib import Path

def filter_bedrifter(json_file):
    """Filtrerer bedrifter basert på kriterier."""
    with open(json_file, "r", encoding="utf-8") as f:
        bedrifter = json.load(f)
    
    print(f"Filtrerer {len(bedrifter)} bedrifter...")
    
    filtrerte = []
    
    for bedrift in bedrifter:
        # Sjekk grunnleggende kriterier
        if bedrift.get("konkurs"):
            continue
        if bedrift.get("under_avvikling"):
            continue
        if bedrift.get("under_tvangsavvikling"):
            continue
        
        # Kun AS
        if bedrift.get("organisasjonsform") != "AS":
            continue
        
        filtrerte.append(bedrift)
    
    return filtrerte

def sort_by_potential(bedrifter):
    """Sorterer bedrifter etter potensial for AI-salg."""
    def score(bedrift):
        score = 0
        
        # Bedrifter uten nettside er gode mål
        if not bedrift.get("hjemmeside"):
            score += 10
        
        # Bedrifter med svak nettside (hvis analysert)
        analyse = bedrift.get("nettside_analyse", {})
        if analyse:
            score += (10 - analyse.get("score", 5))  # Lavere score = høyere potensial
            
            # Bonus hvis de ikke har booking-system
            if not analyse.get("har_booking", False):
                score += 5
            
            # Bonus hvis de ikke har AI
            if not analyse.get("har_ai", False):
                score += 3
        
        # Bedrifter med mange ansatte = større omsetning
        ansatte = bedrift.get("antall_ansatte", 0)
        if ansatte:
            score += min(ansatte, 10)  # Max 10 poeng for ansatte
        
        return score
    
    return sorted(bedrifter, key=score, reverse=True)

def save_csv(bedrifter, filename="haandverkere_top.csv"):
    """Lagrer til CSV."""
    data_dir = Path(__file__).parent / "data" / "filtered"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = data_dir / filename
    
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Navn", "Sted", "Org.nr", "Bransje", "Ansatte", "Google-søk", "E-post", "Telefon", "Nettside", "Potensial"])
        
        for b in bedrifter:
            sted = b["forretningsadresse"].get("poststed", "")
            google_sok = f"https://www.google.com/search?q={b['navn'].replace(' ', '+')}+{sted}+epost"
            
            # Beregn potensial-score
            analyse = b.get("nettside_analyse", {})
            potensial = "Høyt" if analyse.get("score", 5) <= 3 else "Middels" if analyse.get("score", 5) <= 6 else "Lavt"
            
            writer.writerow([
                b["navn"],
                sted,
                b["orgnr"],
                b.get("bransje", "Ukjent"),
                b.get("antall_ansatte", ""),
                google_sok,
                "",  # E-post (må fylles inn manuelt)
                "",  # Telefon
                b.get("hjemmeside", ""),
                potensial
            ])
    
    print(f"Lagret {len(bedrifter)} filtrerte bedrifter til {output_file}")

def main():
    # Prøv analysert fil først, ellers rå fil
    json_file = Path(__file__).parent / "data" / "analyzed" / "haandverker_analysert.json"
    if not json_file.exists():
        json_file = Path(__file__).parent / "data" / "raw" / "haandverker_bedrifter_raw.json"
    
    if not json_file.exists():
        print(f"Fant ikke datafil. Kjør først: python fetch_brreg.py")
        return
    
    filtrerte = filter_bedrifter(json_file)
    sorterte = sort_by_potential(filtrerte)
    
    # Lagre topp 100
    save_csv(sorterte[:100], "haandverkere_top100.csv")
    
    # Lagre alle
    save_csv(sorterte, "haandverkere_all.csv")
    
    print(f"\n✓ Filtrert til {len(filtrerte)} AS-bedrifter")
    print(f"  Topp 100 lagret i haandverkere_top100.csv")
    print(f"  Alle {len(sorterte)} lagret i haandverkere_all.csv")

if __name__ == "__main__":
    main()
