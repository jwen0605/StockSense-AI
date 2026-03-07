from flask import Flask, render_template, request, jsonify
import os
from search import google_search, analyze_stock_performance, lookup_ticker
from llm import generate_insight

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    """Render the front-end page. Client handles form submission via JavaScript."""
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search_api():
    """AJAX endpoint: return search and analysis data as JSON."""
    data = request.get_json() or {}
    query = data.get('query', '').strip()
    if not query:
        return jsonify(error="No query provided"), 400

    search_text = f"{query} stock price today"
    result = google_search(search_text)
    ticker = lookup_ticker(query)
    if not ticker:
        analysis = f"Unable to resolve '{query}' to a ticker symbol. Please try a valid ticker or company name."
    else:
        analysis = analyze_stock_performance(query)

    # if we have an LLM available, add a natural-language summary
    try:
        summary = generate_insight(query, result, analysis)
    except Exception as e:
        summary = f"(LLM unavailable: {e})"

    return jsonify(result=result, ticker=ticker, analysis=analysis, llm_summary=summary)

if __name__ == '__main__':
    # Running with debug enabled for development; turn off in production.
    # Use a port other than 5000/5001 which macOS sometimes reserves.
    # Allow overriding via the PORT environment variable (useful for deployment).
    base_port = int(os.getenv('PORT', 5003))
    # try a handful of consecutive ports; if all are busy, fall back to an
    # ephemeral port (0) so the server always starts somewhere.
    for offset in range(0, 10):
        port = base_port + offset
        try:
            print(f"attempting to start server on port {port}…")
            app.run(host='0.0.0.0', port=port, debug=True)
            break  # if app.run returns normally (e.g. shutdown), exit loop
        except OSError as exc:
            if "Address already in use" in str(exc):
                print(f"port {port} is busy, trying next")
                continue
            else:
                raise
    else:
        # if we exhausted the loop without breaking, try an ephemeral port
        print("all preferred ports busy, falling back to an ephemeral port")
        app.run(host='0.0.0.0', port=0, debug=True)
