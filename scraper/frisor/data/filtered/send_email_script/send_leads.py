#!/usr/bin/env python3
"""
Script for å sende e-poster og generere Messenger-meldinger til frisør-AS.

Bruker leads.csv med følgende kolonner:
- Navn, Sted, Org.nr, Google-søk, E-post, Telefon, Messenger, bookingsystem

Logikk:
- Har e-post → Send e-post
- Har Messenger (men ikke epost) → Generer melding for manuell sending
- bookingsystem = "nei" → Inkluder booking-tilbud i tekst
"""

import csv
import os
from datetime import datetime

# Konfigurasjon
CSV_FILE = "leads.csv"
OUTPUT_DIR = "output"

# E-postmal
EMAIL_SUBJECT = "Lagde et lite forslag til nettside for {navn}"

EMAIL_TEMPLATE = """Hei {navn},

Jeg kom over {navn} da jeg så etter frisører i {sted}, og la merke til at dere har gode anmeldelser.

Da jeg søkte etter dere fant jeg ingen egen nettside, så jeg lagde en liten demo av hvordan en enkel nettside for {navn} kunne sett ut:

https://frisor-hub.vercel.app/

Den viser blant annet:
• åpningstider og kontaktinfo
• prisoversikt
• online booking
• mobilvennlig design
{booking_pitch}

Jeg studerer datateknologi og lager slike nettsider og små systemer for små bedrifter på fritiden.

Dette er bare et uforpliktende forslag – jeg ville bare vise hva som er mulig for dere.

Gi gjerne en lyd hvis du synes det ser interessant ut, så kan jeg endre på den for dere og tilpasse den med deres logo, bilder og informasjon.

Mvh  
Trym Andreas Johnsen  
+47 915 16 780
"""

# Messenger-melding
MESSENGER_TEMPLATE = """Hei! 👋

Jeg kom over {navn} da jeg så etter frisører i {sted}, og la merke til at dere har gode anmeldelser.

Da jeg søkte etter dere fant jeg ingen egen nettside, så jeg lagde en liten demo av hvordan en enkel nettside for {navn} kunne sett ut:

{demo_link}

{booking_pitch}

Dette er bare et uforpliktende forslag – jeg ville bare vise hva som er mulig.

Hva synes dere om den? 😊

Trym Andreas Johnsen
"""

def ensure_output_dir():
    """Sikrer at output-mappen eksisterer."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def read_leads():
    """Leser CSV-filen og returnerer liste med leads."""
    leads = []
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)
    return leads

def generate_email_text(lead):
    navn = lead['Navn']
    sted = lead['Sted']
    demo_link = lead.get('Demo', 'https://frisor-hub.vercel.app/')

    booking = lead.get('bookingsystem', '').strip().lower()

    if booking == "nei":
        booking_pitch = """• online booking integrert direkte på nettsiden

Slik kan kunder enkelt finne dere på Google og booke time med én gang."""
    
    else:
        booking_pitch = """• tydelig knapp som sender kunder direkte til bookingsiden deres

Da blir det mye enklere for kunder som meg å finne hvor man faktisk booker time."""

    subject = EMAIL_SUBJECT.format(navn=navn)

    body = EMAIL_TEMPLATE.format(
        navn=navn,
        sted=sted,
        demo_link=demo_link,
        booking_pitch=booking_pitch
    )

    return subject, body

def generate_messenger_text(lead):
    navn = lead['Navn']
    sted = lead['Sted']
    demo_link = lead.get('Demo', 'https://frisor-hub.vercel.app/')

    booking = lead.get('bookingsystem', '').strip().lower()

    if booking == "nei":
        booking_pitch = (
            "Den viser blant annet åpningstider, prisoversikt og en enkel online booking "
            "slik at kunder kan booke time direkte. "
            "Hvis dere ikke har dette fra før kan jeg også sette opp noe lignende for dere slik at det blir enklere for kunder å booke."
        )
    else:
        booking_pitch = (
            "Den har blant annet en tydelig knapp som sender kunder direkte til "
            "bookingsiden deres, slik at det blir lettere å finne hvor man booker."
        )

    return MESSENGER_TEMPLATE.format(
        navn=navn,
        sted=sted,
        demo_link=demo_link,
        booking_pitch=booking_pitch
    )



def save_draft(lead, subject, body, channel):
    """Lagrer utkast til fil."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    navn = lead['Navn'].replace(' ', '_').replace('/', '_')
    filename = f"{OUTPUT_DIR}/{channel}_{navn}_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Til: {lead.get('E-post', 'N/A') if channel == 'email' else 'Messenger'}\n")
        f.write(f"Bedrift: {lead['Navn']}\n")
        f.write(f"Sted: {lead['Sted']}\n")
        f.write(f"Kanal: {channel}\n")
        f.write(f"{'='*50}\n\n")
        if subject:
            f.write(f"Emne: {subject}\n\n")
        f.write(body)
    
    return filename

