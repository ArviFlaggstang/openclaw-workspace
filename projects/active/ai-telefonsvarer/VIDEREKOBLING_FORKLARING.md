# Viderekobling - Enkel Forklaring

## 🤔 Hva er viderekobling?

**Vanlig viderekobling:** Når noen ringer ditt nummer, ringer telefonen et ANNET sted.

**Eksempel:**
- Du ringer 12345678 (norsk nummer)
- Det ringer hos bedriften
- Hvis de ikke svarer → ringer det videre til AI

---

## 📞 Vanlige typer viderekobling

### Type 1: "Hvis ikke svar" (MEST BRUKT)

```
Kunde ringer 12345678
        ↓
Bedriftens telefon ringer (f.eks. 10 sekunder)
        ↓
Hvis ingen svarer
        ↓
Viderekobles til AI (f.eks. +44 123 456 789)
        ↓
AI tar imot samtalen
```

**Hva kunden opplever:**
1. Ringer vanlig norsk nummer
2. Hører "ringetone"
3. Hvis ingen svarer → får AI
4. AI svarer på norsk

---

### Type 2: "Alltid viderekoble"

```
Kunde ringer 12345678
        ↓
Direkte til AI (uten å ringe bedriften først)
        ↓
AI tar imot umiddelbart
```

**Brukes når:**
- Etter arbeidstid
- I ferier
- Når alle er opptatt

---

### Type 3: "Etter bestemt tid"

```
Kunde ringer 12345678
        ↓
Ringer hos bedrift (f.eks. 15:00-16:00)
        ↓
Etter kl 16:00 → automatisk til AI
```

**Brukes når:**
- Stengetid
- Lunsjpause
- Helg

---

## 🔧 Hvordan sette opp viderekobling

### Steg 1: Få AI-nummer
1. Kjøp nummer i Retell AI (f.eks. +44 123 456 789)
2. ELLER: Kjøp nummer i Twilio

### Steg 2: Bedriften setter opp viderekobling

**På de fleste telefoner:**
```
*61*[AI-nummer]#  → Hvis ikke svar
*62*[AI-nummer]#  → Hvis opptatt
*21*[AI-nummer]#  → Alltid viderekoble
```

**Eksempel:**
```
*61*+44123456789#   (hvis ikke svar)
*62*+44123456789#   (hvis opptatt)
```

### Steg 3: Test
1. Ring bedriftens norske nummer
2. Ikke svar
3. Se at AI tar over

---

## 💰 Kostnad

| Del | Kostnad |
|-----|---------|
| AI-nummer (Retell/Twilio) | ~$2/mnd |
| Viderekobling fra bedrift | **Gratis** (vanlig tjeneste) |
| Samtale til AI | ~$0.05/min |

**Total:** ~$2/mnd + samtalekostnad

---

## ✅ Fordeler med viderekobling

1. **Kundene ringer vanlig norsk nummer** ✅
2. **Profesjonelt** ✅
3. **Ingen endring for kunder** ✅
4. **Billig** ✅
5. **Enkelt å sette opp** ✅

---

## ❌ Ulemper

1. **Bedriften må gjøre noe** (sette opp viderekobling)
2. **Hvis de glemmer å aktivere** → AI får ikke samtaler
3. **Avhengig av bedriftens telefonsystem**

---

## 🎯 Eksempel: Frisør i Alta

**Før:**
- Kunde ringer 78 43 70 00
- Frisøren er opptatt med kunde
- Ingen svarer
- Kunde legger på → tapt lead

**Med viderekobling:**
- Kunde ringer 78 43 70 00
- Ringer hos frisør (10 sek)
- Ingen svarer
- **Viderekobles til AI**
- AI svarer: "Hei, dette er Alta Kiropraktikk..."
- AI tar imot info
- Frisøren får SMS: "Ny lead: Ola, 12345678, vil bestille time"
- Frisøren ringer tilbake når ledig

---

## 📋 Oppsummering

**Viderekobling =**
- Bedriftens norske nummer ringer først
- Hvis ingen svarer → går til AI
- Kunden opplever én sømløs samtale
- Bedriften får SMS med info

**Enkelt, billig, profesjonelt!**
