#!/usr/bin/env python3
"""
Finner de beste frisør-leads fra rådata.
Filtrerer etter: små bedrifter, aktive, uten nettside, prioritert etter sted.
"""

import json
from pathlib import Path
from datetime import datetime

def load_raw_data():
    """Laster begge rådata-filene."""
    data_dir = Path(__file__).parent / ".." / "raw"
    
    files = [
        "frisor_bedrifter_frisor_only.json",
        "frisor_bedrifter_andre_termer.json"
    ]
    
    all_bedrifter = []
    seen_orgnr = set()
    
    for filename in files:
        filepath = data_dir / filename
        if not filepath.exists():
            print(f"Fant ikke {filepath}")
            continue
        
        with open(filepath, "r", encoding="utf-8") as f:
            bedrifter = json.load(f)
        
        for b in bedrifter:
            orgnr = b.get("orgnr")
            if orgnr and orgnr not in seen_orgnr:
                seen_orgnr.add(orgnr)
                all_bedrifter.append(b)
        
        print(f"Lastet {len(bedrifter)} fra {filename}")
    
    print(f"\nTotalt unike bedrifter: {len(all_bedrifter)}")
    return all_bedrifter

def is_good_lead(bedrift):
    """
    Sjekker om en bedrift er et godt lead.
    Kriterier:
    - Ikke konkurs
    - Ikke under avvikling
    - Ikke under tvangsavvikling
    - Små bedrifter (ENK eller AS med 1-10 ansatte)
    - Uten registrert hjemmeside (størst behov!)
    """
    # Sjekk status
    if bedrift.get("konkurs"):
        return False, "konkurs"
    if bedrift.get("under_avvikling"):
        return False, "under_avvikling"
    if bedrift.get("under_tvangsavvikling"):
        return False, "under_tvangsavvikling"
    
    # Sjekk størrelse
    org_form = bedrift.get("organisasjonsform", "")
    ansatte = bedrift.get("antall_ansatte")
    
    is_small = False
    if org_form == "ENK":
        is_small = True
    elif org_form == "AS":
        if ansatte is None or (1 <= ansatte <= 10):
            is_small = True
    elif org_form in ["ANS", "DA", "KS"]:
        if ansatte is None or (1 <= ansatte <= 10):
            is_small = True
    
    if not is_small:
        return False, "for_stor"
    
    # Sjekk om de har hjemmeside
    if bedrift.get("hjemmeside"):
        return False, "har_hjemmeside"
    
    return True, "ok"

def score_lead(bedrift):
    """
    Gir en score til leadet basert på hvor bra det er.
    Høyere score = bedre lead.
    """
    score = 0
    
    # ENK er best (eier = beslutningstaker)
    if bedrift.get("organisasjonsform") == "ENK":
        score += 20
    
    # Små AS er også bra
    elif bedrift.get("organisasjonsform") == "AS":
        score += 15
    
    # Etablert bedrift (ikke helt ny)
    reg_dato = bedrift.get("registreringsdato")
    if reg_dato:
        try:
            dato = datetime.strptime(reg_dato, "%Y-%m-%d")
            alder = (datetime.now() - dato).days / 365
            if 3 <= alder <= 20:  # 3-20 år er sweet spot
                score += 10
            elif alder > 20:  # Veldig etablert
                score += 5
        except:
            pass
    
    # Alle byer likestilt - ingen ekstra poeng for Trondheim
    adresse = bedrift.get("forretningsadresse", {})
    poststed = adresse.get("poststed", "").upper()
    
    # Store byer får litt poeng (uavhengig av hvilken by)
    if any(by in poststed for by in ["TRONDHEIM", "OSLO", "BERGEN", "STAVANGER", "KRISTIANSAND", "TROMSØ", "BODØ", "DRAMMEN", "FREDRIKSTAD", "SANDNES", "SARPSBORG", "PORSGRUNN", "TØNSBERG", "MOSS", "HAUGESUND", "SANDEFJORD", "LARVIK", "ASKER", "BÆRUM", "LILLESTRØM", "HAMAR", "ELVERUM", "GJØVIK", "RINGERIKE", "KONGSBERG", "HALDEN", "ARENDAL", "GRIMSTAD", "LILLESAND", "MANDAL", "FARSUND", "FLEKKEFJORD", "EIGERSUND", "JØRPELAND", "BRYNE", "KLEPP", "KARMØY", "KOPERVIK", "HAUGESUND", "STORD", "LEIRVIK", "ODDA", "VOSS", "VOSSAVANGEN", "ØYSTESE", "NORHEIMSUND", "ULVIK", "EIDFJORD", "ULENSAKER", "JESSHEIM", "KLØFTA", "NANNESTAD", "NES", "AURSKOG-HØLAND", "BJØRKELANGEN", "LØRENSKOG", "FET", "SØRUM", "RÆLINGEN", "ENEBAKK", "FROGN", "DRØBAK", "NESODDEN", "OPPEGÅRD", "VEVELSTAD", "ÅS", "SKI", "NORDRE FOLLO", "KRÅKSTAD", "VESTBY", "HÅRUM", "SPYDEBERG", "ASKIM", "TRØGSTAD", "ØRJEBRO", "RAKKESTAD", "MARKER", "RØMSKOG", "AURSUND", "TROMSØ", "BODØ", "NARVIK", "HARSTAD", "ALTA", "HAMMERFEST", "VADSØ", "KIRKENES", "MO I RANA", "MOSJØEN", "Fauske", "SORTLAND", "STOKMARKNES", "SVOLVÆR", "LEKNES", "VESTVÅGØY", "MELBU", "HADSEL", "BØ I VESTERÅLEN", "MYRE", "ØKSNES", "ANDENES", "RISØYHAMN", "BJERKA", "MO I RANA", "NESNA", "HEMNES", "KORGAN", "HØYANGER", "STRYN", "SANDANE", "NORDFJORDEID", "MÅLØY", "VÅGSØY", "FLORØ", "FØRDE", "SANDEFJORD", "LARVIK", "TØNSBERG", "HORTEN", "HOLMESTRAND", "RE", "ANDEBU", "STOKKE", "NØTTERØY", "TJØME", "SANDAR", "PORSGRUNN", "SKIEN", "BAMBLE", "LANGESUND", "STATHELLE", "KRAGERØ", "RISØR", "GRIMSTAD", "ARENDAL", "FROLAND", "MYKLAND", "BIRKELAND", "TVEDESTRAND", "VEGÅRSHEI", "GJERSTAD", "SØNDELED", "LILLESAND", "MANDAL", "FARSUND", "FLEKKEFJORD", "LYNGDAL", "KVINESDAL", "SØGNE", "SONGDALEN", "Vennesla", "KRISTIANSAND", "MARNARDAL", "AUDNEDAL", "LINDESNES", "MANDAL"]):
        score += 5
    
    return score

