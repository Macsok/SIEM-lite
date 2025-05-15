# Tylko dla linuksowych bo tam są jakies symulujace ataki

# incident_detection.py
import pandas as pd

def load_logs(csv_path="../logs/Linux/Linux_2k.log_structured.csv"):
    df = pd.read_csv(csv_path)
    alerts = []

    for _, row in df.iterrows():
        content = str(row["Content"]).lower()

        if "authentication failure" in content:
            alerts.append({
                "type": "Authentication failure",
                "severity": "high",
                "time": f"{row['Month']} {row['Date']} {row['Time']}",
                "message": row["Content"],
                "status": "open",
                "Note": None
            })

        if "user unknown" in content:
            alerts.append({
                "type": "Login to Unknown User",
                "severity": "medium",
                "time": f"{row['Month']} {row['Date']} {row['Time']}",
                "message": row["Content"]
            })

    return alerts

# print(load_logs())