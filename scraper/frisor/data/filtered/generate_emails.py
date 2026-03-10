#!/usr/bin/env python3
"""
Fyller ut e-postmal med variabler og genererer ferdige e-poster.
"""

import json
import csv
from pathlib import Path
from datetime import datetime

def load_email_template():
    """Laster e-postmalen."""
    template_file = Path(__file__).parent / "email_mal_med_variabler.md"
    
    # Les malen (vi antar den er i markdown-filen)
    # For enkelhets skyld, lagrer vi malen som en string her
    template = """Hei {{BEDRIFT_NAVN}},

Jeg kom over {{BEDRIFT_NAVN}} da jeg så etter frisører i {{STED}}. Jeg la merke til at dere har holdt på i {{ETABLERT_ÅR}} år — det er imponerende!

Men da jeg googlet dere, fant jeg ingen egen nettside. Det gjør det vanskelig for nye kunder å finne informasjon om dere.

Jeg studerer datateknologi på NTNU og lager nettsider for små bedrifter. Jeg har laget en **gratis demo** av hvordan en enkel nettside for {{BEDRIFT_NAVN}} kunne sett ut:

👉 {{DEMO_LINK}}

Demoen inkluderer:
- Åpningstider og kontaktinfo
- Prisoversikt
- Mulighet for online booking
- Mobilvennlig design

Dette er **helt uforpliktende** — bare et forslag jeg ville dele. Hvis du synes det ser interessant ut, kan jeg tilpasse den med deres logo, bilder og tekst.

**Pris:** Én engangssum for å sette opp siden, pluss en liten månedlig sum for hosting og vedlikehold. Du slipper å tenke på noe teknisk.

Si fra hvis du vil jeg skal justere noe, eller hvis du har spørsmål!

Ha en fin dag,

{{MITT_NAVN}}
{{MIN_TELEFON}}
{{MIN_EPOST}}"""
    
    return template

def calculate_years(established_date):
    """Beregner antall år siden etablering."""
    if not established_date:
        return "flere"
    
    try:
        est_year = int(established_date.split('-')[0])
        current_year = datetime.now().year
        years = current_year - est_year
        return str(years) if years > 0 else "1"
    except:
        return "flere"

def fill_template(template, bedrift, your_info):
    """Fyller ut malen med variabler."""
    filled = template
    
    # Hent adresseinfo
    adresse = bedrift.get("forretningsadresse", {})
    sted = adresse.get("poststed", "")
    
    # Beregn etablerte år
    etablert_ar = calculate_years(bedrift.get("registreringsdato"))
    
    # Erstatt variabler
    filled = filled.replace("{{BEDRIFT_NAVN}}", bedrift.get("navn", ""))
    filled = filled.replace("{{STED}}", sted)
    filled = filled.replace("{{ETABLERT_ÅR}}", etablert_ar)
    filled = filled.replace("{{DEMO_LINK}}", your_info.get("demo_link", ""))
    filled = filled.replace("{{MITT_NAVN}}", your_info.get("navn", ""))
    filled = filled.replace("{{MIN_TELEFON}}", your_info.get("telefon", ""))
    filled = filled.replace("{{MIN_EPOST}}", your_info.get("epost", ""))
    
    return filled

def generate_emails(leads_file, your_info, output_dir):
    """Genererer ferdige e-poster for alle leads med e-post."""
    
    # Last leads
    with open(leads_file, "r", encoding="utf-8") as f:
        leads = json.load(f)
    
    template = load_email_template()
    
    # Lag output-mappe
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated = []
    
    for lead in leads:
        # Sjekk om lead har e-post
        epost = lead.get("epost_manuell") or lead.get("epost")
        
        if not epost or "kundeservice" in epost or "1881" in epost or "thonsenter" in epost:
            # Hopp over hvis ingen ekte e-post
            continue
        
        # Fyll ut mal
        email_body = fill_template(template, lead, your_info)
        
        # Lag filnavn
        bedrift_navn = lead.get("navn", "").replace(" ", "_").replace("/", "-")
        filename = f"email_til_{bedrift_navn}.txt"
        
        # Lagre e-post
        with open(output_dir / filename, "w", encoding="utf-8") as f:
            f.write(f"Til: {epost}\n")
            f.write(f"Emne: Hjemmeside for {lead.get('navn', '')} — et forslag\n")
            f.write("\n" + "="*70 + "\n\n")
            f.write(email_body)
        
        generated.append({
            "bedrift": lead.get("navn"),
            "epost": epost,
            "fil": filename
        })
        
        print(f"✓ Generert e-post til: {lead.get('navn')} ({epost})")
    
    # Lag CSV med alle e-poster
    csv_file = output_dir / "email_liste.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Bedrift", "E-post", "Fil"])
        for g in generated:
            writer.writerow([g["bedrift"], g["epost"], g["fil"]])
    
    print(f"\nGenerert {len(generated)} e-poster")
    print(f"Lagret i: {output_dir}")
    print(f"CSV-liste: {csv_file}")
    
    return generated

def main():
    print("=" * 70)
    print("GENERERER E-POSTER")
    print("=" * 70)
    print()
    
    # Dine opplysninger (endre disse!)
    your_info = {
        "navn": "Trym Johnsen",  # Endre til ditt navn
        "telefon": "123 45 678",  # Endre til ditt telefonnummer
        "epost": "trym@example.com",  # Endre til din e-post
        "demo_link": "https://altaie-hair-hub.vercel.app"  # Endre til din demo
    }
    
    print("Dine opplysninger:")
    for key, value in your_info.items():
        print(f"  {key}: {value}")
    print()
    
    # Fil med leads (må ha ekte e-poster fylt inn)
    leads_file = Path(__file__).parent / "filtered_best_leads_enriched.json"
    
    if not leads_file.exists():
        print(f"Fant ikke {leads_file}")
        print("Du må først finne e-poster og lagre dem i filen!")
        return
    
    output_dir = Path(__file__).parent / "ferdige_emails"
    
    generated = generate_emails(leads_file, your_info, output_dir)
    
    print("\n" + "=" * 70)
    print("FERDIG!")
    print("=" * 70)
    print("\nNeste steg:")
    print("1. Sjekk at opplysningene dine er riktige")
    print("2. Åpne hver .txt-fil i ferdige_emails/")
    print("3. Kopier innholdet og send fra din e-postklient")
    print("4. ELLER bruk en e-posttjeneste som Mailchimp/SendGrid")

if __name__ == "__main__":
    main()
