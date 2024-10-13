import datetime

import pandas as pd


def get_stock_today_news(news_df: pd.DataFrame):
    recent_news = []

    for i, news in news_df.iterrows():
        if pd.Timestamp(news['Date']).date() == datetime.datetime.now().date():
            recent_news.append(news['Link'])

    return recent_news
