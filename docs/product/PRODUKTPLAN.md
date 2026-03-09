# PRODUKTPLAN — AI Telefonsvar for Håndverkere

_Versjon: 1.0 | Opprettet: 2026-03-06 | Sist oppdatert: 2026-03-06_

## Hva vi selger

**Produkt:** AI Telefonsvar 24/7 for håndverkere (rørleggere, elektrikere, VVS)

**Kjerneverdi:** Aldri miste en leadsamtale igjen

## Teknisk arkitektur

```
Kunde ringer
    ↓
Retell AI (skybasert) — svarer, tar imot info
    ↓
Make.com — videresender data
    ↓
SMS til håndverker
```

**Viktig:** Kunden trenger IKKE OpenClaw. De trenger kun:
- Et telefonnummer (vi setter opp)
- En telefon som mottar SMS (de har allerede)

## Hva kunden får

| Komponent | Beskrivelse |
|-----------|-------------|
| Dedikert telefonnummer | Kunder ringer hit i stedet for direkte til håndverker |
| AI som svarer 24/7 | Tar imot navn, telefon, hva det gjelder |
| SMS-varsling | Håndverker får SMS umiddelbart etter samtale |
| Lead-logg | Oversikt over alle henvendelser |

## Hvordan kunden bruker tjenesten

### Oppsett (vi gjør dette)
1. Vi kjøper nytt telefonnummer (f.eks. 930 12 345)
2. Vi konfigurerer AI-en med håndverkerens info
3. Vi kobler nummeret til AI-en
4. Vi tester at SMS kommer til håndverkerens telefon

### Daglig bruk (kunden gjør ingenting)
- Håndverkeren beholder sitt gamle nummer (f.eks. 901 23 456)
- **NYTT nummer (930 12 345) blir markedsført:**
  - På nettside
  - I Google Maps
  - På bilen
  - I annonser
  - På visittkort

### Hva som skjer
```
Kunde ser: "Ring 930 12 345 for rørleggerhjelp"
    ↓
Kunde ringer 930 12 345
    ↓
AI svarer, tar imot info
    ↓
Håndverker får SMS: "Ny henvendelse fra Ola, tlf 123 45 678, 
                      gjelder vannlekkasje"
    ↓
Håndverker ringer tilbake til kunden
```

### Overgangsfase (valgfritt)
Hvis håndverkeren vil beholde gammelt nummer:
- Gammelt nummer kan videresendes til nytt AI-nummer
- Eks: 901 23 456 → 930 12 345
- Da svarer AI-en uansett hvilket nummer kunden ringer

## Hva kunden IKKE trenger

- ❌ OpenClaw
- ❌ Egen server
- ❌ Teknisk kompetanse
- ❌ App eller programvare

## Hva vi gjør (Trym + Arvi)

| Oppgave | Hvem |
|---------|------|
| Sette opp Retell AI | Arvi |
| Konfigurere dialogflyt | Arvi |
| Koble til telefonnummer | Arvi |
| Sette opp Make.com | Arvi |
| Teste systemet | Sammen |
| Selge til kunde | Trym |
| Support ved problemer | Trym (med Arvi som backup) |

## Prising

**Kunde betaler:** 4.500 kr/mnd + 8.000 kr oppsett

**Våre kostnader:** ~300-700 kr/mnd per kunde
- Retell AI: ~$0.07/min
- Telefonnummer: ~50-100 kr/mnd
- SMS: ~0.05-0.50 kr per melding

**Margin:** ~80-85%

## Endringslogg

| Dato | Hva endret | Hvorfor |
|------|------------|---------|
| 2026-03-06 | Versjon 1.0 opprettet | Første utkast, MVP-fokus |

## Neste versjoner (fremtid)

- [ ] Automatisk kalenderbooking
- [ ] Smart routing (nød vs ikke-nød)
- [ ] Integrasjon med kundens CRM
- [ ] Flere språk (engelsk, polsk, etc.)