def find_best_leads(bedrifter, max_leads=200):
    """Finner de beste leadsene."""
    good_leads = []
    
    print("\nFiltrerer leads...")
    
    for bedrift in bedrifter:
        is_good, reason = is_good_lead(bedrift)
        if is_good:
            score = score_lead(bedrift)
            bedrift["lead_score"] = score
            good_leads.append(bedrift)
    
    print(f"Fant {len(good_leads)} gode leads av {len(bedrifter)} totale")
    
    # Sorter etter score (høyest først)
    good_leads.sort(key=lambda x: x["lead_score"], reverse=True)
    
    # Ta de beste
    best_leads = good_leads[:max_leads]
    
    return best_leads

def save_best_leads(leads):
    """Lagrer beste leads til JSON."""
    output_dir = Path(__file__).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "filtered_best_leads.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(leads, f, ensure_ascii=False, indent=2)
    
    print(f"\nLagret {len(leads)} beste leads til {output_file}")

def print_stats(leads):
    """Skriver ut statistikk."""
    org_forms = {}
    steder = {}
    
    for lead in leads:
        # Org form
        org_form = lead.get("organisasjonsform", "Ukjent")
        org_forms[org_form] = org_forms.get(org_form, 0) + 1
        
        # Sted
        adresse = lead.get("forretningsadresse", {})
        poststed = adresse.get("poststed", "Ukjent")
        steder[poststed] = steder.get(poststed, 0) + 1
    
    print("\n=== TOPP 200 LEADS ===")
    print(f"Totalt: {len(leads)} leads")
    
    print("\nOrganisasjonsformer:")
    for org_form, count in sorted(org_forms.items(), key=lambda x: x[1], reverse=True):
        print(f"  {org_form}: {count}")
    
    print("\nTopp 10 steder:")
    for sted, count in sorted(steder.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {sted}: {count}")
    
    print("\nTopp 10 leads (høyest score):")
    for i, lead in enumerate(leads[:10], 1):
        adresse = lead.get("forretningsadresse", {})
        print(f"  {i}. {lead['navn'][:40]:40} | Score: {lead['lead_score']:2d} | {adresse.get('poststed', 'N/A')}")

def export_to_csv(leads):
    """Eksporterer til CSV for emailing."""
    import csv
    
    output_dir = Path(__file__).parent / "csv"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "best_leads_for_email.csv"
    
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Org.nr", "Navn", "Organisasjonsform", "Adresse", "Postnr", "Poststed",
            "Registrert", "Lead Score", "Telefon", "E-post", "Kontaktet", "Status"
        ])
        
        for lead in leads:
            adresse = lead.get("forretningsadresse", {})
            writer.writerow([
                lead.get("orgnr", ""),
                lead.get("navn", ""),
                lead.get("organisasjonsform", ""),
                adresse.get("adresse", ""),
                adresse.get("postnummer", ""),
                adresse.get("poststed", ""),
                lead.get("registreringsdato", ""),
                lead.get("lead_score", 0),
                "",  # Telefon (må fylles inn manuelt)
                "",  # E-post (må fylles inn manuelt)
                "Nei",  # Kontaktet
                ""  # Status
            ])
    
    print(f"\nEksportert til {output_file}")
    print("  Kolonner for telefon/e-post er tomme - må hentes fra 1881/Gulesider")

def main():
    print("=" * 60)
    print("FINNER BESTE FRISØR-LEADS")
    print("=" * 60)
    
    # Last data
    bedrifter = load_raw_data()
    
    if not bedrifter:
        print("Ingen data funnet!")
        return
    
    # Finn beste leads
    best_leads = find_best_leads(bedrifter, max_leads=200)
    
    if not best_leads:
        print("Ingen gode leads funnet!")
        return
    
    # Lagre og eksporter
    save_best_leads(best_leads)
    print_stats(best_leads)
    export_to_csv(best_leads)
    
    print("\n" + "=" * 60)
    print("FERDIG!")
    print("=" * 60)
    print(f"\nNeste steg:")
    print(f"1. Åpne: data/filtered/csv/best_leads_for_email.csv")
    print(f"2. Hent telefon/e-post fra 1881.no eller Gulesider")
    print(f"3. Send cold emails til de 10-20 beste først (test)")
    print(f"4. Følg opp med telefon etter 3-4 dager")

if __name__ == "__main__":
    main()
