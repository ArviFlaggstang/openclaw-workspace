# Booking System Playbook

_Komplett guide for å sette opp SimplyBook for frisør-kunder_

## Oversikt

Dette dokumentet beskriver hvordan vi setter opp et komplett booking-system for frisør-kunder, fra SimplyBook-registrering til ferdig integrert nettside.

---

## Forutsetninger

- Kunden har en frisørsalong
- Kunden trenger online booking
- Kunden vil ha SMS/e-post bekreftelser

---

## Steg 1: Registrer SimplyBook-konto

### 1.1 Gå til SimplyBook

```
URL: https://simplybook.me
```

### 1.2 Registrer ny konto

| Felt | Verdi |
|------|-------|
| **Company name** | [Kundens salongnavn] |
| **Your URL** | [kundenavn].simplybook.me |
| **Industry** | Beauty and Personal Care → Hair Salons |
| **Email** | Kundens e-post |
| **Password** | (Kunden velger selv) |

**Tips:** Velg en kort, lett URL som kunden kan huske.

### 1.3 Verifiser e-post

1. Sjekk kundens e-post
2. Klikk verifiseringslenke fra SimplyBook
3. Logg inn på dashboardet

---

## Steg 2: Konfigurer tjenester

### 2.1 Gå til Services

```
Dashboard → Services → Add Service
```

### 2.2 Legg til standard tjenester

| Tjeneste | Varighet | Pris |
|----------|----------|------|
| Herreklipp | 30 min | 350 kr |
| Dameklipp | 45 min | 450 kr |
| Barneklipp | 20 min | 250 kr |
| Farging | 90 min | 800 kr |
| Striper/Highlights | 120 min | 1200 kr |
| Barbering | 15 min | 200 kr |

**Merk:** Tilpass priser etter kundens prisliste.

### 2.3 For hver tjeneste:

1. **Service name**: Navn på tjenesten
2. **Duration**: Varighet i minutter
3. **Price**: Pris (valgfritt)
4. **Description**: Kort beskrivelse
5. **Click "Save"**

---

## Steg 3: Sett åpningstider

### 3.1 Gå til Working Schedule

```
Dashboard → Settings → Working Schedule
```

### 3.2 Standard åpningstider

| Dag | Fra | Til |
|-----|-----|-----|
| Mandag | 09:00 | 17:00 |
| Tirsdag | 09:00 | 17:00 |
| Onsdag | 09:00 | 17:00 |
| Torsdag | 09:00 | 17:00 |
| Fredag | 09:00 | 17:00 |
| Lørdag | 10:00 | 14:00 |
| Søndag | Stengt | - |

### 3.3 Legg til pauser (valgfritt)

- Lunsjpause: 12:00-13:00
- Andre pauser etter behov

---

## Steg 4: Legg til provider (frisør)

### 4.1 Gå til Providers

```
Dashboard → Providers → Add Provider
```

### 4.2 Fyll inn info

| Felt | Verdi |
|------|-------|
| **Name** | Kundens navn / frisørens navn |
| **Email** | Kundens e-post |
| **Phone** | Kundens telefon |

### 4.3 Koble tjenester til provider

1. Gå til provider-innstillingene
2. Velg "Services" tab
3. Kryss av for alle tjenester
4. Klikk "Save"

---

## Steg 5: Konfigurer varsler

### 5.1 Gå til Notifications

```
Dashboard → Settings → Notifications
```

### 5.2 Sett opp varsler for kunden

| Type | Innstilling |
|------|-------------|
| **Ny booking** | ✅ E-post + SMS |
| **Avbestilling** | ✅ E-post + SMS |
| **Påminnelse** | ✅ SMS 24t før |

### 5.3 Sett opp varsler for kundens kunder

| Type | Innstilling |
|------|-------------|
| **Bekreftelse** | ✅ E-post |
| **Påminnelse** | ✅ SMS 24t før |
| **Takk for besøket** | ✅ E-post (valgfritt) |

