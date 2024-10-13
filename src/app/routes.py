from flask import Blueprint, jsonify, request

from db.news import get_tickers_in_db, remove_ticker_to_watch, add_ticker_to_watch, clear_all_data

news_routes = Blueprint('news_routes', __name__)


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
