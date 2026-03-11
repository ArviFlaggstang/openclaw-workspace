#!/usr/bin/env python3
"""Test-script for å se eksempler på genererte meldinger."""

import csv

def read_leads():
    with open("leads.csv", 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def show_examples():
    leads = read_leads()
    
    print("="*60)
    print("EKSEMPEL: E-post til bedrift med e-post OG mangler booking")
    print("="*60)
    for lead in leads:
        if lead.get('E-post', '').strip() and lead.get('bookingsystem', '').strip() == 'nei':
            print(f"\nBedrift: {lead['Navn']} i {lead['Sted']}")
            print(f"E-post: {lead['E-post']}")
            print(f"Booking: {lead.get('bookingsystem', 'ikke satt')}")
            print("\n--- GENERERT E-POST ---")
            
            subject = f"Hei {lead['Navn']} – vi hjelper frisører med digital tilstedeværelse"
            body = f"""Hei {lead['Navn']}!

Jeg håper du har en fin dag i {lead['Sted']}.

Jeg kontakter deg fordi jeg ser at {lead['Navn']} er en etablert frisørsalong, og jeg lurte på om dere har behov for hjelp med digital markedsføring eller nettside?

Vi spesialiserer oss på å hjelpe små bedrifter som frisørsalonger med:
• Profesjonell nettside som viser frem deres arbeid
• Booking-system integrert på nettsiden
• Enkelt online booking-system (ser dere ikke har dette ennå)
• Google Business-optimalisering for flere lokale kunder

Dette er en uforpliktende henvendelse – jeg vil gjerne høre om dette er noe dere kunne vært interessert i.

Har du 10 minutter til en uforpliktende prat i løpet av uken?

Med vennlig hilsen,
[Navnet ditt]
[Tlf]"""
            print(f"Emne: {subject}")
            print(body)
            break
    
    print("\n" + "="*60)
    print("EKSEMPEL: Messenger-melding til bedrift med Messenger")
    print("="*60)
    for lead in leads:
        if lead.get('Messenger', '').strip().lower() == 'ja' and not lead.get('E-post', '').strip():
            print(f"\nBedrift: {lead['Navn']} i {lead['Sted']}")
            print(f"Messenger: ja")
            print("\n--- GENERERT MELDING ---")
            
            msg = f"""Hei! 👋

Jeg ser at {lead['Navn']} i {lead['Sted']} er en flott frisørsalong. 

Jeg hjelper frisører med digital tilstedeværelse – nettsider, booking-system og Google-optimalisering.

Er dette noe dere kunne tenke dere å høre mer om? 😊

[Navnet ditt]"""
            print(msg)
            break
    
    print("\n" + "="*60)
    print("STATISTIKK")
    print("="*60)
    
    with_email = sum(1 for l in leads if l.get('E-post', '').strip())
    with_messenger = sum(1 for l in leads if l.get('Messenger', '').strip().lower() == 'ja')
    without_booking = sum(1 for l in leads if l.get('bookingsystem', '').strip().lower() == 'nei')
    
    print(f"Totalt antall leads: {len(leads)}")
    print(f"Med e-post: {with_email}")
    print(f"Med Messenger: {with_messenger}")
    print(f"Uten booking-system: {without_booking}")

if __name__ == "__main__":
    show_examples()
