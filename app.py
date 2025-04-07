from flask import Flask, render_template, request
import requests

app = Flask(__name__)

ELASTIC_URL = "http://localhost:9200/_search"

@app.route("/", methods=["GET"])
def search():
    query = request.args.get("q", "")
    results = []

    if query:
        payload = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "content"],
                }
            }
        }
        try:
            res = requests.post(ELASTIC_URL, json=payload)
            res.raise_for_status()
            data = res.json()
            results = data.get("hits", {}).get("hits", [])
        except Exception as e:
            print("Błąd podczas zapytania do Elasticsearch:", e)

    return render_template("search.html", query=query, results=results)

if __name__ == "__main__":
    app.run(debug=True)
