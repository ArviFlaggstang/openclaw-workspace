a, men jeg ville gjort det på en kontrollert måte, ikke bare “send alt”. For tusenvis av mottakere er personlig Gmail feil verktøy; Google Workspace har daglige grenser på mottakere, og Gmail stiller også strengere krav til større avsendere. I tillegg bør du være forsiktig med kald e-post som markedsføring; Forbrukertilsynet er tydelig på at markedsføring via e-post er regulert, særlig mot forbrukere, så hold dette til relevante bedriftspubliserte adresser, vær målrettet, og gi enkel opt-out.

Den enkleste og tryggeste prosessen er:
- Samle leads i én CSV i stedet for mange .txt-filer
- Send i små batcher
- Logg hvem som fikk første mail
- Send oppfølging etter 3 dager bare til dem som ikke svarte
- Jeg anbefaler denne strukturen i CSV:

email,business_name,city,owner_name,demo_link,status,first_sent_at,followup_sent_at
post@eksempel.no,Frisør Eksempel,Trondheim,Mona,https://frisor-hub.vercel.app,pending,,


Python-script som:
- leser CSV
- sender første mail til status=pending
- oppdaterer first_sent_at
- etter 3 dager sender reminder til dem som fortsatt har status=sent og ingen followup_sent_at