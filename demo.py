import json
import os
from search import google_search, analyze_stock_performance
from llm import generate_insight

# Load tool schema from file
with open('tool_schema.json', 'r') as f:
    tool_schema = json.load(f)

def simulate_ai_response(user_query):
    """
    Simulate AI thinking and actions
    """
    print(f"User asks: {user_query}")
    print("AI thinks: My training data doesn't have today's real-time stock price information.")
    print("AI action: Generates a tool_call to invoke Google Search(query=\"NVIDIA stock price today\").")

    # Assume AI decides to call the tool
    tool_call = {
        "name": "google_search",
        "arguments": {
            "query": "NVIDIA stock price today"
        }
    }

    # Execute tool call
    result = google_search(tool_call["arguments"]["query"])
    print(f"Program: Fetches search results from the web (e.g., {result['results']}).")

    # Research layer: Analyze stock performance
    print("AI thinks: Now I should analyze the stock's historical performance for better context.")
    analysis = analyze_stock_performance("NVDA")  # NVIDIA ticker
    print("Program: Performs analysis of past 12 months performance.")

    # generate an LLM summary if possible
    try:
        llm_response = generate_insight(user_query, result, analysis)
        print("AI response: " + llm_response)
    except Exception as e:
        print(f"AI response (no LLM): Based on the latest information I just queried, NVIDIA's stock price today is approximately {result['results']}\n\n{analysis}")
        print(f"(LLM error: {e})")

if __name__ == "__main__":
    # Check API KEY
    if not os.getenv("SERPER_API_KEY"):
        print("Please set the environment variable SERPER_API_KEY")
        exit(1)

    user_query = "What is NVIDIA's stock price today?"
    simulate_ai_response(user_query)