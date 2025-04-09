from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/bybit")
def bybit_proxy():
    q = request.query_string.decode()
    if not q:
        return jsonify({"error": "missing query parameters"}), 400

    url = f"https://api.bytick.com/v5/market/kline?{q}"
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return jsonify({
            "error": "Invalid response from Bybit",
            "details": str(e),
            "text": r.text if r else "No response"
        }), 500

@app.route("/")
def home():
    return "✅ NEURAL EDGE PROXY is LIVE via Fly.io"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Fly passes 8080
    app.run(host="0.0.0.0", port=port)
