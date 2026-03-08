# AI Resepsjonist - Komplett Oppsett Guide

## 🎯 Mål
Bygge en AI-telefonsvarer som:
1. Svarer telefonen 24/7 på norsk
2. Tar imot navn, telefon, behov
3. Sender SMS til bedriftseier
4. Lagrer leads i database

---

## 🔧 Del 1: Retell AI (Stemme & Samtale)

### Steg 1.1: Registrer konto
1. Gå til https://www.retellai.com
2. Registrer med GitHub/e-post
3. Verifiser e-post

### Steg 1.2: Lag ny Agent
1. Klikk "Create Agent"
2. Velg "Single Prompt Agent"
3. Navn: "AI Resepsjonist - [Bedriftsnavn]"

### Steg 1.3: Konfigurer språk
```
Language: Norwegian (nb-NO)
TTS Provider: ElevenLabs
Voice: Leland (eller annen norsk)
```

### Steg 1.4: Skriv prompt
```
Du er en hjelpsom og vennlig AI-assistent for [BEDRIFTSNAVN].

OPPGAVE:
- Ta imot telefonsamtaler fra kunder
- Hjelpe med timebestilling og spørsmål
- Være profesjonell og effektiv

VIKTIG INFO:
- Åpningstider: [Fyll inn]
- Adresse: [Fyll inn]
- Telefon: [Fyll inn]
- Tjenester: [Fyll inn]

SAMTALE-FLYT:
1. Hils: "Hei, dette er [BEDRIFT]. Jeg er en digital assistent. Hva kan jeg hjelpe deg med?"
2. Lytt til hva kunden trenger
3. Be om: navn, telefonnummer, hva det gjelder
4. Bekreft: "Takk! Jeg sender info til [EIER] som ringer deg tilbake snart."
5. Avslutt hyggelig

REGLER:
- Snakk norsk
- Ikke gi medisinske/tekniske råd
- Aldri bekreft timer direkte - si at eier ringer tilbake
- Vær høflig og tålmodig
```

### Steg 1.5: Test agenten
1. Klikk "Test" i Retell AI
2. Skriv: "Hei, jeg vil bestille time"
3. Se at AI svarer riktig

---

## 🔧 Del 2: Telefonnummer

### Steg 2.1: Kjøp nummer i Retell
1. Gå til "Phone Numbers"
2. Klikk "+ Add"
3. Velg "Buy Number"
4. Velg norsk nummer (hvis tilgjengelig) ELLER internasjonalt
5. Koble til agenten

### Steg 2.2: Alternativ - BYON (Bring Your Own Number)
Hvis bedriften har eget nummer:
1. Be bedriften om å viderekoble til Retell-nummeret
2. ELLER portere nummeret til Retell (tar 4 uker)

---

## 🔧 Del 3: n8n (Automatisering & SMS)

### Steg 3.1: Installer n8n
```bash
# Med Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# Åpne http://localhost:5678
```

### Steg 3.2: Lag ny workflow
1. Klikk "Add Workflow"
2. Navn: "AI Resepsjonist - Lead Capture"

### Steg 3.3: Webhook-trigger
1. Legg til "Webhook" node
2. Method: POST
3. Path: `lead-capture`
4. Kopier webhook URL (f.eks. `https://din-n8n.com/webhook/lead-capture`)

### Steg 3.4: Koble Retell til n8n
I Retell AI:
1. Gå til agent settings
2. Finn "Webhook" eller "Post-call webhook"
3. Lim inn n8n webhook URL
4. Velg å sende: transcript, caller_info, etc.

### Steg 3.5: Prosesser data
I n8n workflow:

**Node 1: Webhook (mottar data)**
```json
{
  "caller_phone": "+4791234567",
  "caller_name": "Ola Nordmann",
  "need": "Vil bestille time til rørlegger",
  "timestamp": "2026-03-07T10:00:00Z"
}
```

**Node 2: Set (formater data)**
```javascript
// Formater data for SMS
return {
  json: {
    message: `Ny lead!\nNavn: ${$json.caller_name}\nTlf: ${$json.caller_phone}\nBehov: ${$json.need}\nTid: ${$json.timestamp}`
  }
}
```

**Node 3: Twilio (send SMS)**
- Account SID: [Fra Twilio]
- Auth Token: [Fra Twilio]
- From: [Ditt Twilio-nummer]
- To: [Bedriftseiers mobil]
- Body: `{{$json.message}}`

**Node 4: Google Sheets (lagre lead)**
- Spreadsheet: "AI Resepsjonist Leads"
- Sheet: "Leads"
- Columns: Timestamp, Navn, Telefon, Behov, Status

