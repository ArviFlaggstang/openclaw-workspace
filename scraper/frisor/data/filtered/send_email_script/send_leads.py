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
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Konfigurasjon
CSV_FILE = "leads.csv"
OUTPUT_DIR = "output"
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "din@epost.no")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

# E-postmal
EMAIL_SUBJECT = "Hei {navn} – vi hjelper frisører med digital tilstedeværelse"

EMAIL_TEMPLATE = """Hei {navn}!

Jeg håper du har en fin dag i {sted}.

Jeg kontakter deg fordi jeg ser at {navn} er en etablert frisørsalong, og jeg lurte på om dere har behov for hjelp med digital markedsføring eller nettside?

Vi spesialiserer oss på å hjelpe små bedrifter som frisørsalonger med:
• Profesjonell nettside som viser frem deres arbeid
• Booking-system integrert på nettsiden{booking_tekst}
• Google Business-optimalisering for flere lokale kunder

Dette er en uforpliktende henvendelse – jeg vil gjerne høre om dette er noe dere kunne vært interessert i.

Har du 10 minutter til en uforpliktende prat i løpet av uken?

Med vennlig hilsen,
[Navnet ditt]
[Tlf]
"""

# Messenger-melding
MESSENGER_TEMPLATE = """Hei! 👋

Jeg ser at {navn} i {sted} er en flott frisørsalong. 

Jeg hjelper frisører med digital tilstedeværelse – nettsider, booking-system{booking_tekst} og Google-optimalisering.

Er dette noe dere kunne tenke dere å høre mer om? 😊

[Navnet ditt]
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
    """Genererer e-posttekst for et lead."""
    navn = lead['Navn']
    sted = lead['Sted']
    
    # Sjekk om de mangler booking-system
    if lead.get('bookingsystem', '').strip().lower() == 'nei':
        booking_tekst = "\n• Enkelt online booking-system (ser dere ikke har dette ennå)"
    else:
        booking_tekst = ""
    
    subject = EMAIL_SUBJECT.format(navn=navn)
    body = EMAIL_TEMPLATE.format(
        navn=navn,
        sted=sted,
        booking_tekst=booking_tekst
    )
    
    return subject, body

def generate_messenger_text(lead):
    """Genererer Messenger-melding for et lead."""
    navn = lead['Navn']
    sted = lead['Sted']
    
    # Sjekk om de mangler booking-system
    if lead.get('bookingsystem', '').strip().lower() == 'nei':
        booking_tekst = " (inkludert booking-løsning)"
    else:
        booking_tekst = ""
    
    return MESSENGER_TEMPLATE.format(
        navn=navn,
        sted=sted,
        booking_tekst=booking_tekst
    )

def send_email(to_email, subject, body):
    """Sender e-post via SMTP."""
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True, "Sendt"
    except Exception as e:
        return False, str(e)

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
