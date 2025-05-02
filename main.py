import snscrape.modules.twitter as sntwitter
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

    query = f"{ticker} lang:en"
    try:
        tweets = []
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            if i >= 20:
                break
            tweets.append(tweet.content)
        return jsonify({'ticker': ticker, 'tweets': tweets})
    except Exception as e:
        return jsonify({'error': 'Failed to scrape tweets', 'details': str(e)}), 500
