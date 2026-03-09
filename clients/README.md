# CRM — Kundeoversikt

## Aktive Leads

| Bedrift | Status | Neste steg | Prioritet |
|---------|--------|------------|-----------|
| **Altaie Frisør** | 🔥 Møte booket (påske) | Forberede presentasjon | Høy |
| **Alta Mekaniske Verksted** | 🔥 Demo sendt | Følge opp om 2-3 dager | Høy |

## Pipeline

```
[Lead] → [Samtale] → [Møte/Tilbud] → [Kontrakt] → [Leveranse] → [Ferdig]
   │          │             │              │            │
   ▼          ▼             ▼              ▼            ▼
  Research   Ringe      Presentere    Signere      Utvikle
```

## Mappestruktur

```
clients/
├── altaie-frisor/
│   ├── README.md           # Hovedinfo og status
│   ├── calls/              # Samtale-notater
│   ├── proposals/          # Tilbud sendt
│   ├── contracts/          # Signerte avtaler
│   └── deliverables/       # Ferdige filer
│
└── altamekaniske/
    ├── README.md
    ├── calls/
    ├── proposals/
    ├── contracts/
    └── deliverables/
```

## Maler (opprettes etter behov)

- [ ] Tilbudsmal
- [ ] Kontraktmal
- [ ] Fakturamal

---

*Sist oppdatert: 9. mars 2026*
