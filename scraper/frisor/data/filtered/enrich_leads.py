#!/usr/bin/env python3
"""
Henter telefon og e-post fra 1881.no for frisørbedrifter.
Bruker web scraping for å finne kontaktinfo.
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

def search_1881(navn, poststed):
    """
    Søker på 1881.no etter bedrift.
    Returnerer telefon og e-post hvis funnet.
    """
    # Bygg søke-URL
    sokeord = f"{navn} {poststed}"
    url = f"https://www.1881.no/?query={quote(sokeord)}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return None, None
        
        # Sjekk om vi fant e-post
        email = None
        if "@" in response.text:
            import re
            emails = re.findall(r'[\w.-]+@[\w.-]+\.\w+', response.text)
            if emails:
                email = emails[0]
        
        # Sjekk om vi fant telefon
        phone = None
        if "Ring" in response.text:
            import re
            phones = re.findall(r'\d{3}[\s-]?\d{2}[\s-]?\d{3}', response.text)
            if phones:
                phone = phones[0].replace(" ", "").replace("-", "")
        
        return phone, email
        
    except Exception as e:
        print(f"  Feil ved søk: {e}")
        return None, None

def search_proff_no(orgnr):
    """
    Søker på proff.no etter bedrift med orgnr.
    Noen bedrifter har kontaktinfo der.
    """
    url = f"https://www.proff.no/selskap/search/{orgnr}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return None, None
        
        # Sjekk etter e-post
        email = None
        if "@" in response.text:
            import re
            emails = re.findall(r'[\w.-]+@[\w.-]+\.\w+', response.text)
            # Filtrer ut vanlige falske positive
            filtered = [e for e in emails if not any(x in e.lower() for x in ['proff.no', 'example.com', 'test.com'])]
            if filtered:
                email = filtered[0]
        
        # Sjekk etter telefon
        phone = None
        import re
        phones = re.findall(r'\d{3}[\s-]?\d{2}[\s-]?\d{3}', response.text)
        if phones:
            phone = phones[0].replace(" ", "").replace("-", "")
        
        return phone, email
        
    except Exception as e:
        return None, None

def search_google_for_contact(navn, poststed):
    """
    Alternativ: Søk på Google for å finne kontaktinfo.
    Dette er en placeholder - krever Google Custom Search API.
    """
    # TODO: Implementer med Google Custom Search API hvis nødvendig
    return None, None

def enrich_leads(leads, max_leads=20):
    """
    Beriker leads med telefon og e-post.
    Begrens til max_leads for å unngå å bli blokkert.
    """
    enriched = []
    
    print(f"Henter kontaktinfo for {min(max_leads, len(leads))} leads...")
    print("(Dette tar tid pga. rate limiting)\n")
    
    for i, lead in enumerate(leads[:max_leads]):
        navn = lead.get("navn")
        adresse = lead.get("forretningsadresse", {})
        poststed = adresse.get("poststed", "")
        
        print(f"[{i+1}/{min(max_leads, len(leads))}] {navn} - {poststed}")
        
        # Søk på 1881 først
        phone, email = search_1881(navn, poststed)
        source = "1881"
        
        # Hvis ikke funnet, prøv proff.no
        if not phone and not email:
            orgnr = lead.get("orgnr")
            phone, email = search_proff_no(orgnr)
            source = "proff.no"
        
        if phone or email:
            print(f"  ✓ Telefon: {phone or 'Ikke funnet'}")
            print(f"  ✓ E-post: {email or 'Ikke funnet'}")
            print(f"  ✓ Kilde: {source}")
        else:
            print(f"  ✗ Ingen kontaktinfo funnet (prøvde 1881 og proff.no)")
        
        # Legg til i lead
        lead["telefon"] = phone
        lead["epost"] = email
        enriched.append(lead)
        
        # Rate limiting - vær snill med serveren
        time.sleep(2)
    
    return enriched

def save_enriched_leads(leads):
    """Lagrer berikede leads."""
    output_dir = Path(__file__).parent
    output_file = output_dir / "filtered_best_leads_enriched.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(leads, f, ensure_ascii=False, indent=2)
    
    print(f"\nLagret {len(leads)} berikede leads til {output_file}")

def export_to_csv(leads):
    """Eksporterer til CSV med kontaktinfo."""
    import csv
    
    output_dir = Path(__file__).parent / "csv"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "best_leads_with_contact.csv"
    
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Org.nr", "Navn", "Organisasjonsform", "Adresse", "Postnr", "Poststed",
            "Telefon", "E-post", "Registrert", "Lead Score", "Kontaktet", "Status"
        ])
        
        for lead in leads:
            adresse = lead.get("forretningsadresse", {})
            writer.writerow([
                lead.get("orgnr", ""),
                lead.get("navn", ""),
                lead.get("organisasjonsform", ""),
                adresse.get("adresse", [""])[0] if isinstance(adresse.get("adresse"), list) else adresse.get("adresse", ""),
                adresse.get("postnummer", ""),
                adresse.get("poststed", ""),
                lead.get("telefon", ""),
                lead.get("epost", ""),
                lead.get("registreringsdato", ""),
                lead.get("lead_score", 0),
                "Nei",  # Kontaktet
                ""  # Status
            ])
    
    print(f"Eksportert til {output_file}")

def print_summary(leads):
    """Skriver ut oppsummering."""
    with_phone = sum(1 for l in leads if l.get("telefon"))
    with_email = sum(1 for l in leads if l.get("epost"))
    
    print("\n" + "=" * 60)
    print("RESULTAT")
    print("=" * 60)
    print(f"Totalt beriket: {len(leads)}")
    print(f"Med telefon: {with_phone}")
    print(f"Med e-post: {with_email}")
    print(f"Uten kontaktinfo: {len(leads) - max(with_phone, with_email)}")
    
    print("\nTop 10 leads med kontaktinfo:")
    for i, lead in enumerate(leads[:10], 1):
        phone = lead.get("telefon") or "-"
        email = lead.get("epost") or "-"
        print(f"  {i}. {lead['navn'][:35]:35} | Tlf: {phone:12} | {email[:30]}")

def main():
    print("=" * 60)
    print("HENTER KONTAKTINFO FRA 1881.NO")
    print("=" * 60)
    print()
    
    # Last leads
    leads = load_best_leads()
    print(f"Lastet {len(leads)} beste leads")
    
    # Berik med kontaktinfo
    enriched = enrich_leads(leads, max_leads=20)
    
    # Lagre og eksporter
    save_enriched_leads(enriched)
    export_to_csv(enriched)
    print_summary(enriched)
    
    print("\n" + "=" * 60)
    print("FERDIG!")
    print("=" * 60)
    print("\nNeste steg:")
    print("1. Åpne: csv/best_leads_with_contact.csv")
    print("2. Send cold emails til de med e-post")
    print("3. Ring de med telefon (eller send SMS)")

if __name__ == "__main__":
    main()
