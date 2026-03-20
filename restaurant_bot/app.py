from flask import Flask, request, send_file
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import threading
import time
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder=r"D:\Whatsapp\restaurant_bot")

# ===== SECURE CREDENTIALS (Loaded from .env) =====
TWILIO_SID        = os.environ.get("TWILIO_SID", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_NUMBER     = os.environ.get("TWILIO_NUMBER", "")
SHEET_ID          = os.environ.get("SHEET_ID", "")
CREDS_FILE        = os.environ.get("CREDS_FILE", "")
NGROK_URL         = os.environ.get("NGROK_URL", "")
# =================================================

twilio_client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
_sheet_cache = None
user_sessions = {}

def get_sheet():
    global _sheet_cache
    if _sheet_cache is None:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # In production (Render/Heroku), load from a raw JSON environment variable
        env_creds = os.environ.get("GOOGLE_CREDS_JSON")
        if env_creds:
            try:
                creds_dict = json.loads(env_creds)
                creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            except Exception as e:
                print(f"Failed to parse GOOGLE_CREDS_JSON from environment: {e}")
                raise e
        else:
            # Fallback to local file for testing
            creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)

        client = gspread.authorize(creds)
        _sheet_cache = client.open_by_key(SHEET_ID).sheet1
    return _sheet_cache

def save_to_sheets(name, datetime_slot, guests, phone):
    global _sheet_cache
    try:
        sheet = get_sheet()
        booking_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        clean_phone = phone.strip().replace(" ", "")
        sheet.append_row([name, datetime_slot, guests, clean_phone, booking_time])
        print(f"✅ Saved to sheets: {name} | {clean_phone}")
    except Exception as e:
        _sheet_cache = None
        print(f"❌ Sheets save error: {e}")

def delete_from_sheets(phone):
    global _sheet_cache
    try:
        sheet = get_sheet()
        all_records = sheet.get_all_records()
        clean_input = phone.strip().replace(" ", "")
        print(f"🔍 Looking for: {clean_input}")
        for i, record in enumerate(all_records):
            sheet_phone = str(record.get("Phone", "")).strip().replace(" ", "")
            if sheet_phone == clean_input:
                sheet.delete_rows(i + 2)
                print(f"✅ Deleted booking for: {clean_input}")
                return True, record.get("Name", "")
        print(f"❌ Not found: {clean_input}")
        return False, ""
    except Exception as e:
        _sheet_cache = None
        print(f"❌ Sheets delete error: {e}")
        return False, ""

def generate_pdf(name, datetime_slot, guests, phone):
    filename = rf"D:\Whatsapp\restaurant_bot\receipt_{name.replace(' ', '_')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    title_style = ParagraphStyle(
        "title",
        parent=styles["Title"],
        fontSize=24,
        textColor=colors.HexColor("#A86A32"),
        spaceAfter=10
    )
    elements.append(Paragraph("The Grand | Taj Lands End", title_style))
    elements.append(Paragraph("Official Reservation Record", styles["Heading2"]))
    elements.append(Spacer(1, 0.3 * inch))

    booking_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data = [
        ["Field",         "Details"],
        ["Guest Name",    name],
        ["Date & Time",   datetime_slot],
        ["No. of Guests", guests],
        ["Phone",         phone],
        ["Booking Time",  booking_time],
        ["Status",        "CONFIRMED"],
    ]

    table = Table(data, colWidths=[2.5 * inch, 4 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  colors.HexColor("#2C3E50")),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0),  13),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [colors.white, colors.HexColor("#F0F4F8")]),
        ("FONTNAME",      (0, 1), (0, -1),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 1), (-1, -1), 11),
        ("GRID",          (0, 0), (-1, -1), 0.5, colors.HexColor("#DEE2E6")),
        ("ROWHEIGHT",     (0, 0), (-1, -1), 30),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("BACKGROUND",    (0, -1),(-1, -1), colors.HexColor("#D4EDDA")),
        ("TEXTCOLOR",     (0, -1),(-1, -1), colors.HexColor("#155724")),
        ("FONTNAME",      (0, -1),(-1, -1), "Helvetica-Bold"),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.4 * inch))
    elements.append(Paragraph(
        "We eagerly await your arrival at The Grand, Mumbai.",
        styles["Heading3"]
    ))
    elements.append(Paragraph(
        "Kindly present this record to our maître d' upon arrival.",
        styles["Normal"]
    ))

    doc.build(elements)
    print(f"✅ PDF generated: {filename}")
    return filename

def background_tasks(name, dt, guests, phone, sender):
    try:
        # 1. Save to sheets
        save_to_sheets(name, dt, guests, phone)

        # 2. Generate PDF
        pdf_path = generate_pdf(name, dt, guests, phone)
        pdf_filename = os.path.basename(pdf_path)
        pdf_url = f"{NGROK_URL}/receipts/{pdf_filename}"

        # 3. Small wait for file to be ready
        time.sleep(2)

        # 4. Send PDF to user
        twilio_client.messages.create(
            media_url=[pdf_url],
            from_=TWILIO_NUMBER,
            to=sender
        )
        print(f"✅ PDF sent to: {sender}")

        # 5. Delete after 30 seconds
        time.sleep(30)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            print(f"✅ PDF deleted")

    except Exception as e:
        print(f"❌ Background task error: {e}")

