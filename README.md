# 🎣 Phishing Security Lab — Dashboard Edition

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-Web-green?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=for-the-badge)
![Security](https://img.shields.io/badge/Security-Educational-red?style=for-the-badge)

</div>

> **A controlled phishing simulation lab + automated detector with dashboard and professional reports (JSON + PDF).**

This project combines:
- 🟥 **Red Team** → Local, transparent phishing simulation lab  
- 🟦 **Blue Team** → Automated phishing detector with risk scoring  
- 📊 **Dashboard** → Web UI to visualize and download reports  
- 📄 **Reporting** → Structured JSON + multi-page professional PDF  

⚠️ **For education and authorized testing only.**

---

## 🎯 What you will learn

- How phishing pages are structured  
- How typosquatting detection works  
- How security headers affect risk  
- How to generate professional security reports  
- How to build a simple security dashboard  
- How to containerize a cybersecurity project with Docker  

---

## 🏗️ Project Structure

phishing-security-lab/
│
├── main.py # Phishing Lab (educational simulator)
├── detector.py # Phishing Detector (risk analysis)
│
├── templates/
│ ├── google.html
│ ├── microsoft.html
│ └── github.html
│ └── dashboard.html # Web dashboard
│
├── reports/
│ ├── init.py
│ ├── json_report.py
│ └── pdf_report.py
│
├── Dockerfile
├── requirements.txt
└── README.md

yaml
Copier le code

---

## 🧪 Part 1 — Phishing Lab (Local & Transparent)

Launch the lab:

```bash
pip install -r requirements.txt
python3 main.py --template google --port 8080
Then open:
👉 http://127.0.0.1:8080

Available templates:

bash
Copier le code
python3 main.py --template microsoft --port 8080
python3 main.py --template github --port 8080
Features:

Realistic login pages (Google, Microsoft, GitHub)

Clear warning banner (training lab)

Transparent logging (phishing_lab.log)

Automatic analysis on form submission

🔎 Part 2 — Phishing Detector (Blue Team)
Analyze a URL:

bash
Copier le code
python3 detector.py --url https://google.com
Example suspicious URL:

bash
Copier le code
python3 detector.py --url http://g00gle-login-secure.com
What it checks:

Typosquatting (domain similarity)

IP-based URLs

Redirect chains

Security headers (HSTS, CSP, X-Frame-Options)

Automated risk scoring: LOW / MEDIUM / HIGH

📊 Part 3 — Dashboard
Open:
👉 http://127.0.0.1:8080/dashboard

You will see:

List of generated reports

Download links for JSON & PDF

Central view of all analyses

📄 Reporting
Every analysis generates:

JSON
pgsql
Copier le code
phishing_lab_analysis_YYYYMMDD_HHMMSS.json
Multi-page PDF
Includes:

Cover page

Executive summary

Technical findings

🐳 Docker (Recommended)
Build:

bash
Copier le code
docker build -t phishing-lab .
Run:

bash
Copier le code
docker run -p 8080:8080 phishing-lab
Then open:
👉 http://127.0.0.1:8080

🚀 Roadmap
Authentication-aware detection

Better similarity algorithm

Interactive charts in dashboard

CVSS-like scoring model

Cloud deployment

⚖️ Legal Disclaimer
For education, research, and authorized testing only.
Do not use against real users or systems without permission.

👨‍💻 Author
Ashdevvv