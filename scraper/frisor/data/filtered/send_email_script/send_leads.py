#!/usr/bin/env python3
"""
Script for å generere e-postutkast og Messenger-meldinger til frisørsalonger.

Bruker leads.csv med følgende kolonner:
- Navn, Sted, Org.nr, Google-søk, E-post, Telefon, Messenger, bookingsystem

Logikk:
- Har e-post -> lag e-postutkast
- Har Messenger = ja -> lag Messenger-utkast
- Hvis en bedrift har begge deler -> lag begge utkast
- bookingsystem = "nei" -> tilby nettside + booking
- bookingsystem != "nei" -> tilby nettside som gjør det enklere å finne booking

Ingen meldinger sendes automatisk.
Alle utkast lagres som .txt-filer i output-mappen.
"""

import csv
import os
from datetime import datetime

# Konfigurasjon
CSV_FILE = "leads.csv"
OUTPUT_DIR = "output"
DEFAULT_DEMO_LINK = "https://frisor-hub.vercel.app/"

# E-postmal
EMAIL_SUBJECT = "Lagde et lite forslag til nettside for {navn}"

EMAIL_TEMPLATE = """Hei {navn},

Jeg kom over {navn} da jeg så etter frisører i {sted}, og la merke til at dere har gode anmeldelser.

Da jeg søkte etter dere fant jeg ingen egen nettside, så jeg lagde en liten demo av hvordan en enkel nettside for {navn} kunne sett ut:

{demo_link}

Den viser blant annet:
• åpningstider og kontaktinfo
• prisoversikt
• mobilvennlig design
{booking_pitch}

Jeg studerer datateknologi og lager slike nettsider og små systemer for små bedrifter på fritiden.

Dette er bare et uforpliktende forslag – jeg ville bare vise hva som er mulig for dere.

Gi gjerne en lyd hvis du synes det ser interessant ut, så kan jeg tilpasse den med deres logo, bilder og informasjon.

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



def clean_company_name(name):
    """Fjerner AS og gjør navnet mer naturlig."""
    
    name = name.strip()

    # fjern AS på slutten
    if name.upper().endswith(" AS"):
        name = name[:-3]

    # gjør til normal casing
    name = name.title()

    return name



def ensure_output_dir():
    """Sikrer at output-mappen eksisterer."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def read_leads():
    """Leser CSV-filen og returnerer en liste med leads."""
    leads = []

    with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            raise ValueError("CSV-filen ser ut til å mangle kolonneoverskrifter.")

        # Fjern eventuelle skjulte mellomrom i kolonnenavn
        reader.fieldnames = [field.strip() for field in reader.fieldnames]

        for row in reader:
            clean_row = {}
            for key, value in row.items():
                clean_key = key.strip() if key else ""
                clean_value = value.strip() if value else ""
                clean_row[clean_key] = clean_value
            leads.append(clean_row)

    return leads


def get_demo_link(lead):
    """Henter demo-link fra CSV hvis den finnes, ellers standardlink."""
    return lead.get("Demo", "").strip() or DEFAULT_DEMO_LINK


def get_email_booking_pitch(booking_value):
    """Genererer booking-tekst for e-post."""
    booking = booking_value.strip().lower()

    if booking == "nei":
        return """• online booking integrert direkte på nettsiden

Slik kan kunder enkelt finne dere på Google og booke time med én gang."""
    return """• tydelig knapp som sender kunder direkte til bookingsiden deres

Da blir det mye enklere for kunder som meg å finne hvor man faktisk booker time."""


def get_messenger_booking_pitch(booking_value):
    """Genererer booking-tekst for Messenger."""
    booking = booking_value.strip().lower()

    if booking == "nei":
        return (
            "Den viser blant annet åpningstider, prisoversikt og en enkel online booking "
            "slik at kunder kan booke time direkte. "
            "Hvis dere ikke har dette fra før kan jeg også sette opp noe lignende for dere "
            "slik at det blir enklere for kunder å booke."
        )
    return (
        "Den har blant annet en tydelig knapp som sender kunder direkte til bookingsiden deres, "
        "slik at det blir lettere å finne hvor man booker."
    )


