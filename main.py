from flask import Flask, request, jsonify
import praw

app = Flask(__name__)

# Reddit API credentials
reddit = praw.Reddit(
    client_id="YLxAAUb0IJy4Okz7Tvhcfg",
    client_secret="e30IywaS21aAhSYy0XAm6i2dFz3EZw",
    user_agent="StockSentimentAI/0.1 by Wonderful_Wash7798"
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
        for submission in reddit.subreddit("all").search(
            query=ticker,
            sort='new',
            limit=20,
            params={'timeout': 10}  # ⏱️ added timeout to avoid hanging
        ):
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