**Merk:** SMS koster ekstra (~0.50 kr per melding).

---

## Steg 6: Integrer i nettsiden

### 6.1 Hent SimplyBook URL

```
URL: https://[kundenavn].simplybook.me/v2/
```

Eksempel: `https://altaie.simplybook.it/v2/`

### 6.2 Oppdater BookingSection.tsx

```tsx
const SIMPLYBOOK_URL = "https://[kundenavn].simplybook.me/v2/";
```

### 6.3 Komponent-kode (simplified)

```tsx
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

const SIMPLYBOOK_URL = "https://[kundenavn].simplybook.me/v2/";

const BookingSection = () => {
  return (
    <section id="bestill" className="py-16 md:py-24">
      <div className="container mx-auto px-4 max-w-4xl text-center">
        <h2 className="text-3xl md:text-4xl font-bold mb-4">
          Bestill time
        </h2>
        <p className="text-muted-foreground mb-8">
          Book din time raskt og enkelt
        </p>
        
        <Card className="bg-accent text-accent-foreground shadow-xl">
          <CardContent className="p-8 md:p-12">
            <h3 className="text-2xl font-bold mb-4">
              Klar til å bestille?
            </h3>
            <Button
              size="lg"
              variant="secondary"
              className="rounded-full px-8 py-6 text-lg"
              onClick={() => window.open(SIMPLYBOOK_URL, '_blank')}
            >
              Åpne booking
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
          </CardContent>
        </Card>
      </div>
    </section>
  );
};

export default BookingSection;
```

---

## Steg 7: Test systemet

### 7.1 Test-booking

1. Gå til nettsiden
2. Klikk "Åpne booking"
3. Velg tjeneste, dato, tid
4. Fullfør booking
5. Sjekk at kunden får SMS/e-post

### 7.2 Verifiser varsler

- [ ] Kunden får SMS ved ny booking
- [ ] Kunden får e-post ved ny booking
- [ ] Kunde får påminnelse 24t før

---

## Steg 8: Opplæring av kunden

### 8.1 Vis kunden hvordan de:

1. **Ser nye bookinger** (dashboard)
2. **Avbestiller timer** (hvis nødvendig)
3. **Endrer åpningstider** (settings)
4. **Legger til nye tjenester** (services)

### 8.2 Gi kunden:

- SimplyBook login-info
- Direkte link til admin: `https://[kundenavn].simplybook.me/admin/`
- Support-kontakt: SimplyBook support

---

## Prising

### Vår pris til kunden:

| Post | Beløp |
|------|-------|
| Nettside med booking | 15 000 kr |
| Drift (hosting) | 500 kr/mnd |

### SimplyBook kostnad (kunden betaler selv):

| Plan | Pris | Inkludert |
|------|------|-----------|
| **Free** | 0 kr | 50 bookinger/mnd, begrenset funksjoner |
| **Basic** | ~199 kr/mnd | Ubegrenset, standard funksjoner |
| **Standard** | ~399 kr/mnd | Avansert, flere brukere |

**Anbefaling:** Start med Basic (~199 kr/mnd).

---

## Gjenbruk for neste kunde

1. Kopier denne playbooken
2. Bytt ut [kundenavn] med nytt navn
3. Tilpass tjenester og priser
4. Følg stegene 1-8
5. Ferdig!

---

## Support

### Hvis noe ikke fungerer:

1. **SimplyBook support:** support@simplybook.me
2. **Norsk support:** Finnes (kan være treg)
3. **Vi hjelper med:** Tekniske spørsmål, integrasjon

---

## Sjekkliste før lansering

- [ ] SimplyBook-konto opprettet
- [ ] Tjenester lagt inn
- [ ] Åpningstider satt
- [ ] Provider lagt til
- [ ] Varsler konfigurert
- [ ] Test-booking gjennomført
- [ ] Kunden har fått opplæring
- [ ] Kunden har login-info
- [ ] Nettside lansert

---

*Sist oppdatert: 9. mars 2026*
