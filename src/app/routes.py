from flask import Blueprint, jsonify, request

from db.news import get_tickers_in_db, add_ticker_to_watch, clear_all_data, remove_ticker_to_watch
from news_scrapper.openai.news_prediction import get_prediction_from_llm
from watch.watch_news import create_wpp_msg

news_routes = Blueprint('news_routes', __name__)


@news_routes.route('/news', methods=['GET'])
def news():
    try:
        data = request.get_json()
        ticker = data.get('ticker')
        url = data.get('url')
        prediction = get_prediction_from_llm(url, ticker)

        return jsonify({"message": create_wpp_msg(ticker, url, prediction)}), 200
    except Exception as e:
        return jsonify({"error": "Unable to process request", "message": str(e)}), 400


@news_routes.route('/get-tickers', methods=['GET'])
def get_tickers():
    jsonify(get_tickers_in_db())


@news_routes.route('/add-ticker', methods=['POST'])
def add_ticker():
    try:
        data = request.get_json()
        ticker = data.get('ticker')

        add_ticker_to_watch(ticker)

        return jsonify({"ticker": ticker}), 200
    except Exception as e:
        return jsonify({"error": "Unable to process request", "message": str(e)}), 400


@news_routes.route('/remove-ticker', methods=['POST'])
def remove_ticker():
    try:
        data = request.get_json()
        ticker = data.get('ticker')

        remove_ticker_to_watch(ticker)

        return jsonify({"ticker": ticker}), 200
    except Exception as e:
        return jsonify({"error": "Unable to process request", "message": str(e)}), 400


@news_routes.route('/clear-news', methods=['GET'])
def clear_news():
    try:
        clear_all_data()

        return jsonify({}), 200
    except Exception as e:
        return jsonify({"error": "Unable to process request", "message": str(e)}), 400