---

## 🔧 Del 4: Twilio (SMS)

### Steg 4.1: Registrer Twilio
1. Gå til https://www.twilio.com
2. Registrer konto
3. Verifiser telefonnummer

### Steg 4.2: Kjøp nummer
1. Gå til "Phone Numbers" → "Manage"
2. Klikk "Buy a number"
3. Velg norsk nummer (hvis tilgjengelig) ELLER US/UK nummer
4. Noter SID og telefonnummer

### Steg 4.3: Hent credentials
1. Gå til "Account" → "API keys & tokens"
2. Kopier:
   - Account SID (starter med AC...)
   - Auth Token

### Steg 4.4: Legg til i n8n
1. I n8n: Settings → Credentials
2. "Add Credential" → Twilio
3. Lim inn SID og Auth Token

---

## 🔧 Del 5: Google Sheets (Database)

### Steg 5.1: Opprett spreadsheet
1. Gå til https://sheets.google.com
2. Lag ny spreadsheet: "AI Resepsjonist Leads"
3. Første rad (headers):
   - A: Timestamp
   - B: Navn
   - C: Telefon
   - D: Behov
   - E: Status
   - F: Notater

### Steg 5.2: Del med n8n
1. Klikk "Share"
2. Legg til: n8n-service-account@... (eller bruk OAuth)
3. Gi "Editor" tilgang

### Steg 5.3: Kopier Spreadsheet ID
URL: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`
Kopier SPREADSHEET_ID

---

## 🔧 Del 6: Testing

### Steg 6.1: Test webhook
```bash
curl -X POST https://din-n8n.com/webhook/lead-capture \
  -H "Content-Type: application/json" \
  -d '{
    "caller_name": "Test Person",
    "caller_phone": "+4799999999",
    "need": "Vil ha tilbud på nytt bad"
  }'
```

### Steg 6.2: Sjekk SMS
- Mottok bedriftseier SMS?
- Er formatet riktig?

### Steg 6.3: Sjekk Google Sheets
- Ble rad lagt til?
- Er alle felter fylt ut?

### Steg 6.4: Test full flyt
1. Ring Retell AI-nummeret
2. Snakk med AI
3. Legg på
4. Vent 10-30 sekunder
5. Sjekk at SMS kommer
6. Sjekk at Sheets er oppdatert

---

## 🔧 Del 7: Produksjon

### Steg 7.1: Dokumenter alt
- Lag README for bedriften
- Skriv hvordan det fungerer
- Lag troubleshoot-guide

### Steg 7.2: Overlevering til kunde
1. Gi tilgang til Google Sheets
2. Vis hvordan de ser leads
3. forklar SMS-varsling
4. Gi kontaktinfo for support

### Steg 7.3: Overvåking
- Sjekk n8n logs daglig første uken
- Følg med på Twilio-kostnader
- Spør kunde om feedback

---

## 💰 Kostnadsoversikt

| Tjeneste | Kostnad |
|----------|---------|
| Retell AI | $10 gratis, deretter ~$0.05/min |
| Twilio nummer | $1.15/mnd |
| Twilio SMS | $0.0651 per melding |
| n8n (self-hosted) | Gratis |
| Google Sheets | Gratis |
| **TOTALT** | ~$2-10/mnd + bruk |

---

## 📋 Sjekkliste før lansering

- [ ] Retell AI agent testet og fungerer
- [ ] Telefonnummer kjøpt og koblet
- [ ] n8n webhook mottar data
- [ ] Twilio SMS sendes riktig
- [ ] Google Sheets oppdateres
- [ ] Full test av hele flyten OK
- [ ] Dokumentasjon klar
- [ ] Kunde informert

---

## 🆘 Feilsøking

### Problem: AI svarer ikke
- Sjekk at agenten er "Active"
- Sjekk at nummer er koblet
- Test i Retell AI dashboard

### Problem: Webhook mottar ikke data
- Sjekk at URL er riktig
- Sjekk at Retell webhook er aktivert
- Test med curl

### Problem: SMS sendes ikke
- Sjekk Twilio credentials
- Sjekk at telefonnummer er verifisert
- Sjekk Twilio logs

### Problem: Sheets ikke oppdatert
- Sjekk at spreadsheet er delt
- Sjekk at ID er riktig
- Sjekk n8n error logs

---

## 🚀 Neste steg

1. Start med Retell AI (steg 1)
2. Når det fungerer, gå til n8n (steg 3)
3. Deretter Twilio (steg 4)
4. Til slutt testing (steg 6)

**Ta én del om gangen!**
