# Booking System - Teknisk Implementasjonsguide

_Hvordan integrere SimplyBook i React/Vite nettsider_

## Arkitektur

```
Nettside (React/Vite)
    ↓
BookingSection.tsx
    ↓
window.open(SIMPLYBOOK_URL, '_blank')
    ↓
SimplyBook (https://[kunde].simplybook.me)
    ↓
SMS/E-post til kunden
```

## Fordeler med denne løsningen

1. **Enkel** — Ingen kompleks API-integrasjon
2. **Pålitelig** — SimplyBook håndterer alt
3. **Vedlikeholdsfri** — Ingen backend-kode
4. **Skalerbar** — Fungerer for alle kunder

## Ulemper

1. **Kunden forlater nettsiden** — Åpnes i ny fane
2. **Begrenset styling** — Kan ikke tilpasse SimplyBook UI
3. **Avhengig av tredjepart** — SimplyBook må være oppe

## Implementasjon

### 1. Komponent-struktur

```
src/
├── components/
│   └── BookingSection.tsx      # Hovedkomponent
├── lib/
│   └── simplybook-config.ts    # Konfigurasjon (valgfritt)
```

### 2. Minimalkode

```tsx
// src/components/BookingSection.tsx
const SIMPLYBOOK_URL = "https://[kunde].simplybook.me/v2/";

export const BookingSection = () => (
  <button onClick={() => window.open(SIMPLYBOOK_URL, '_blank')}>
    Bestill time
  </button>
);
```

### 3. Full komponent (med UI)

Se `booking-system-playbook.md` for komplett kode.

## Konfigurasjon per kunde

### 1. Lag config-fil

```ts
// src/lib/simplybook-config.ts
export const simplybookConfig = {
  url: "https://[kunde].simplybook.me/v2/",
  name: "[Kundens navn]",
  phone: "[Telefon]",
};
```

### 2. Bruk i komponent

```tsx
import { simplybookConfig } from "@/lib/simplybook-config";

const BookingSection = () => {
  return (
    <button onClick={() => window.open(simplybookConfig.url, '_blank')}>
      Bestill time hos {simplybookConfig.name}
    </button>
  );
};
```

## Testing

### Lokalt

```bash
npm run dev
# Gå til http://localhost:5173
# Klikk "Bestill time"
# Verifiser at SimplyBook åpnes
```

### Produksjon

```bash
npm run build
npm run preview
# Test på nytt
```

## Deployment

### 1. Bygg

```bash
npm run build
```

### 2. Deploy (Vercel/Netlify)

```bash
vercel --prod
# eller
netlify deploy --prod
```

### 3. Verifiser

- [ ] Nettside laster
- [ ] "Bestill time" knapp fungerer
- [ ] SimplyBook åpnes
- [ ] Test-booking fungerer

## Feilsøking

### Problem: SimplyBook åpnes ikke

**Sjekk:**
1. URL er korrekt (med https://)
2. Ingen adblocker blokkerer popup
3. Browser tillater popups

### Problem: Styling ser rart ut

**Sjekk:**
1. Tailwind CSS er konfigurert
2. Komponenten er importert riktig
3. Ingen CSS-konflikter

### Problem: Kunden får ikke SMS

**Sjekk:**
1. SimplyBook varsler er aktivert
2. Kundens telefonnummer er riktig
3. SMS-kreditt på SimplyBook-konto

## Gjenbruk for neste kunde

1. Kopier `BookingSection.tsx`
2. Endre `SIMPLYBOOK_URL`
3. Tilpass tekst/farger
4. Ferdig!

## Fremtidige forbedringer

### Vurder disse senere:

1. **SimplyBook API** — Dypere integrasjon
2. **Webhook** — Motta booking-data
3. **Egen backend** — Lagre bookinger lokalt
4. **Kalender-synk** — Google Calendar/Outlook

---

## Ressurser

- [SimplyBook Docs](https://simplybook.me/en/documentation)
- [SimplyBook API](https://api.simplybook.me/)
- [React Window Open](https://developer.mozilla.org/en-US/docs/Web/API/Window/open)

---

*Sist oppdatert: 9. mars 2026*
