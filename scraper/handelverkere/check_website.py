#!/usr/bin/env python3
"""
Sjekker nettsider for håndverkerbedrifter og vurderer kvaliteten.
Bruker requests og beautifulsoup for å analysere nettsider.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path
from urllib.parse import urlparse

def check_website(url, timeout=10):
    """
    Sjekker en nettside og returnerer informasjon om kvaliteten.
    """
    if not url:
        return {
            "har_nettside": False,
            "status": "Ingen nettside",
            "score": 0
        }
    
    # Legg til https:// hvis det mangler
    if not url.startswith("http"):
        url = "https://" + url
    
    try:
        response = requests.get(url, timeout=timeout, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        
        if response.status_code != 200:
            return {
                "har_nettside": True,
                "status": f"HTTP {response.status_code}",
                "score": 1
            }
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Sjekk for kontaktskjema
        har_kontaktskjema = bool(soup.find("form"))
        
        # Sjekk for e-post
        epost_elementer = soup.find_all(text=lambda text: text and "@" in text and "." in text.split("@")[-1])
        har_epost = len(epost_elementer) > 0
        
        # Sjekk for telefon
        telefon_elementer = soup.find_all(text=lambda text: text and any(c.isdigit() for c in text) and 
                                          ("tlf" in text.lower() or "telefon" in text.lower() or 
                                           "+47" in text or len([c for c in text if c.isdigit()]) >= 8))
        har_telefon = len(telefon_elementer) > 0
        
        # Sjekk for online booking/timebestilling
        booking_ord = ["bestill", "time", "booking", "avtale", "kontakt", "timebestilling"]
        har_booking = any(ord in response.text.lower() for ord in booking_ord)
        
        # Sjekk for AI/chatbot
        ai_ord = ["chat", "chatbot", "ai", "kunstig intelligens", "automatisk"]
        har_ai = any(ord in response.text.lower() for ord in ai_ord)
        
        # Beregn score (0-10)
        score = 5  # Baseline for å ha nettside
        
        if har_kontaktskjema:
            score += 2
        if har_epost:
            score += 1
        if har_telefon:
            score += 1
        if har_booking:
            score += 2  # Viktig for håndverkere
        if har_ai:
            score += 2  # Allerede har AI = ikke målgruppe
        
        # Trekk poeng for dårlige tegn
        if "under construction" in response.text.lower():
            score -= 3
        if len(response.text) < 1000:
            score -= 2  # Tom/svak side
        
        return {
            "har_nettside": True,
            "status": "OK",
            "score": max(0, min(10, score)),
            "har_kontaktskjema": har_kontaktskjema,
            "har_epost": har_epost,
            "har_telefon": har_telefon,
            "har_booking": har_booking,
            "har_ai": har_ai,
            "url": url
        }
        
    except requests.exceptions.Timeout:
        return {
            "har_nettside": True,
            "status": "Timeout",
            "score": 2
        }
    except requests.exceptions.RequestException as e:
        return {
            "har_nettside": True,
            "status": f"Feil: {str(e)[:50]}",
            "score": 1
        }

def analyze_bedrifter(json_file):
    """Analyserer alle bedrifter i JSON-filen."""
    with open(json_file, "r", encoding="utf-8") as f:
        bedrifter = json.load(f)
    
    print(f"Sjekker {len(bedrifter)} nettsider...")
    
    resultater = []
    for i, bedrift in enumerate(bedrifter):
        if i % 10 == 0:
            print(f"  Behandler {i+1}/{len(bedrifter)}...")
        
        url = bedrift.get("hjemmeside")
        analyse = check_website(url)
        
        resultater.append({
            **bedrift,
            "nettside_analyse": analyse
        })
        
        time.sleep(0.5)  # Vær snill med servere
    
    return resultater

def save_results(resultater, filename="haandverker_analysert.json"):
    """Lagrer analyserte resultater."""
    data_dir = Path(__file__).parent / "data" / "analyzed"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = data_dir / filename
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(resultater, f, ensure_ascii=False, indent=2)
    
    print(f"\nLagret analyserte resultater til {output_file}")

def print_summary(resultater):
    """Skriver ut en oppsummering."""
    har_nettside = sum(1 for r in resultater if r["nettside_analyse"]["har_nettside"])
    har_booking = sum(1 for r in resultater if r["nettside_analyse"].get("har_booking", False))
    har_ai = sum(1 for r in resultater if r["nettside_analyse"].get("har_ai", False))
    
    # Score-fordeling
    scores = [r["nettside_analyse"]["score"] for r in resultater]
    lav_score = sum(1 for s in scores if s <= 3)
    middels_score = sum(1 for s in scores if 4 <= s <= 6)
    hoy_score = sum(1 for s in scores if s >= 7)
    
    print("\n" + "="*60)
    print("OPPSUMMERING")
    print("="*60)
    print(f"Totalt antall bedrifter: {len(resultater)}")
    print(f"Har nettside: {har_nettside} ({100*har_nettside//len(resultater)}%)")
    print(f"Har online booking: {har_booking}")
    print(f"Har allerede AI: {har_ai}")
    print(f"\nScore-fordeling:")
    print(f"  Lav (0-3): {lav_score} bedrifter - GODE MÅLGRUPPER!")
    print(f"  Middels (4-6): {middels_score} bedrifter")
    print(f"  Høy (7-10): {hoy_score} bedrifter - Har allerede mye digitalisering")

def main():
    raw_file = Path(__file__).parent / "data" / "raw" / "haandverker_bedrifter_raw.json"
    
    if not raw_file.exists():
        print(f"Fant ikke {raw_file}")
        print("Kjør først: python fetch_brreg.py")
        return
    
    resultater = analyze_bedrifter(raw_file)
    save_results(resultater)
    print_summary(resultater)

if __name__ == "__main__":
    main()
