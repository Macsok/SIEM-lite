import os
import json
from datetime import datetime

ALERTS_FILE = "utils/alerts.json"

def add_alert(alert):
    alerts = []
    if os.path.exists(ALERTS_FILE):
        with open(ALERTS_FILE, "r", encoding="utf-8") as f:
            alerts = json.load(f)

    alerts.append(alert)

    with open(ALERTS_FILE, "w", encoding="utf-8") as f:
        json.dump(alerts, f, indent=2)


def generate_alert_from_ai_response(text: str):
    """
    Tworzy strukturę alertu na podstawie odpowiedzi od AI.
    """
    lowered = text.lower()
    alert_type = "General AI Alert"
    severity = "medium"

    if "brute force" in lowered or "many authentication failure" in lowered:
        alert_type = "Brute-force Attack Suspected"
        severity = "high"
    elif "denial of service" in lowered or "dos" in lowered:
        alert_type = "Possible DoS Attack"
        severity = "high"
    elif "privilege escalation" in lowered:
        alert_type = "Privilege Escalation"
        severity = "high"
    elif "suspicious login" in lowered or "login to unknown user" in lowered:
        alert_type = "Suspicious Login Detected"
        severity = "medium"
    elif "scan" in lowered or "port scan" in lowered:
        alert_type = "Scanning Activity"
        severity = "low"

    return {
        "type": alert_type,
        "severity": severity,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": text
    }
