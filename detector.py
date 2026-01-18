#!/usr/bin/env python3
import argparse
import re
import requests
from urllib.parse import urlparse
from datetime import datetime
from reports.json_report import JSONReporter
from reports.pdf_report import PDFReporter

# -------------------------------
# UTILITAIRES
# -------------------------------

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

def domain_similarity(a, b):
    """
    Similarité très simple (pédagogique) basée sur caractères communs.
    Plus le score est élevé, plus les domaines se ressemblent.
    """
    a = re.sub(r"[^a-z0-9]", "", a.lower())
    b = re.sub(r"[^a-z0-9]", "", b.lower())

    common = sum(1 for c in a if c in b)
    max_len = max(len(a), len(b), 1)
    return round((common / max_len) * 100, 2)

def extract_domain(url):
    parsed = urlparse(url)
    return parsed.netloc.lower()

def has_ip_in_domain(domain):
    """Détecte si l'URL utilise une IP au lieu d'un nom de domaine."""
    ip_regex = r"^\d{1,3}(\.\d{1,3}){3}$"
    return bool(re.match(ip_regex, domain))

# -------------------------------
# ANALYSES DE SÉCURITÉ
# -------------------------------

def check_headers(url):
    findings = {}

    try:
        r = requests.get(url, timeout=10, allow_redirects=True)
        headers = r.headers

        findings["status_code"] = r.status_code
        findings["final_url"] = r.url
        findings["redirects"] = len(r.history)

        # Headers de sécurité importants
        findings["hsts"] = "Strict-Transport-Security" in headers
        findings["csp"] = "Content-Security-Policy" in headers
        findings["x_frame"] = "X-Frame-Options" in headers

    except Exception as e:
        findings["error"] = str(e)

    return findings

# -------------------------------
# SCORING DE RISQUE
# -------------------------------

def compute_risk(url, target_brand="google.com"):
    domain = extract_domain(url)

    similarity = domain_similarity(domain, target_brand)
    ip_used = has_ip_in_domain(domain)
    headers = check_headers(url)

    risk_score = 0
    reasons = []

    # 1) Similarité de domaine (typosquatting)
    if similarity > 85:
        risk_score += 3
        reasons.append(f"Haute similarité avec {target_brand} ({similarity}%)")

    elif similarity > 60:
        risk_score += 2
        reasons.append(f"Similarité suspecte avec {target_brand} ({similarity}%)")

    # 2) IP dans le domaine
    if ip_used:
        risk_score += 2
        reasons.append("Utilisation d'une adresse IP dans l'URL")

    # 3) Redirections multiples
    if headers.get("redirects", 0) > 1:
        risk_score += 2
        reasons.append("Chaîne de redirections suspecte")

    # 4) Headers de sécurité manquants
    if not headers.get("hsts"):
        risk_score += 1
        reasons.append("HSTS manquant")

    if not headers.get("csp"):
        risk_score += 1
        reasons.append("CSP manquant")

    if not headers.get("x_frame"):
        risk_score += 1
        reasons.append("X-Frame-Options manquant")

    # Détermination du niveau
    if risk_score >= 6:
        level = "HIGH"
    elif risk_score >= 3:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "url": url,
        "domain": domain,
        "similarity_with_brand": similarity,
        "ip_in_domain": ip_used,
        "redirect_chain": headers.get("redirects", 0),
        "security_headers": {
            "hsts": headers.get("hsts"),
            "csp": headers.get("csp"),
            "x_frame": headers.get("x_frame"),
        },
        "risk_level": level,
        "risk_score": risk_score,
        "reasons": reasons,
        "http_status": headers.get("status_code"),
        "final_url": headers.get("final_url"),
    }

# -------------------------------
# CLI PRINCIPALE
# -------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Phishing Detector (V2 - Educational)"
    )

    parser.add_argument("--url", required=True, help="URL à analyser")
    parser.add_argument(
        "--brand",
        default="google.com",
        help="Marque de référence pour détection (ex: google.com, microsoft.com)",
    )

    args = parser.parse_args()

    print("\n======================================")
    print("   PHISHING DETECTOR — V2")
    print("   (Analyse défensive & pédagogique)")
    print("======================================\n")

    log(f"Analyzing: {args.url}")
    log(f"Reference brand: {args.brand}")

    result = compute_risk(args.url, args.brand)

    print("\n=== RÉSULTAT DE L'ANALYSE ===")
    print(f"URL: {result['url']}")
    print(f"Domaine: {result['domain']}")
    print(f"Similarité avec {args.brand}: {result['similarity_with_brand']}%")
    print(f"IP dans le domaine: {result['ip_in_domain']}")
    print(f"Redirections: {result['redirect_chain']}")
    print(f"HSTS présent: {result['security_headers']['hsts']}")
    print(f"CSP présent: {result['security_headers']['csp']}")
    print(f"X-Frame-Options présent: {result['security_headers']['x_frame']}")

    print(f"\n➡️  NIVEAU DE RISQUE: {result['risk_level']} (score={result['risk_score']})")

    if result["reasons"]:
        print("\nRaisons:")
        for r in result["reasons"]:
            print(f"- {r}")
    else:
        print("\nAucun signal fort de phishing détecté.")

    # -------------------------------
    # CLI PRINCIPALE
    # -------------------------------
    print("\n[*] Generating reports...")
    
    json_reporter = JSONReporter(base_name="phishing_analysis")
    pdf_reporter = PDFReporter(base_name="pishing_analysis")

    json_file = json_reporter.save(result)
    pdf_file = pdf_reporter.save(result)

    print("\n=== REPORTS GENERATED ===")
    print(f"- {json_file}")
    print(f"- {pdf_file}")

if __name__ == "__main__":
    main()