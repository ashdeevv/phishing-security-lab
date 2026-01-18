#!/usr/bin/env python3
import argparse
import os
import json
from datetime import datetime
from reports.json_report import JSONReporter
from reports.pdf_report import PDFReporter
from detector import compute_risk
from flask import send_from_directory

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

LOG_FILE = "phishing_lab.log"

def log_event(event: str):
    """Journalisation explicite et transparente (audit / formation)."""
    timestamp = datetime.utcnow().isoformat()
    line = f"[{timestamp}] {event}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)
    print(line.strip())

@app.route("/")
def index():
    """Page d'accueil qui explique clairement qu'il s'agit d'un LAB."""
    return """
    <h1>🔐 Phishing Security Lab — ENVIRONNEMENT DE FORMATION</h1>
    <p>
    Ceci est une simulation <b>pédagogique</b> destinée à comprendre 
    comment les pages de phishing sont construites et comment les détecter.
    </p>
    <ul>
        <li>👉 <a href="/login">Voir la page de login simulée</a></li>
        <li>👉 <a href="/report">Voir les journaux du lab</a></li>
    </ul>
    """

@app.route("/login", methods=["GET"])
def login_page():
    """Affiche une page de login simulée (template)."""
    template = request.args.get("template", "google")
    log_event(f"VIEW login page — template={template}")
    return render_template(f"{template}.html")

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username", "<vide>")
    log_event(f"FORM SUBMISSION (simulated) — username={username}")

    # 🔹 Lancer automatiquement l’analyse de phishing sur l’URL locale
    local_url = "http://127.0.0.1:8080/login"

    result = compute_risk(local_url)

    # 🔹 Générer rapports
    json_reporter = JSONReporter(base_name="phishing_lab_analysis")
    pdf_reporter = PDFReporter(base_name="phishing_lab_analysis")

    json_file = json_reporter.save(result)
    pdf_file = pdf_reporter.save(result)

    return f"""
    <h2>⚠️ Simulation de phishing — Alerte de formation</h2>
    <p>Analyse automatique effectuée sur : <b>{local_url}</b></p>

    <h3>📊 Résultat</h3>
    <p><b>Risque :</b> {result['risk_level']} (score={result['risk_score']})</p>

    <h3>📄 Rapports générés</h3>
    <ul>
        <li>{json_file}</li>
        <li>{pdf_file}</li>
    </ul>

    <a href="/">Retour à l'accueil</a>
    """

@app.route("/report")
def report():
    """Affiche les logs pour analyse (transparence du lab)."""
    if not os.path.exists(LOG_FILE):
        return "<h2>Aucun log pour l'instant.</h2><a href='/'>Retour</a>"

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logs = f.read().replace("\n", "<br>")

    return f"""
    <h1>📋 Journaux du Phishing Lab</h1>
    <pre>{logs}</pre>
    <a href="/">Retour</a>
    """

@app.route("/dashboard")
def dashboard():
    files = []
    for f in os.listdir("."):
        if f.endswith(".json") or f.endswith(".pdf"):
            files.append({
                "name": f,
                "type": "PDF" if f.endswith(".pdf") else "JSON"
            })

    return render_template("dashboard.html", files=files)

@app.route("/download/<path:filename>")
def download_file(filename):
    return send_from_directory(".", filename, as_attachment=True)


def main():
    parser = argparse.ArgumentParser(description="Phishing Security Lab (V1 - Educational)")
    parser.add_argument("--template", default="google",
                        choices=["google", "microsoft", "github"],
                        help="Template de page simulée")
    parser.add_argument("--port", type=int, default=8080,
                        help="Port local (ex: 8080)")
    args = parser.parse_args()

    print("\n======================================")
    print("   PHISHING SECURITY LAB — V1")
    print("   (ENVIRONNEMENT ÉDUCATIF LOCAL)")
    print("======================================\n")

    print(f"[+] Template sélectionné : {args.template}")
    print(f"[+] Serveur local : http://localhost:{args.port}")
    print("[+] Logs : phishing_lab.log")
    print("\n⚠️  UTILISATION STRICTEMENT ÉDUCATIVE\n")

    app.run(host="127.0.0.1", port=args.port, debug=False)

if __name__ == "__main__":
    main()