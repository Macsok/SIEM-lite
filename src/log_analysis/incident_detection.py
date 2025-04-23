import re
from datetime import datetime

def technical_incident_detection(file_path_for_logs):
    alerts = []
    with open(file_path_for_logs, "r", encoding="utf-8") as file:
        for line in file:
            find_timestamp_in_log = re.match(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", line)
            if find_timestamp_in_log:
                timestamp = find_timestamp_in_log.group(1)
            else:
                "No timestamp detected"

            if "Failed to upload" in line or "Failed to start upload" in line:
                alerts.append({
                    "timestamp": timestamp,
                    "event_type": "SQM Upload Failure",
                    "severity": "low",
                    "message": line.strip()
                })

            elif "Warning: Unrecognized packageExtended attribute" in line:
                alerts.append({
                    "timestamp": timestamp,
                    "event_type": "Malformed Attribute",
                    "severity": "low",
                    "message": line.strip()
                })

    return alerts