def generate_email_text(lead):
    """Genererer emne og e-posttekst for ett lead."""
    navn = clean_company_name(lead["Navn"])
    sted = lead["Sted"].title()
    demo_link = get_demo_link(lead)
    booking_pitch = get_email_booking_pitch(lead.get("bookingsystem", ""))

    subject = EMAIL_SUBJECT.format(navn=navn)
    body = EMAIL_TEMPLATE.format(
        navn=navn,
        sted=sted,
        demo_link=demo_link,
        booking_pitch=booking_pitch,
    )

    return subject, body


def generate_messenger_text(lead):
    """Genererer Messenger-melding for ett lead."""
    navn = clean_company_name(lead["Navn"])
    sted = lead["Sted"].title()
    demo_link = get_demo_link(lead)
    booking_pitch = get_messenger_booking_pitch(lead.get("bookingsystem", ""))

    return MESSENGER_TEMPLATE.format(
        navn=navn,
        sted=sted,
        demo_link=demo_link,
        booking_pitch=booking_pitch,
    )


def sanitize_filename(text):
    """Gjør tekst trygg å bruke i filnavn."""
    safe = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in text.strip())
    return safe.strip("_") or "ukjent"


def save_draft(lead, subject, body, channel):
    """Lagrer utkast til tekstfil."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    safe_name = sanitize_filename(lead.get("Navn", "ukjent"))

    filename = os.path.join(OUTPUT_DIR, f"{channel}_{safe_name}_{timestamp}.txt")

    with open(filename, "w", encoding="utf-8") as f:
        if channel == "email":
            recipient = lead.get("E-post", "N/A")
        else:
            recipient = "Facebook Messenger"

        f.write(f"Til: {recipient}\n")
        f.write(f"Bedrift: {lead.get('Navn', 'N/A')}\n")
        f.write(f"Sted: {lead.get('Sted', 'N/A')}\n")
        f.write(f"Kanal: {channel}\n")
        f.write("=" * 50 + "\n\n")

        if subject:
            f.write(f"Emne: {subject}\n\n")

        f.write(body)

    return filename


def process_leads():
    """Prosesserer alle leads og lagrer utkast i output-mappen."""
    ensure_output_dir()
    leads = read_leads()

    stats = {
        "email_draft": 0,
        "messenger_draft": 0,
        "skipped": 0,
        "errors": [],
    }

    print(f"Prosesserer {len(leads)} leads...\n")

    for index, lead in enumerate(leads, start=1):
        try:
            navn = lead.get("Navn", "").strip()
            sted = lead.get("Sted", "").strip()
            epost = lead.get("E-post", "").strip()
            messenger = lead.get("Messenger", "").strip().lower()

            if not navn or not sted:
                msg = f"Rad {index}: mangler Navn eller Sted"
                print(f"❌ {msg}")
                stats["errors"].append(msg)
                continue

            created_any = False

            if epost and "@" in epost:
                subject, body = generate_email_text(lead)
                save_draft(lead, subject, body, "email")
                print(f"📝 E-postutkast lagret: {navn}")
                stats["email_draft"] += 1
                created_any = True

            if messenger == "ja":
                body = generate_messenger_text(lead)
                save_draft(lead, None, body, "messenger")
                print(f"💬 Messenger-utkast lagret: {navn}")
                stats["messenger_draft"] += 1
                created_any = True

            if not created_any:
                print(f"⏭️  Hoppet over: {navn} (ingen brukbar kontaktinfo)")
                stats["skipped"] += 1

        except KeyError as e:
            msg = f"Rad {index}: mangler kolonnen {e}"
            print(f"❌ {msg}")
            stats["errors"].append(msg)
        except Exception as e:
            msg = f"Rad {index} ({lead.get('Navn', 'ukjent')}): {e}"
            print(f"❌ Feil: {msg}")
            stats["errors"].append(msg)

    print("\n" + "=" * 50)
    print("OPPSUMMERING:")
    print(f"  E-postutkast:      {stats['email_draft']}")
    print(f"  Messenger-utkast:  {stats['messenger_draft']}")
    print(f"  Hoppet over:       {stats['skipped']}")

    if stats["errors"]:
        print("\nFeil:")
        for error in stats["errors"]:
            print(f"  - {error}")

    print(f"\nUtkast lagret i: {OUTPUT_DIR}/")


if __name__ == "__main__":
    if not os.path.exists(CSV_FILE):
        print(f"Feil: Fant ikke {CSV_FILE}")
        print("Sørg for at filen er i samme mappe som scriptet.")
        raise SystemExit(1)

    process_leads()
