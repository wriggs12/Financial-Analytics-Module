import os

import finnhub
from dotenv import load_dotenv

load_dotenv()

client = finnhub.Client(api_key=os.environ.get("FINNHUB_API_KEY"))


def fetch_stock_data_bulk(tickers: list[str]):
    data = [client.quote(ticker) for ticker in tickers]

    return data
