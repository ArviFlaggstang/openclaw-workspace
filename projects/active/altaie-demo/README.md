# Altaie Frisør - Booking System

## Demo for Mohammed (møtet i påsken)

Denne mappen inneholder en **fullt fungerende demo** av nettsiden med booking-system som du kan vise Mohammed.

---

## Hva du skal vise Mohammed

### 1. Åpne demo-filen
```bash
cd demo/booking-form
python3 -m http.server 8000
```

Åpne nettleseren på `http://localhost:8000`

### 2. Gå gjennom flyten sammen med Mohammed:

**Steg 1:** Kunde velger tjeneste  
**Steg 2:** Kunde velger dato  
**Steg 3:** Kunde velger tid  
**Steg 4:** Kunde fyller inn navn og telefon  
**Steg 5:** Kunde fullfører i SimplyBook (vises i iframe)

### 3. Kalkulasjonen (viktig!)

> "Mohammed, du sa du bruker 20 minutter på telefonen hver dag med bookinger. Det er **600 minutter i måneden** — nesten **10 timer**, eller én hel arbeidsdag! Med dette systemet booker kundene selv, og du får bare en SMS-beskjed."

---

## Teknisk oppsett (etter salg)

### Steg 1: Registrer SimplyBook-konto for Mohammed

1. Gå til https://simplybook.me
2. Registrer konto med:
   - Bedriftsnavn: Altaie Frisør
   - URL: `altaiefrisor.simplybook.me`
   - E-post: Mohammeds e-post
3. Velg "Beauty and Personal Care" som bransje
4. Fullfør registreringen

### Steg 2: Konfigurer tjenester

I SimplyBook admin-panel:

```
Tjenester → Legg til ny:
- Herreklipp (30 min, 350 kr)
- Dameklipp (45 min, 450 kr)
- Barnklipp (20 min, 250 kr)
- Farging (90 min, 800 kr)
- Striper (120 min, 1200 kr)
- Barbering (15 min, 200 kr)
```

### Steg 3: Sett åpningstider

```
Innstillingene → Åpningstider:
- Mandag-fredag: 09:00-17:00
- Lørdag: 10:00-14:00
- Søndag: Stengt
```

### Steg 4: Integrer i nettsiden

Bytt ut mock-URL i `index.html`:

```javascript
// FRA (demo):
const mockUrl = `https://simplybook.me/v2/?...`;

// TIL (produksjon):
const simplybookUrl = `https://altaiefrisor.simplybook.me/v2/?
    service=${service}&
    date=${date}&
    provider=1&
    staff=1`;
```

### Steg 5: SMS-varsler (valgfritt)

SimplyBook kan sende SMS:
- Kunden får påminnelse 24t før
- Mohammed får beskjed ved ny booking

Kostnad: ~0.50 kr per SMS

---

## Gjenbruk for andre kunder

Dette systemet kan enkelt gjenbrukes:

### 1. Kopier `src/booking-widget/`

```bash
cp -r src/booking-widget ../andre-kunde/src/
```

### 2. Endre config

```javascript
// simplybook-config.js
widgetUrl: 'https://[NY-KUNDE].simplybook.me/v2/',
services: [
  // Tilpass tjenester
]
```

### 3. Tilpass farger

```css
:root {
  --primary-color: #NY-FARGE;
  --secondary-color: #NY-FARGE;
}
```

---

## Pris til Mohammed

| Post | Beløp |
|------|-------|
| Nettside med booking | 15 000 kr |
| SimplyBook (Standard) | ~199 kr/mnd (han betaler selv) |
| Drift (hosting) | 500 kr/mnd |
| **Din månedlige inntekt** | **500 kr/mnd** |

**Total inntekt:** 15 000 kr + 500 kr/mnd

---

## Fordeler for Mohammed

| Før | Etter |
|-----|-------|
| 20 min telefon per dag | Kunder booker selv |
| 10 timer per måned tapt | Får SMS-beskjed |
| Dobbel-bookinger | Systemet styrer alt |
| Ingen oversikt | Full kalender |

---

## Neste steg etter møtet

1. ✅ Mohammed sier ja
2. Du oppretter SimplyBook-konto (15 min)
3. Du lager nettsiden (1-2 dager)
4. Mohammed tester
5. Lansering!

---

## Support

Hvis Mohammed har spørsmål etter lansering:
- SimplyBook har norsk support
- Du hjelper med tekniske spørsmål
- Eventuelle endringer: 500 kr/tim

---

*Sist oppdatert: 9. mars 2026*
