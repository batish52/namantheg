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
    print(f"[PROXY] → {url}")
    try:
        r = requests.get(url)
        print("[BYBIT RAW RESPONSE]", r.status_code, r.text[:500])  # limit output

        # Try parsing as JSON, fallback to raw output
        try:
            return r.json()
        except Exception as json_err:
            return jsonify({
                "error": "Invalid JSON from Bybit",
                "status_code": r.status_code,
                "text": r.text[:500]
            }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "✅ NEURAL EDGE PROXY IS LIVE"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
