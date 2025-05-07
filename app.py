from flask import Flask, render_template, request, jsonify
import requests
from incident_detection import load_logs
from llm_utils import analyze_log_with_llm

app = Flask(__name__)

ELASTIC_URL = "http://localhost:9200/loghub-logs-*/_search"

@app.route("/", methods=["GET", "POST"])
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
                        "default_field ": field,
                        "query": query
                    }
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


@app.route('/analyze', methods=['POST'])
def analyze_endpoint():
    try:
        data = request.get_json()
        log_text = data.get('log_text', '')

        if not log_text:
            return jsonify({"error": "Brak log_text w żądaniu"}), 400

        analysis = analyze_log_with_llm(log_text)  # Wywołanie zgodnej funkcji
        return jsonify({"analysis": analysis})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
