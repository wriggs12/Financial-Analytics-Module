import os

import finnhub
from dotenv import load_dotenv

load_dotenv()

client = finnhub.Client(api_key=os.environ.get("FINNHUB_API_KEY"))


def fetch_stock_data_bulk(tickers: list[str]):
    data = []
    
    for ticker in tickers:
        equity_data = client.quote(ticker)
        equity_data["symbol"] = ticker

        data.append(equity_data)
        
    return data
