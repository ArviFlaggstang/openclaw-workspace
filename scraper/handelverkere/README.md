# Håndverkere - AI-salgsprospekter

Dette prosjektet inneholder lister over håndverkerbedrifter (VVS, elektrikere, rørleggere, snekkere) som er potensielle kunder for AI-automasjonstjenester.

## Målgruppe

Bedrifter som kan dra nytte av:
- AI-drevet kundeservice (chatbots)
- Automatisert timebestilling
- Dokumenthåndtering og fakturering
- Kundedatabase og CRM-automasjon
- Markedsføringsautomasjon
- Prosjektstyring

## Filstruktur

```
scraper/handelverkere/
├── data/
│   └── haandverkere_trondheim.csv    # Håndverkere i Trondheim
│   └── haandverkere_alta.csv         # Håndverkere i Alta (kommer)
└── README.md
```

## Dataformat

CSV-filen inneholder følgende kolonner:
- Navn: Bedriftsnavn
- Sted: Lokasjon
- Org.nr: Organisasjonsnummer
- Bransje: VVS/Rørlegger, Elektriker, Snekker, etc.
- Google-søk: Lenke til Google-søk
- E-post: Kontakt e-post (hvis funnet)
- Telefon: Telefonnummer
- Nettside: URL til bedriftens nettside

## Status

- [x] Opprettet mappestruktur
- [x] Funnet håndverkere i Trondheim
- [x] Funnet e-poster for 7 bedrifter
- [ ] Søke etter håndverkere i Alta
- [ ] Utvide til flere byer
- [ ] Lage script for automatisk e-postutsending
