# n8n Workflows - Lokalt Klonet

## 📁 Lokasjon
`~/.openclaw/workspace/n8n-workflows-reference/`

## 📊 Størrelse
- **83 MB** totalt
- **188+ workflow-mapper**
- **4,343+ workflows**

---

## 🎯 Mest relevante for AI-resepsjonist

### 1. Twilio (Telefoni & SMS)
**Mappe:** `workflows/Twilio/`

| Fil | Hva den gjør |
|-----|--------------|
| `0354_Twilio_Typeform_Send_Triggered.json` | Sender Typeform-leads via WhatsApp/Twilio |
| `0841_Twilio_Stickynote_Send_Triggered.json` | Twilio + notater |
| `0842_Twilio_Cron_Send_Scheduled.json` | Planlagte Twilio-sendinger |
| `1198_Twilio_Pushcut_Send_Triggered.json` | Twilio + Pushcut integrasjon |

**Verdi for oss:**
- ✅ Se hvordan Twilio SMS settes opp
- ✅ Lære webhook-triggere
- ✅ Forstå credentials-håndtering

---

### 2. OpenAI (AI & Automatisering)
**Mappe:** `workflows/Openai/`

| Fil | Hva den gjør |
|-----|--------------|
| `0248_Openai_Telegram_Automate_Triggered.json` | AI-chatbot i Telegram |
| `0334_Openai_Form_Create_Triggered.json` | AI prosesserer skjemaer |
| `0464_Openai_Form_Create_Webhook.json` | AI via webhook |
| `1177_Openai_GoogleSheets_Create_Triggered.json` | AI + Google Sheets |
| `1256_Openai_Form_Automation_Triggered.json` | AI skjemabehandling |
| `1618_Openai_GoogleSheets_Create_Triggered.json` | AI + Sheets (variant) |
| `1685_Openai_Telegram_Automate_Triggered.json` | AI + Telegram (variant) |

**Verdi for oss:**
- ✅ Se hvordan OpenAI integreres
- ✅ Lære prompt-engineering i n8n
- ✅ Forstå AI + database flyt

---

### 3. Google Calendar (Booking)
**Mappe:** `workflows/Googlecalendar/`

**Verdi for oss:**
- ✅ Automatisk timebestilling
- ✅ Sjekke ledig tid
- ✅ Opprette avtaler

---

### 4. Webhook (Triggere)
**Mappe:** `workflows/Webhook/`

**Verdi for oss:**
- ✅ Motta data fra Retell AI
- ✅ Trigge workflows eksternt
- ✅ Integrere med andre systemer

---

### 5. Airtable / Google Sheets (Database)
**Mapper:** `workflows/Airtable/`, `workflows/Googlesheets/`

**Verdi for oss:**
- ✅ Lagre leads
- ✅ Logge samtaler
- ✅ Rapportering

---

## 🚀 Hvordan bruke

### 1. Kopiere workflow:
```bash
cp ~/.openclaw/workspace/n8n-workflows-reference/workflows/Twilio/0354_Twilio_Typeform_Send_Triggered.json \
   ~/min-workflow.json
```

### 2. Importere i n8n:
1. Åpne n8n UI (http://localhost:5678)
2. Settings → Import
3. Velg JSON-filen
4. Tilpass credentials

### 3. Modifisere:
- Endre telefonnummer
- Legg til egne prompts
- Koble til egne databaser

---

## 💡 Neste steg

### For AI-resepsjonist:

1. **Studere Twilio-workflows**
   - Forstå SMS-oppsett
   - Se på webhook-håndtering

2. **Studere OpenAI-workflows**
   - Lære AI-integrasjon
   - Se på prompt-struktur

3. **Bygge vår egen**
   - Kombinere Twilio + OpenAI
   - Legge til Google Calendar
   - Koble til Airtable/Sheets

---

## 📚 Ressurser

- **Repo:** https://github.com/Zie619/n8n-workflows
- **Lokalt:** `~/.openclaw/workspace/n8n-workflows-reference/`
- **Dokumentasjon:** Se `docs/` mappen

---

*Klonet: 2026-03-07*
*Størrelse: 83 MB*
*Workflows: 4,343+*
