from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/bybit")
def bybit_proxy():
    q = request.query_string.decode()
    if not q:
        return jsonify({"error": "missing query parameters"}), 400

    url = f"https://api.bytick.com/v5/market/kline?{q}"
    print(f"[PROXY] → {url}")
    try:
        r = requests.get(url)
        return r.json()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "✅ NEURAL EDGE PROXY is live"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
