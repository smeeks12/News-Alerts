from flask import Flask, render_template, jsonify
import yfinance as yf
import requests

app = Flask(__name__)
news_api_key = 'YOUR_NEWSAPI_KEY'

def get_fast_movers():
    tickers = ["TSLA", "NVDA", "AMD", "SPY", "META"]
    fast_movers = []

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d", interval="5m")

        if not hist.empty and hist["Volume"].iloc[-1] > hist["Volume"].mean() * 3:
            news = get_news(ticker)
            fast_movers.append({
                "ticker": ticker,
                "latest_price": hist["Close"].iloc[-1],
                "news": news
            })

    return fast_movers

def get_news(ticker):
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': ticker,
        'apiKey': news_api_key,
        'sortBy': 'publishedAt',
        'language': 'en',
        'pageSize': 3
    }
    res = requests.get(url, params=params)
    articles = res.json().get("articles", [])
    return [{"title": a["title"], "url": a["url"]} for a in articles]

@app.route('/')
def dashboard():
    return render_template("dashboard.html")

@app.route('/data')
def data():
    return jsonify(get_fast_movers())

if __name__ == '__main__':
    app.run(debug=True)
