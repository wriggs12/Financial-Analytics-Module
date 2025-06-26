from dotenv import load_dotenv
import requests
import os

load_dotenv()

def fetch_stock_data(ticker: str):
    response = requests.get(f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={os.environ.get("API_KEY")}")
    return response.json()


def fetch_stock_data_bulk(tickers: list[str]):
    data = [
        fetch_stock_data(ticker)
        for ticker in tickers
    ]

    return data
