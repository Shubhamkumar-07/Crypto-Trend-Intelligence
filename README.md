# HypeShield AI - Meme Coin Bubble & Crash Predictor

HypeShield AI is a full-stack Python project built with FastAPI and Streamlit. It tracks meme coin chatter from Twitter/X and Reddit when API credentials are available, and falls back to a realistic simulated social stream when they are not.

## What it does

- Collects posts about meme coins such as `DOGE`, `SHIB`, `PEPE`, `FLOKI`, `BONK`, and `WIF`
- Cleans text and detects coin mentions
- Scores sentiment with VADER and a lightweight fallback when NLTK data is unavailable
- Calculates fake hype using repetition rate, new account ratio, and engagement anomalies
- Detects trend strength, mention velocity, and spike behavior
- Predicts pump probability and crash probability
- Classifies hype lifecycle stage: Early, Viral, Peak, Stable, or Dump
- Generates real-time alerts for fake hype, emerging momentum, viral growth, and crash risk
- Visualizes everything in a dark, crypto-styled Streamlit dashboard

## Folder structure

```text
crypto/
├── app.py
├── requirements.txt
├── README.md
├── frontend/
│   ├── __init__.py
│   └── app.py
└── backend/
    └── app/
        ├── main.py
        ├── models/
        │   ├── alert.py
        │   ├── analysis_result.py
        │   └── coin_data.py
        ├── routers/
        │   ├── alerts.py
        │   ├── analyze.py
        │   └── coins.py
        └── services/
            ├── alert_system.py
            ├── analysis_engine.py
            ├── data_collection.py
            ├── data_processing.py
            ├── fake_hype_detection.py
            ├── hype_lifecycle.py
            ├── prediction_engine.py
            ├── sentiment_analysis.py
            └── trend_detection.py
```

## API endpoints

- `GET /api/coins`
- `GET /api/analyze/{coin}`
- `GET /api/alerts`
- `GET /api/alerts?coin=DOGE`

## Environment variables for live APIs

Twitter/X with Tweepy:

- `TWITTER_BEARER_TOKEN`

Reddit with PRAW:

- `REDDIT_CLIENT_ID`
- `REDDIT_CLIENT_SECRET`
- `REDDIT_USER_AGENT`

If these are not set, the backend automatically switches to realistic simulated data.

## Installation

```bash
pip install -r requirements.txt
```

## Run the backend

```bash
cd backend
uvicorn app.main:app --reload
```

## Run the frontend

From the project root:

```bash
streamlit run app.py
```

Alternative:

```bash
cd frontend
streamlit run app.py
```

## Demo notes

- The simulator creates believable social bursts, sentiment flips, and engagement anomalies to make the hackathon demo smooth even without API keys.
- `data_mode` in `/api/coins` tells you whether the app is using `live` or `simulated` data.
- The dashboard auto-refreshes so the metrics feel live during a demo.
