from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import red, orange, green, black
from reportlab.pdfgen import canvas

class PDFReporter:
    def __init__(self, base_name="phishing_report"):
        self.base_name = base_name

    def _severity_color(self, level: str):
        level = level.upper()
        if level == "HIGH":
            return red
        if level == "MEDIUM":
            return orange
        return green

    def save(self, result: dict) -> str:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.base_name}_{timestamp}.pdf"

        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        # ========== PAGE 1 — COUVERTURE ==========
        c.setFont("Helvetica-Bold", 22)
        c.drawString(80, height - 120, "Phishing Detection Report")

        c.setFont("Helvetica", 12)
        c.drawString(80, height - 160, f"Analyzed URL: {result['url']}")
        c.drawString(80, height - 180, f"Generated: {datetime.utcnow().isoformat()} UTC")

        c.drawString(80, height - 240, f"Risk Level: {result['risk_level']}")
        c.drawString(80, height - 260, f"Risk Score: {result['risk_score']}")

        c.showPage()

        # ========== PAGE 2 — RÉSUMÉ EXÉCUTIF ==========
        c.setFont("Helvetica-Bold", 16)
        c.drawString(80, height - 100, "Executive Summary")

        c.setFont("Helvetica", 11)
        y = height - 140

        for reason in result["reasons"]:
            c.drawString(90, y, f"- {reason}")
            y -= 18
            if y < 80:
                c.showPage()
                y = height - 100

        c.showPage()

        # ========== PAGE 3 — TECHNICAL FINDINGS ==========
        c.setFont("Helvetica-Bold", 16)
        c.drawString(80, height - 100, "Technical Findings")

        c.setFont("Helvetica", 11)
        c.drawString(80, height - 140, f"Domain: {result['domain']}")
        c.drawString(80, height - 160, f"Similarity: {result['similarity_with_brand']}%")
        c.drawString(80, height - 180, f"Redirects: {result['redirect_chain']}")
        c.drawString(80, height - 200, f"IP in domain: {result['ip_in_domain']}")

        sh = result["security_headers"]
        c.drawString(80, height - 240, f"HSTS: {sh['hsts']}")
        c.drawString(80, height - 260, f"CSP: {sh['csp']}")
        c.drawString(80, height - 280, f"X-Frame-Options: {sh['x_frame']}")

        c.showPage()
        c.save()

        print(f"[+] PDF report saved: {filename}")
        return filename