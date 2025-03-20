from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("q")
    api_key = "48ff2f8522af691f7a1e41c65f454bda076373ce78849652c75d4c3fec14e482"
    url = f"https://serpapi.com/search.json"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    params = {
        "engine": "google_play",
        "q": query,
        "gl": "us",
        "start": 0,
        "api_key": api_key
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        print("API Response:", data)

        results = []
        
        if "app_highlight" in data:
            app = data["app_highlight"]
            results.append({
                "title": app.get("title", "Unknown"),
                "author": app.get("author", "Unknown"),
                "rating": app.get("rating", "N/A"),
                "thumbnail": app.get("thumbnail", ""),
                "link": app.get("link", "#")
            })
            

        if "organic_results" in data and len(data["organic_results"]) > 0:
            for item in data["organic_results"][0].get("items", []):
                results.append({
                    "title": item.get("title", "Unknown"),
                    "author": item.get("author", "Unknown"),
                    "rating": item.get("rating", "N/A"),
                    "thumbnail": item.get("thumbnail", ""),
                    "link": item.get("link", "#")
                })

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)

