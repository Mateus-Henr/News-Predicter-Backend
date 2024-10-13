import time

from finvizfinance.util import web_scrap

from models.prediction import Prediction
from news_scrapper.openai.client import client
from news_scrapper.scrapper import get_stock_today_news


def is_news_element_in_url(url):
    return web_scrap(url).find("table", class_="fullview-news-outer") is not None


def retrieve_today_news(stock):
    if len(stock.today_news_links) != 0:
        return False

    time.sleep(0.5)
    if is_news_element_in_url(stock.quote_url):
        news = stock.ticker_news()

        if news is not None:
            today_news = get_stock_today_news(news)

            for news_link in today_news:
                stock.today_news_links.append(news_link)

            return True

    return False


def get_prediction_from_llm(link: str, ticker: str):
    prediction = client.chat.completions.create(
        model="gpt-4o",
        response_model=Prediction,
        messages=[{"role": "system",
                   "content": "Perform a detailed sentiment analysis on this stock news for " + ticker + " ticker, " +
                              "identifying whether the tone is positive, negative, or neutral. "
                              "Additionally, evaluate the alert level of the news, indicating how significantly it "
                              "may impact stock movement. "
                              "Make sure to use your browser capabilities on the following link: " + link}],
    )

    return prediction
