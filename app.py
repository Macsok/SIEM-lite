from flask import Flask, render_template, request
import requests

app = Flask(__name__)

ELASTIC_URL = "http://localhost:9200/loghub-logs-*/_search"

@app.route("/", methods=["GET", "POST"])
def search():
    query = ""
    results = []
    error = None

    if request.method == "POST":
        query = request.form.get("query", "")
        field = request.form.get("field", "").strip()
        size = request.form.get("size", "10")

        if field:
            payload = {
                "query": {
                    "match_phrase": {
                        field: query
                    }
                },
                "size": int(size)
            }
        else:
            payload = {
                "query": {
                "query_string": {
                    "query": f"*{query}*"
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

    return render_template("search.html", query=query, results=results, error=error)

if __name__ == "__main__":
    app.run(debug=True)
