from flask import Flask, render_template, request, jsonify
import requests

import sys
import os

# Konfiguracja ścieżek
SCRIPT_DIR = os.path.join(os.path.dirname(__file__), 'scripts')
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'web', 'templates')

sys.path.append(SCRIPT_DIR)

from scripts.incident_detection import load_logs
from scripts.llm_utils import analyze_log_with_llm

app = Flask(__name__, template_folder=TEMPLATE_DIR)

ELASTIC_URL = "http://localhost:9200/loghub-logs-*/_search"

@app.route("/", methods=["GET"])
def start_view():
    return render_template("home.html")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/file")
def file_selection():
    # Path to the folder where your log files are stored
    logs_folder = os.path.join(os.path.dirname(__file__), "logs")

    # Get the list of log files in the folder
    available_files = [f for f in os.listdir(logs_folder) if os.path.isfile(os.path.join(logs_folder, f))]

    return render_template("file.html", files=available_files)

@app.route("/search", methods=["GET", "POST"])
def search():
    query = ""
    field = ""
    use_regex = False
    results = []
    error = None
    size = 10

    if request.method == "POST":
        query = request.form.get("query", "")
        field = request.form.get("field", "").strip()
        size = request.form.get("size", "10")
        use_regex = request.form.get("use_regex", "off") == "on"

        if use_regex:
            field = f"*{field}*"
            query = f"*{query}*"

        if field:
            payload = {
                "query": {
                    "query_string": {
                        "default_field": field,
                        "query": query
                    }
                    # "term": {
                    #     f"{field}": query
                    # }
                },
                "size": int(size)
            }
        else:
            payload = {
                "query": {
                    "query_string": {
                        "query": '"' + query + '"'
                    }
                },
                "size": int(size)
            }

        try:
            res = requests.post(ELASTIC_URL, json=payload)
            res.raise_for_status()
            data = res.json()
            results = data.get("hits", {}).get("hits", [])
        except Exception as e:
            error = f"Error querying Elasticsearch: {e}"

    return render_template("search.html", query=query, field=field, size=size, use_regex=use_regex, results=results, error=error)

@app.route("/alerts")
def alerts():
    alerts = load_logs("logs/Linux/Linux_2k.log_structured.csv")
    return render_template("alerts.html", alerts=alerts)


@app.route("/analyze", methods=["GET", "POST"])
def recommendations_view():
    if request.method == "POST":
        try:
            # Ładujemy logi z pliku (zmień ścieżkę na odpowiednią)
            alerts = load_logs("logs/Linux/Linux_2k.log_structured.csv")

            # Wytwarzamy prompt na podstawie alertów
            log_text = "\n".join([alert["message"] for alert in alerts])

            # Wysyłamy logi do LLM
            analysis = analyze_log_with_llm(log_text)  # Wykorzystanie funkcji analizy

            return render_template("analyze.html", recommendations=analysis)
        except Exception as e:
            return render_template("analyze.html", error=f"Error: {str(e)}")

    # W przypadku GET, po prostu renderujemy pustą stronę
    return render_template("analyze.html")

def run_app():
    app.run(debug=True)

