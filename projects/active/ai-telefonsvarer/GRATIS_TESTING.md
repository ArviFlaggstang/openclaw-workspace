# Teste AI Resepsjonist UTEN å kjøpe nummer

## ✅ Gratis testing mulig!

### 1. Retell AI - Web Simulator (GRATIS)

**Hva:** Test AI-agenten direkte i nettleseren

**Hvordan:**
1. Logg inn på Retell AI
2. Gå til din agent
3. Klikk "Test" eller "Web Simulator"
4. Skriv meldinger i chat-vinduet
5. AI svarer med stemme!

**Koster:** $0

---

### 2. Retell AI - Demo Call (GRATIS)

**Hva:** Ring en test-samtale fra nettleseren

**Hvordan:**
1. I agent-settings, finn "Demo"
2. Klikk "Start Demo Call"
3. Bruk nettleserens mikrofon
4. Snakk med AI som en vanlig telefonsamtale

**Koster:** $0 (bruker gratis kreditt)

---

### 3. n8n - Lokal testing (GRATIS)

**Hva:** Test webhook og automatisering lokalt

**Hvordan:**
```bash
# Start n8n lokalt
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  n8nio/n8n

# Åpne http://localhost:5678
```

**Test webhook med curl:**
```bash
curl -X POST http://localhost:5678/webhook/lead-capture \
  -H "Content-Type: application/json" \
  -d '{
    "caller_name": "Test Person",
    "caller_phone": "+4799999999",
    "need": "Vil ha tilbud"
  }'
```

**Koster:** $0

---

### 4. Twilio - Trial Account (GRATIS)

**Hva:** Test SMS med gratis trial

**Hvordan:**
1. Registrer på twilio.com/try-twilio
2. Få $15.50 gratis kreditt
3. Få et gratis trial-nummer
4. Send opptil 100 SMS gratis

**Begrensning:**
- Kan kun sende til verifiserte numre (din egen mobil)
- Trial-nummer har begrenset funksjonalitet

**Koster:** $0 (trial)

---

### 5. Google Sheets - Alltid GRATIS

**Hva:** Test lagring av leads

**Hvordan:**
1. Lag ny spreadsheet
2. Del med n8n
3. Se at data kommer inn

**Koster:** $0

---

## 🎯 Full test-flyt UTEN å betale

### Steg 1: Sett opp Retell AI (GRATIS)
- Registrer konto ($10 gratis kreditt)
- Lag agent med norsk prompt
- Test i Web Simulator

### Steg 2: Sett opp n8n lokalt (GRATIS)
```bash
docker run -p 5678:5678 n8nio/n8n
```
- Lag webhook
- Test med curl

### Steg 3: Sett opp Twilio Trial (GRATIS)
- Registrer trial account
- Få gratis nummer
- Verifiser din egen mobil

### Steg 4: Lag Google Sheets (GRATIS)
- Ny spreadsheet
- Del med n8n

### Steg 5: Test ALT sammen (GRATIS)
1. Snakk med AI i Retell Web Simulator
2. Se at webhook trigges i n8n
3. Se at SMS kommer til din mobil
4. Se at Sheets oppdateres

---

## 💰 Når du MÅ betale

| Funksjon | Når du må betale |
|----------|------------------|
| **Eget telefonnummer** | Når du skal i produksjon |
| **Ringe til eksterne numre** | Etter trial-kvoten |
| **Mer enn 100 SMS** | Etter trial-kvoten |
| **Retell AI etter $10** | Når gratis kreditt brukt opp |

---

## 📊 Kostnadsfri test-periode

| Tjeneste | Gratis | Varighet |
|----------|--------|----------|
| Retell AI | $10 kreditt | ~200 minutter |
| Twilio Trial | $15.50 + nummer | ~100 SMS |
| n8n | Ubegrenset | For alltid |
| Google Sheets | Ubegrenset | For alltid |

**Total test-verdi:** ~$25 gratis

---

## 🚀 Anbefalt test-plan

### Uke 1: Gratis testing
- Mandag: Sett opp Retell AI, test i simulator
- Tirsdag: Sett opp n8n lokalt
- Onsdag: Sett opp Twilio trial
- Torsdag: Koble alt sammen
- Fredag: Test full flyt

### Uke 2: Pilot (hvis test OK)
- Kjøp telefonnummer ($2/mnd)
- Sett opp for pilot-kunde
- Gå i produksjon

---

## ✅ Sjekkliste for gratis testing

- [ ] Retell AI konto registrert
- [ ] Agent opprettet og testet i Web Simulator
- [ ] n8n kjører lokalt
- [ ] Webhook mottar data
- [ ] Twilio trial registrert
- [ ] SMS sendes til din mobil
- [ ] Google Sheets oppdateres
- [ ] Full flyt testet OK

---

## 🆘 Hvis noe ikke fungerer

### Retell AI Web Simulator virker ikke
- Sjekk at agenten er "Active"
- Prøv Demo Call isteden
- Sjekk nettleser-mikrofon

### n8n webhook ikke tilgjengelig
- Sjekk at docker kjører: `docker ps`
- Sjekk port 5678: `localhost:5678`
- Prøv `127.0.0.1:5678` istedenfor `localhost`

### Twilio SMS ikke sendt
- Sjekk at nummer er verifisert
- Sjekk at du har kreditt igjen
- Sjekk Twilio logs

---

## 💡 Tips

1. **Bruk trial-perioden maksimalt**
   - Test ALT før du betaler
   - Få erfaring med verktøyene
   - Bygg demo for kunder

2. **Dokumenter underveis**
   - Skriv ned hva som funker
   - Lag skjermbilder
   - Lag video av test

3. **Når du er klar til å betale**
   - Du vet at det fungerer
   - Du har pilot-kunde klar
   - Du har testet alle scenarioer

---

## 🎯 Konklusjon

**JA, du kan teste ALT gratis!**

- Retell AI: $10 gratis
- Twilio: $15.50 + nummer gratis
- n8n: Gratis
- Sheets: Gratis

**Du trenger IKKE betale noe før du skal i produksjon med pilot-kunde!**
