from flask import Flask, request, jsonify
import praw
import time

app = Flask(__name__)

# Reddit API credentials
reddit = praw.Reddit(
    client_id="YLxAAUbOlJy4Okz7Tvhcfg",
    client_secret="e30IywaS21aAhSYy0XAm6i2dFz3EZw",
    user_agent="StockSentimentAI/0.1 (by Wonderful_Wash7798)"
)

@app.route('/')
def home():
    return "✅ Reddit sentiment scraper is running. Use /scrape?ticker=AAPL"

@app.route('/scrape')
def scrape():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({'error': 'Missing ticker'}), 400

    posts = []
    try:
        # Calculate the timestamp for 3 days ago
        three_days_ago = time.time() - (3 * 24 * 60 * 60)

        for submission in reddit.subreddit("all").search(ticker, sort='new', limit=100):
            if submission.created_utc >= three_days_ago:
                posts.append({
                    'title': submission.title,
                    'text': submission.selftext,
                    'url': submission.url,
                    'score': submission.score,
                    'created_utc': submission.created_utc,
                    'subreddit': submission.subreddit.display_name
                })

        return jsonify({'ticker': ticker, 'posts': posts})
    except Exception as e:
        return jsonify({'error': 'Failed to fetch Reddit posts', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
