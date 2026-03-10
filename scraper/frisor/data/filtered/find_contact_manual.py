#!/usr/bin/env python3
"""
Henter ekte kontaktinfo fra flere kilder.
Prøver: Facebook, Google, Proff, Gulesider
"""

import json
import requests
import time
from pathlib import Path
from urllib.parse import quote

def load_best_leads():
    """Laster de beste leadsene."""
    data_file = Path(__file__).parent / "filtered_best_leads.json"
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)

def search_facebook_email(navn, poststed):
    """
    Søker på Facebook for å finne e-post.
    Mange små bedrifter har e-post på Facebook-siden sin.
    """
    # Bruk web search for å finne Facebook-side
    sokeord = f"{navn} {poststed} facebook email"
    
    try:
        # Dette er en placeholder - vi kan ikke scrape Google direkte
        # Men vi kan bruke Brave Search API eller lignende
        return None
    except:
        return None

def search_google_for_contact(navn, poststed, orgnr):
    """
    Bruker web search for å finne kontaktinfo.
    Krever API-nøkkel for Brave Search eller Google Custom Search.
    """
    # TODO: Implementer med Brave Search API hvis tilgjengelig
    # For nå, returner None
    return None, None

def find_contact_manually(navn, poststed, orgnr):
    """
    Lager en søke-URL som brukeren kan åpne manuelt
    for å finne kontaktinfo.
    """
    queries = [
        f"{navn} {poststed} epost",
        f"{navn} {poststed} facebook",
        f"{navn} {poststed} telefon",
        f"{navn} {poststed} 1881",
        f"{navn} {poststed} gulesider",
    ]
    
    return [f"https://www.google.com/search?q={quote(q)}" for q in queries]

def enrich_leads_manual(leads, max_leads=20):
    """
    Lager en liste med manuelle søk for hver bedrift.
    Brukeren må selv åpne URL-ene og finne kontaktinfo.
    """
    enriched = []
    
    print("=" * 70)
    print("MANUELL KONTAKTINFO-JAKT")
    print("=" * 70)
    print("\nJeg lager Google-søk for hver bedrift.")
    print("Du må selv åpne linkene og finne e-post/telefon.\n")
    
    for i, lead in enumerate(leads[:max_leads]):
        navn = lead.get("navn")
        adresse = lead.get("forretningsadresse", {})
        poststed = adresse.get("poststed", "")
        orgnr = lead.get("orgnr")
        
        print(f"\n[{i+1}/{min(max_leads, len(leads))}] {navn}")
        print(f"    Adresse: {adresse.get('adresse', [''])[0] if isinstance(adresse.get('adresse'), list) else ''}, {poststed}")
        print(f"    Org.nr: {orgnr}")
        print(f"\n    Søk her:")
        
        urls = find_contact_manually(navn, poststed, orgnr)
        for j, url in enumerate(urls, 1):
            print(f"      {j}. {url}")
        
        # Lagre URL-ene
        lead["search_urls"] = urls
        enriched.append(lead)
        
        print("\n" + "-" * 70)
    
    return enriched

def save_manual_search_list(leads):
    """Lagrer liste med manuelle søk."""
    output_dir = Path(__file__).parent
    
    # JSON med alle URL-er
    output_file = output_dir / "manual_search_list.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(leads, f, ensure_ascii=False, indent=2)
    
    # Tekstfil lett å lese
    output_txt = output_dir / "manual_search_list.txt"
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write("MANUELL KONTAKTINFO-JAKT - TOPP 20 LEADS\n")
        f.write("=" * 70 + "\n\n")
        
        for i, lead in enumerate(leads, 1):
            navn = lead.get("navn")
            adresse = lead.get("forretningsadresse", {})
            poststed = adresse.get("poststed", "")
            adresse_str = adresse.get("adresse", [""])[0] if isinstance(adresse.get("adresse"), list) else ""
            orgnr = lead.get("orgnr")
            
            f.write(f"{i}. {navn}\n")
            f.write(f"   Adresse: {adresse_str}, {poststed}\n")
            f.write(f"   Org.nr: {orgnr}\n")
            f.write(f"   Søk:\n")
            
            for url in lead.get("search_urls", []):
                f.write(f"      {url}\n")
            
            f.write("\n" + "-" * 70 + "\n\n")
    
    print(f"\nLagret til:")
    print(f"  - {output_file}")
    print(f"  - {output_txt}")

def main():
    print("=" * 70)
    print("KONTAKTINFO-FINNER")
    print("=" * 70)
    print()
    
    leads = load_best_leads()
    print(f"Lastet {len(leads)} beste leads")
    print()
    
    # Siden automatisk scraping er vanskelig/ureliable,
    # lager vi manuelle søk i stedet
    enriched = enrich_leads_manual(leads, max_leads=20)
    
    save_manual_search_list(enriched)
    
    print("\n" + "=" * 70)
    print("FERDIG!")
    print("=" * 70)
    print("\nNeste steg:")
    print("1. Åpne filen: manual_search_list.txt")
    print("2. Gå gjennom hver bedrift og klikk på Google-søk-linkene")
    print("3. Finn e-post (ofte på Facebook, 1881, eller egen nettside)")
    print("4. Noter e-post og telefon i CSV-filen")
    print("5. Send cold emails!")

if __name__ == "__main__":
    main()
