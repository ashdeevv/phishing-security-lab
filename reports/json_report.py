import json
from datetime import datetime

class JSONReporter:
    def __init__(self, base_name="phishing_report"):
        self.base_name = base_name

    def save(self, data: dict) -> str:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.base_name}_{timestamp}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"[+] JSON report saved: {filename}")
        return filename