def process_leads(send_emails=False):
    """
    Prosesserer alle leads.
    
    Args:
        send_emails: Hvis True, prøver å sende e-poster. Hvis False, lagrer kun utkast.
    """
    ensure_output_dir()
    leads = read_leads()
    
    stats = {
        'email_sent': 0,
        'email_draft': 0,
        'messenger_draft': 0,
        'skipped': 0,
        'errors': []
    }
    
    print(f"Prosesserer {len(leads)} leads...\n")
    
    for lead in leads:
        navn = lead['Navn']
        epost = lead.get('E-post', '').strip()
        messenger = lead.get('Messenger', '').strip().lower()
        
        # Prioritet 1: Har e-post
        if epost and '@' in epost:
            subject, body = generate_email_text(lead)
            
            if send_emails and SENDER_PASSWORD:
                success, msg = send_email(epost, subject, body)
                if success:
                    print(f"✉️  E-post sendt til: {navn} ({epost})")
                    stats['email_sent'] += 1
                else:
                    print(f"❌ Feil ved sending til {navn}: {msg}")
                    stats['errors'].append(f"{navn}: {msg}")
                    # Lagre som utkast ved feil
                    filename = save_draft(lead, subject, body, 'email')
                    stats['email_draft'] += 1
            else:
                filename = save_draft(lead, subject, body, 'email')
                print(f"📝 E-post utkast lagret: {navn}")
                stats['email_draft'] += 1
        
        # Prioritet 2: Har Messenger (men ikke epost)
        elif messenger == 'ja':
            body = generate_messenger_text(lead)
            filename = save_draft(lead, None, body, 'messenger')
            print(f"💬 Messenger utkast lagret: {navn}")
            stats['messenger_draft'] += 1
        
        else:
            print(f"⏭️  Hoppet over: {navn} (ingen kontaktinfo)")
            stats['skipped'] += 1
    
    # Print statistikk
    print(f"\n{'='*50}")
    print("OPPSUMMERING:")
    print(f"  E-poster sendt:     {stats['email_sent']}")
    print(f"  E-post utkast:      {stats['email_draft']}")
    print(f"  Messenger utkast:   {stats['messenger_draft']}")
    print(f"  Hoppet over:        {stats['skipped']}")
    
    if stats['errors']:
        print(f"\nFeil:")
        for error in stats['errors']:
            print(f"  - {error}")
    
    print(f"\nUtkast lagret i: {OUTPUT_DIR}/")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Send e-poster og generer Messenger-meldinger til frisører')
    parser.add_argument('--send', action='store_true', help='Faktisk send e-poster (krever miljøvariabler)')
    parser.add_argument('--dry-run', action='store_true', default=True, help='Kun generer utkast (default)')
    
    args = parser.parse_args()
    
    # Sjekk at CSV-filen finnes
    if not os.path.exists(CSV_FILE):
        print(f"Feil: Fant ikke {CSV_FILE}")
        print("Sørg for at filen er i samme mappe som scriptet.")
        exit(1)
    
    process_leads(send_emails=args.send)
