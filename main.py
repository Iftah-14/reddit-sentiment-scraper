from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)  # ✅ This must come before any @app.route

@app.route('/')
def index():
    return '✅ Flask is running. Use /scrape?ticker=NVDA'

@app.route('/scrape')
def scrape():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({'error': 'Ticker is required'}), 400

    try:
        result = subprocess.run(
            ['snscrape', '--jsonl', '--max-results', '50', 'reddit-subreddit:all'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        raw_posts = [json.loads(line) for line in result.stdout.strip().split("\n") if line]
        filtered = [
            post["content"] for post in raw_posts
            if ticker.lower() in post.get("content", "").lower()
        ]
        return jsonify({'ticker': ticker, 'reddit_posts': filtered[:20]})

    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Failed to scrape Reddit posts', 'details': e.stderr}), 500

# Optional: only for local debugging
# if __name__ == "__main__":
#     app.run(debug=True)
