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
from google import genai

app = Flask(__name__, template_folder=TEMPLATE_DIR)

ELASTIC_URL = "http://localhost:9200/loghub-logs-*/_search"

@app.route("/", methods=["GET"])
def start_view():
    return render_template("home.html")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/file", methods=["GET", "POST"])
def file_selection():
    # Path to the folder where your log files are stored
    logs_folder = os.path.join(os.path.dirname(__file__), "logs")
    
    # Get all log files recursively from the logs directory
    available_files = []
    for root, _, files in os.walk(logs_folder):
        for file in files:
            # Get relative path to make it easier to display
            rel_path = os.path.relpath(os.path.join(root, file), logs_folder)
            available_files.append(rel_path)
    
    logs = []
    selected_file = None
    
    if request.method == "POST":
        selected_file = request.form.get("selected_file")
        if selected_file:
            file_path = os.path.join(logs_folder, selected_file)
            try:
                # Check if this is a structured CSV file
                if selected_file.endswith('.csv'):
                    logs = load_logs(file_path)
                else:
                    # For raw text log files
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        log_lines = f.readlines()
                        logs = [{"Content": line.strip()} for line in log_lines]
            except Exception as e:
                logs = [{"Error": f"Failed to load logs: {str(e)}"}]
    
    return render_template("file.html", files=available_files, logs=logs, selected_file=selected_file)

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


@app.route("/analysis", methods=["GET", "POST"])
def analysis():
    # Implement your analysis view
    return render_template("analysis.html")

@app.route("/test_AI", methods=["GET", "POST"])
def test_ai():
    # Path to the folder where your log files are stored
    logs_folder = os.path.join(os.path.dirname(__file__), "logs")
    
    # Get all log files recursively from the logs directory
    available_files = []
    for root, _, files in os.walk(logs_folder):
        for file in files:
            # Get relative path to make it easier to display
            rel_path = os.path.relpath(os.path.join(root, file), logs_folder)
            available_files.append(rel_path)
    
    logs = []
    selected_file = None
    
    if request.method == "POST":
        selected_file = request.form.get("selected_file")
        if selected_file:
            file_path = os.path.join(logs_folder, selected_file)
            try:
                # Check if this is a structured CSV file
                if selected_file.endswith('.csv'):
                    logs = load_logs(file_path)
                else:
                    # For raw text log files
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        log_lines = f.readlines()
                        logs = [{"Content": line.strip()} for line in log_lines]
            except Exception as e:
                logs = [{"Error": f"Failed to load logs: {str(e)}"}]
    
    return render_template("test_AI.html", files=available_files, logs=logs, selected_file=selected_file)

@app.route("/analyze_log", methods=["POST"])
def analyze_log():
    try:
        data = request.get_json()
        log_content = data.get("log_content", "")
        # print(data)
        if not log_content:
            return jsonify({"error": "No log content provided"}), 400

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return jsonify({"error": "API key not found in environment variables"}), 500

        # Initialize the AI client
        client = genai.Client(api_key=api_key)

        # Log the received content for debugging
        print(f"Received log content: {log_content}")
        prompt = """Analyze log and give answer in pretty output (no latex format, only plain text, dont use stars, it is not markdown output).
        Give just analysis, dont display introduction sentence. Give some advice. Log: """
        + log_content

        # Generate AI response
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )

        # Log the AI response for debugging
        #print(f"AI response: {response.text}")

        return jsonify({"response": response.text})

    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        return jsonify({"error": str(e)}), 500

def run_app():
    app.run(debug=True)

