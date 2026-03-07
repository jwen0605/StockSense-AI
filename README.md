# StockSense AI

A personal finance assistant web app powered by **Gemini 2.5 Flash** with real-time stock data and AI-driven tool use.

<p align="center">
  <img src="Demo.png" alt="StockSense AI Demo" />
</p>

---

## Features

- **Conversational AI** — Chat with a finance assistant that remembers context across messages
- **Real-time Search** — Fetches latest stock prices and news via the Serper (Google Search) API
- **Historical Analysis** — 12-month performance metrics via Yahoo Finance: return %, volatility, 52-week high/low, and a BUY / HOLD / SELL recommendation
- **Agentic Tool Use** — Gemini automatically decides when to call search and analysis tools
- **Finance-styled UI** — Dark theme chat interface with colored recommendation badges and highlighted numbers

---

## Architecture

```
app.py          Flask web server — serves UI and /chat endpoint
llm.py          Gemini 2.5 Flash with tool use (google_search, analyze_stock_performance)
search.py       Serper API (web search) + Yahoo Finance (stock data)
templates/
  index.html    Chat UI frontend
```

---

## Setup

### 1. Get API Keys

| Key | Where to get it |
|-----|----------------|
| `SERPER_API_KEY` | [serper.dev](https://serper.dev) |
| `GEMINI_API_KEY` | [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) |

### 2. Create `.env` in the project root

```
SERPER_API_KEY=your_serper_key_here
GEMINI_API_KEY=your_gemini_key_here
```

### 3. Install dependencies

```bash
pip3 install flask python-dotenv requests yfinance google-genai
```

### 4. Run

```bash
python3 app.py
```

Open [http://localhost:5003](http://localhost:5003) in your browser.

---

## How It Works

```
User: "Should I buy NVIDIA?"
  ↓
Gemini calls → google_search_tool("NVIDIA stock price today")
             → analyze_stock_performance_tool("NVDA")
             → reads both results
             → writes final answer with price, metrics, and recommendation
  ↓
UI renders reply with colored STRONG BUY / HOLD / SELL badges and green/red numbers
```

---

## Notes

- Not financial advice — always do your own research
- API rate limits apply to Serper and Gemini
- Port defaults to `5003`; override with `PORT=5004 python3 app.py`
