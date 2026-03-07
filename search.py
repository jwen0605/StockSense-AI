import requests
import json
import os
from dotenv import load_dotenv
import yfinance as yf
from datetime import datetime, timedelta

load_dotenv()  # Load environment variables from .env file

def google_search(query):
    """Call Serper API for Google search"""
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': os.getenv("SERPER_API_KEY"),  # Add this key to .env file
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
    # Simplify results, return only top 3 organic search snippets to AI
    search_results = response.json()
    snippets = [item.get('snippet', '') for item in search_results.get('organic', [])[:3]]
    return {"results": "\n".join(snippets)}

def get_stock_history(ticker, months=12):
    """Get stock price history for the past N months"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months*30)  # Approximate months to days

    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_date, end=end_date)

    if hist.empty:
        return None

    return {
        'current_price': hist['Close'].iloc[-1] if not hist.empty else None,
        'start_price': hist['Close'].iloc[0] if not hist.empty else None,
        'history': hist
    }

def lookup_ticker(query):
    """Try to resolve a company name or ticker string into a valid ticker symbol.

    This uses Yahoo Finance's search API provided by yfinance. If the query is
    already a well‑formed ticker the search will usually return it as the first
    result, otherwise we fall back to the top equity result for the name.
    Returns the symbol string or ``None`` if nothing sensible is found.
    """
    # attempt a search; yfinance will even accept tickers directly
    try:
        search = yf.Search(query).search()
        quotes = search.quotes
        if quotes:
            # pick the first equity-like result
            for item in quotes:
                if item.get('quoteType') == 'EQUITY':
                    return item.get('symbol')
            # if no equity was found, just return the first symbol anyway
            return quotes[0].get('symbol')
    except Exception:
        pass
    return None


def analyze_stock_performance(ticker_or_name):
    """Analyze stock performance over past 12 months and provide recommendation.

    ``ticker_or_name`` may be either a ticker symbol (e.g. "AAPL") or a company
    name ("Apple"). We attempt to resolve it to a ticker before fetching
    historical data. If resolution fails the analysis will indicate the problem.
    """
    symbol = lookup_ticker(ticker_or_name)
    if not symbol:
        return f"Unable to resolve '{ticker_or_name}' to a ticker symbol."

    data = get_stock_history(symbol, 12)
    if not data or data['history'].empty:
        return f"Unable to retrieve stock data for '{symbol}'."

    hist = data['history']
    current_price = data['current_price']
    start_price = data['start_price']

    # Calculate metrics
    total_return = ((current_price - start_price) / start_price) * 100
    volatility = hist['Close'].pct_change().std() * (252 ** 0.5) * 100  # Annualized volatility
    max_price = hist['Close'].max()
    min_price = hist['Close'].min()

    # Simple recommendation logic
    if total_return > 20 and volatility < 30:
        recommendation = "BUY - Strong performance with moderate risk"
    elif total_return > 10:
        recommendation = "HOLD - Decent returns, monitor closely"
    elif total_return < -10:
        recommendation = "SELL - Significant decline, consider exiting"
    else:
        recommendation = "HOLD - Stable performance, wait for clearer trends"

    summary = f"""
Stock Analysis for {symbol.upper()} (Past 12 Months):
- Current Price: ${current_price:.2f}
- Starting Price: ${start_price:.2f}
- Total Return: {total_return:.2f}%
- Annualized Volatility: {volatility:.2f}%
- 52-Week High: ${max_price:.2f}
- 52-Week Low: ${min_price:.2f}
- Recommendation: {recommendation}

Note: This is not financial advice. Please consult a financial advisor.
"""

    return summary.strip()