@app.route("/receipts/<filename>")
def serve_receipt(filename):
    filepath = os.path.join(r"D:\Whatsapp\restaurant_bot", filename)
    if os.path.exists(filepath):
        return send_file(filepath, mimetype="application/pdf")
    return "File not found", 404

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.form.get("Body", "").strip()
    sender = request.form.get("From")
    phone = sender.replace("whatsapp:", "").strip()

    resp = MessagingResponse()
    msg = resp.message()

    session = user_sessions.get(sender, {"step": 0})

    # ===== RESET =====
    if incoming_msg.upper() in ["RESET", "START"]:
        user_sessions[sender] = {"step": 0}
        msg.body(
            "Namaste. Welcome to The Grand Concierge at Taj Lands End, Mumbai.\n\n"
            "I am here to assist you with your reservation.\n"
            "May I have the honor of knowing your *full name*?"
        )
        user_sessions[sender] = {"step": 1}
        return str(resp)

    # ===== CANCEL BOOKING =====
    if incoming_msg.upper() == "CANCEL BOOKING":
        msg.body(
            "❈ *Reservation Cancellation*\n\n"
            "Please provide the *phone number* associated with this booking.\n\n"
            "Example: _+919876543210_"
        )
        session = {"step": "cancel_lookup"}
        user_sessions[sender] = session
        return str(resp)

    if session.get("step") == "cancel_lookup":
        lookup_phone = incoming_msg.strip().replace(" ", "")
        deleted, name = delete_from_sheets(lookup_phone)
        if deleted:
            msg.body(
                f"✓ *Reservation Cancelled*\n\n"
                f"The booking under *{name}* has been gracefully removed from our ledger.\n\n"
                f"Should you wish to dine with us in the future, simply reply *START*."
            )
        else:
            msg.body(
                f"✗ *Record Not Found*\n\n"
                f"We could not locate a reservation for `{lookup_phone}`.\n"
                f"Please verify the number and reply *CANCEL BOOKING* to retry."
            )
        session = {"step": 0}
        user_sessions[sender] = session
        return str(resp)

    # ===== MAIN FLOW =====
    if session.get("step") == 0:
        msg.body(
            "Namaste. Welcome to The Grand Concierge at Taj Lands End, Mumbai.\n\n"
            "I am here to oversee your dining reservation.\n\n"
            "To begin, may I please have your *full name*?\n\n"
            "_Reply *CANCEL BOOKING* securely at any time._"
        )
        session["step"] = 1

    elif session.get("step") == 1:
        session["name"] = incoming_msg
        msg.body(
            f"A pleasure to assist you, *{incoming_msg}*.\n\n"
            "For what *date and time* shall I reserve your table?\n\n"
            "Example: _Tomorrow, 8:00 PM_"
        )
        session["step"] = 2

    elif session.get("step") == 2:
        session["datetime"] = incoming_msg
        msg.body("Splendid. How many esteemed *guests* will be joining us for this occasion?")
        session["step"] = 3

    elif session.get("step") == 3:
        session["guests"] = incoming_msg
        name   = session["name"]
        dt     = session["datetime"]
        guests = incoming_msg
        msg.body(
            f"Thank you. Please review your reservation request:\n\n"
            f"Guest: *{name}*\n"
            f"Date & Time: *{dt}*\n"
            f"Party Size: *{guests}*\n\n"
            f"Kindly reply *CONFIRM* to secure this table, or *CANCEL* to withdraw."
        )
        session["step"] = 4

    elif session.get("step") == 4:
        if incoming_msg.upper() == "CONFIRM":
            name   = session["name"]
            dt     = session["datetime"]
            guests = session["guests"]

            # ⚡ Reply instantly
            msg.body(
                f"✓ *Reservation Confirmed*\n\n"
                f"Your table is successfully secured.\n"
                f"Date & Time: {dt}\n\n"
                f"A personalized PDF record will be sent to you momentarily.\n\n"
                f"We eagerly await your arrival at The Grand."
            )

            # ⚡ Run heavy tasks in background
            thread = threading.Thread(
                target=background_tasks,
                args=(name, dt, guests, phone, sender)
            )
            thread.daemon = True
            thread.start()

            session = {"step": 0}

        elif incoming_msg.upper() == "CANCEL":
            session = {"step": 0}
            msg.body(
                "❈ *Reservation Voided*\n\n"
                "Your request has been discarded. No details were saved.\n"
                "When you are ready, simply reply to this chat to begin anew."
            )
        else:
            msg.body("Please reply *CONFIRM* to finalize the reservation, or *CANCEL* to withdraw.")

    user_sessions[sender] = session
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)