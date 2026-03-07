import os

# lightweight wrapper around OpenAI ChatCompletion
# requires OPENAI_API_KEY set in environment or .env

try:
    import openai
except ImportError:
    openai = None


def ensure_openai():
    if openai is None:
        raise RuntimeError("openai package not installed; run 'pip install openai'")
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_insight(query: str, search_result: dict, analysis: str) -> str:
    """Generate a human-readable response using an LLM based on search and analysis.

    query: the original user query (ticker or company name)
    search_result: object returned from google_search (has 'results' key with snippet text)
    analysis: string result from analyze_stock_performance
    """
    ensure_openai()

    prompt = f"""
You are a friendly financial assistant. A user asked about this stock or company: {query}

Here are the search snippets you retrieved:
{search_result.get('results', '')}

And here is the historical analysis you computed:
{analysis}

Compose a concise summary that explains the current situation, highlights any key metrics
(from the analysis), and gives a high-level recommendation or next step. Keep tone helpful and
clear. Avoid giving explicit financial advice.
"""
    # use ChatCompletion API
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful stock analysis assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.7,
        timeout=10  # Add timeout to prevent hanging
    )
    return response.choices[0].message["content"].strip()
