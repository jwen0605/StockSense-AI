import os
from search import google_search as _google_search, analyze_stock_performance as _analyze_stock

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

SYSTEM_PROMPT = """You are a knowledgeable personal finance assistant. You have access to real-time web search and stock analysis tools.

When users ask about stocks, companies, or market data:
- Use google_search_tool to get the latest news and prices
- Use analyze_stock_performance_tool for historical metrics and trends
- Combine both sources for a well-rounded answer

For general finance questions (budgeting, investing concepts, etc.) you can answer from your training knowledge.
Always be concise, accurate, and remind users that nothing you say is financial advice."""


def google_search_tool(query: str) -> str:
    """Search the web for real-time stock prices, financial news, and market data.

    Args:
        query: The search query, e.g. 'NVIDIA stock price today'
    """
    print(f"[Tool] google_search({query!r})")
    return _google_search(query).get("results", "No results found.")


def analyze_stock_performance_tool(ticker_or_name: str) -> str:
    """Analyze a stock's historical performance over the past 12 months.
    Returns current price, total return %, annualized volatility, 52-week high/low,
    and a buy/hold/sell recommendation.

    Args:
        ticker_or_name: Stock ticker symbol (e.g. 'NVDA') or company name (e.g. 'NVIDIA')
    """
    print(f"[Tool] analyze_stock_performance({ticker_or_name!r})")
    return _analyze_stock(ticker_or_name)


def _get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    if genai is None:
        raise RuntimeError("google-genai not installed; run: pip3 install google-genai")
    return genai.Client(api_key=api_key)


def _to_genai_history(history: list) -> list:
    return [
        types.Content(
            role="model" if msg["role"] == "assistant" else "user",
            parts=[types.Part(text=msg["content"])]
        )
        for msg in history
    ]


def chat(history: list, user_message: str) -> str:
    """Multi-turn chat. history is a list of {role, content} plain-text dicts."""
    client = _get_client()
    session = client.chats.create(
        model="gemini-2.5-flash",
        history=_to_genai_history(history),
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[google_search_tool, analyze_stock_performance_tool],
        ),
    )
    return session.send_message(user_message).text
