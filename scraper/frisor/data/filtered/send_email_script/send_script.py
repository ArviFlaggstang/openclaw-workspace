import csv
import os
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.environ["SMTP_USER"]
SMTP_PASS = os.environ["SMTP_PASS"]

CSV_FILE = " "
MY_NAME = "Trym Andreas Johnsen"
MY_PHONE = "91516780"

SUBJECT_1 = "Forslag til nettside for {business_name}"
SUBJECT_2 = "Re: Forslag til nettside for {business_name}"

BODY_1 = """ 

"""

BODY_2 = """Hei {business_name},

Ville bare følge opp mailen jeg sendte for noen dager siden med demoen deres:

{demo_link}

Si gjerne ifra hvis dette er interessant, dette er helt risikofritt og jeg er fleksibel.

Mvh
{my_name}
{my_phone}
"""

def send_email(to_email: str, subject: str, body: str):
    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg["Reply-To"] = SMTP_USER
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

def main():
    now = datetime.utcnow()
    rows = []

    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    sent_count = 0
    max_per_run = 40

    for row in rows:
        if sent_count >= max_per_run:
            break

        email = row["email"].strip()
        business_name = row["business_name"].strip()
        city = row["city"].strip()
        demo_link = row["demo_link"].strip()
        status = (row.get("status") or "pending").strip()
        first_sent_at = (row.get("first_sent_at") or "").strip()
        followup_sent_at = (row.get("followup_sent_at") or "").strip()

        if status == "pending":
            subject = SUBJECT_1.format(business_name=business_name)
            body = BODY_1.format(
                business_name=business_name,
                city=city,
                demo_link=demo_link,
                my_name=MY_NAME,
                my_phone=MY_PHONE,
            )
            send_email(email, subject, body)
            row["status"] = "sent"
            row["first_sent_at"] = now.isoformat()
            sent_count += 1

        elif status == "sent" and first_sent_at and not followup_sent_at:
            sent_time = datetime.fromisoformat(first_sent_at)
            if now - sent_time >= timedelta(days=3):
                subject = SUBJECT_2.format(business_name=business_name)
                body = BODY_2.format(
                    business_name=business_name,
                    demo_link=demo_link,
                    my_name=MY_NAME,
                    my_phone=MY_PHONE,
                )
                send_email(email, subject, body)
                row["followup_sent_at"] = now.isoformat()
                row["status"] = "followup_sent"
                sent_count += 1

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Sent {sent_count} emails.")

if __name__ == "__main__":
    main()