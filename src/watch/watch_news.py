import os
import time

import requests
from finvizfinance.quote import finvizfinance

from db.news import get_tickers_in_db, is_news_in_db, add_news_to_db
from models.prediction import Prediction
from news_scrapper.openai.news_prediction import get_prediction_from_llm

BASE_URL = os.environ.get("BASE_URL")


def create_wpp_msg(ticker: str, url: str, prediction: Prediction):
    return (
        f"📈 *Stock Alert:* {ticker}\n"
        f"*Prediction:* {prediction.prediction_value.value}\n"
        f"*Alert Level:* {prediction.alert_level.value} 🚨\n"
        "🔍 Details\n"
        f"URL: {url}"
    )


def send_message_to_wpp_server(message):
    url = f'{BASE_URL}/send-message'
    payload = {'message': message}
    headers = {'User-Agent': 'Chrome/123.0.0.0',
               'Accept-Language': 'en-US',
               'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print(f"Server response: {response.json()}")
        return True
    except Exception as e:
        print("error: " + str(e))


def watch():
    while True:
        for ticker in get_tickers_in_db():
            stock = finvizfinance(ticker)
            stock_news = stock.ticker_news()

            for i in range(min(len(stock_news), 5)):
                news_cell = stock_news.iloc[i]
                news_url = news_cell["Link"]

                if not is_news_in_db(news_url):
                    try:
                        prediction = get_prediction_from_llm(news_url, ticker)
                        if add_news_to_db(news_url):
                            send_message_to_wpp_server(create_wpp_msg(ticker, news_url, prediction))
                    except Exception as e:
                        print("ERROR", str(e))

            time.sleep(0.1)
        time.sleep(60)
