# The Grand | Luxury Reservation System 🍴

Welcome to **The Grand**, an integrated, ultra-premium digital reservation system built for high-end restaurants. It combines an elite, typography-driven React web application with an automated WhatsApp personal concierge bot.

No clicking dropdowns on slow websites. Diners simply hit the **"Secure Your Table"** link, which immediately connects them to our Twilio-powered intelligent booking assistant right on WhatsApp. The bot handles their request, instantly writes it to our private Google Sheets ledger, and auto-generates a personalized PDF booking receipt, turning a mundane reservation process into a premium experience!

---

### Features & Workflow

✨ **Elite Typographic Frontend (React + Vite)**
A minimalist, bold typography-driven landing page prioritizing intense white space, dramatic contrasts with pure CSS variables, and modern responsive `clamp()` typography to draw the eye exclusively to the dining experience. *(Absolutely zero images used!)*

🤖 **WhatsApp Concierge Bot (Python + Flask)**
A lightweight webhook server waiting for inbound Twilio payloads. It talks to clients politely, walks them through table dates and party sizing, and gracefully handles unexpected inputs. A user can even cancel their table right from the chat using their phone number.

📊 **Automated Google Sheets Ledger**
The moment the booking is confirmed, the Python backend securely pushes the reservation via the `gspread` API to an interconnected Google Sheet running as the restaurant's operational database.

🧾 **Dynamic PDF Generation**
Upon confirmation, the backend compiles a customized, beautifully formatted PDF digital receipt dynamically generated using `reportlab`. It's signed, dated, and dispatched instantly via Twilio media servers back to the guest.

---

### Tech Stack

**Frontend:**
* React 18 & Vite
* Pure CSS (Global & Scoped Variables)
* Responsive Asymmetrical Editorial Typography Layout

**Backend:**
* Python & Flask
* Twilio WhatsApp Sandbox / Production API
* Google Sheets API (via Google Cloud IAM Service Accounts)
* `reportlab` (for rapid PDF generation)
* `ngrok` (for local webhook tunneling)

---

### How to Run Locally

Because security matters, this repository does not include our actual Google Sheets `.json` keys or our Twilio `.env` files. To run this project yourself:

**1. The Web Application:**
```bash
cd restaurant_frontend
npm install
npm run dev
```
Navigate to `http://localhost:5173` to see the live site.

**2. The WhatsApp Bot:**
* Ensure your Twilio API keys and Google Sheets service accounts are correctly established in an `.env` file within the `restaurant_bot/` folder.
* Setup your local environment:
```bash
cd restaurant_bot
pip install -r requirements.txt # (Flask, gspread, reportlab, python-dotenv, twilio)
python app.py
```
* Point an `ngrok` tunnel (`ngrok http 5000`) at the server and plug that URL into Twilio to start chatting with your concierge!

---

💡 **Built from scratch by [Manvi Sinha](https://github.com/manviisinha).** 
*This project explores the intersection of premium web design with instant, invisible API automation using modern communication tools like WhatsApp.*
