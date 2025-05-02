from flask import Flask, request, jsonify
import subprocess
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Flask is running. Use /scrape?ticker=NVDA"

@app.route('/scrape')
def scrape():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({'error': 'Ticker is required'}), 400

    query = f"{ticker} lang:en"
    try:
        result = subprocess.run(
            ['snscrape', '--jsonl', '--max-results', '20', f'twitter-search:"{query}"'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        tweets = [json.loads(line)["content"] for line in result.stdout.strip().split("\n") if line]
        return jsonify({'ticker': ticker, 'tweets': tweets})

    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Failed to scrape tweets', 'details': e.stderr}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
