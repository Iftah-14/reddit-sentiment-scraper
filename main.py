import subprocess
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return '✅ Flask is running. Use /scrape?ticker=NVDA'

@app.route('/scrape')
def scrape():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({'error': 'Ticker is required'}), 400

    query = f'{ticker} site:reddit.com'
    try:
        result = subprocess.run(
            ['snscrape', '--jsonl', '--max-results', '20', f'reddit-search:"{query}"'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        posts = [
            json.loads(line).get("content", "") for line in result.stdout.strip().split("\n") if line
        ]
        return jsonify({'ticker': ticker, 'reddit_posts': posts})

    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Failed to scrape Reddit posts', 'details': e.stderr}), 500
