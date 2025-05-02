import snscrape.modules.twitter as sntwitter
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Twitter Scraper is running! Use /scrape?ticker=AAPL"

@app.route('/scrape')
def scrape():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({'error': 'Missing ticker param'}), 400

    query = f"{ticker} lang:en"
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= 20:
            break
        tweets.append(tweet.content)

    return jsonify({'ticker': ticker, 'tweets': tweets})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
