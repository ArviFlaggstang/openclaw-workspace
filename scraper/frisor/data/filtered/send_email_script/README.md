# Oppsett for Send Script

## 1. Sett miljøvariabler

I terminalen, før du kjører scriptet:

```bash
export SMTP_USER="din@gmail.com"
export SMTP_PASS="ditt_app_passord"  # Se nedenfor for hvordan lage
```

## 2. Lag App-passord for Gmail

Gmail krever "App Password" (ikke dvanlig passord):

1. Gå til https://myaccount.google.com/
2. Sikkerhet → 2-trinnsbekreftelse (må være på)
3. Sikkerhet → App-passord
4. Velg "Mail" og "Annen (egendefinert navn)"
5. Skriv "Frisor Script" → Generer
6. Kopier passordet (16 tegn)

## 3. Fyll inn ekte e-poster

Åpne `leads.csv` og erstatt `@epost.mangler` med ekte e-poster:

```csv
email,business_name,city,owner_name,demo_link,status,first_sent_at,followup_sent_at
awad@frisor.no,AWAD FRISØR,Trondheim,,https://frisor-hub.vercel.app,pending,,
```

## 4. Kjør scriptet

```bash
cd scraper/frisor/data/filtered/send_email_script
python3 send_script.py
```

## 5. Hva skjer?

- Scriptet sender til alle med `status=pending`
- Oppdaterer `first_sent_at` med tidspunkt
- Etter 3 dager: sender oppfølging til de med `status=sent` og ingen `followup_sent_at`
- Maks 40 e-poster per kjøring

## Viktig

- **Test først:** Send til din egen e-post
- **Start smått:** 5-10 e-poster første gang
- **Respekter grenser:** Gmail har daglige sending-grenser
- **Unsubscribe:** Inkluder måte å melde seg av (Forbrukertilsynet)

## Feilsøking

Hvis du får feil:
- Sjekk at SMTP_USER og SMTP_PASS er satt
- Sjekk at leads.csv finnes
- Sjekk at du bruker App-passord (ikke vanlig Gmail-passord)
