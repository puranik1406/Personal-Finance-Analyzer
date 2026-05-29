# Personal-Finance-Analyzer

### AI-Powered Financial Insights. 100% Private.

Private Finance Analyzer is a privacy-first financial analysis application that helps users understand spending habits, identify recurring expenses, and generate personalized financial insights using **Google's Gemma model running locally through Ollama**.

Unlike traditional AI-powered finance tools, all processing happens entirely on the user's device. No financial data is uploaded to cloud servers, ensuring complete privacy and control over sensitive information.

---

## The Problem

Most AI-powered financial tools require users to upload bank statements and transaction histories to external servers.

Financial records contain highly sensitive information such as:

* Income
* Spending habits
* Subscriptions
* Healthcare expenses
* Travel history
* Personal purchases

Many users are uncomfortable sharing this information with third-party cloud providers.

---

## The Solution

Private Finance Analyzer uses **Gemma running locally** to provide intelligent financial analysis without sending any data outside the device.

```text
User Data
    ↓
Local FastAPI Backend
    ↓
Local Ollama Server
    ↓
Gemma
    ↓
Financial Insights
```

No cloud APIs.

No external storage.

No data sharing.

---

## Why Gemma?

This project demonstrates one of the most important use cases of local AI.

### Privacy First

Financial data never leaves the user's machine.

### Offline Operation

Works completely offline after setup.

### No API Costs

Unlimited inference with no recurring charges.

### Natural Language Understanding

Gemma can interpret transaction descriptions such as:

```text
UPI SWIGGY PAYMENT
NETFLIX.COM PAYMENT
AMZN MKTP IN
SHELL OIL STATION
```

and convert them into meaningful financial categories and insights.

### Local AI for Sensitive Data

Applications involving financial, medical, legal, academic, or personal information benefit significantly from local AI because privacy is a requirement rather than a feature.

---

## Features

### Transaction Categorization

Automatically classifies expenses into:

* Food & Dining
* Shopping
* Transportation
* Utilities
* Entertainment
* Healthcare
* Education
* Income
* Other

### Financial Summary

Generate:

* Total Income
* Total Expenses
* Net Savings
* Top Spending Categories
* Spending Distribution

### AI-Powered Insights

Using Gemma:

* Spending pattern analysis
* Unusual expense detection
* Subscription identification
* Personalized saving recommendations
* Monthly financial summaries

### Privacy Dashboard

Clearly shows that all processing occurs locally and no information is transmitted externally.

---

## Tech Stack

### Frontend

* React
* Tailwind CSS

### Backend

* FastAPI
* Python

### AI

* Gemma
* Ollama

### Data Processing

* Pandas

---

## Running Locally

### Install Ollama

```bash
ollama pull gemma:e2b
```

### Start Gemma

```bash
ollama run gemma:e2b
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start Backend

```bash
uvicorn main:app --reload
```

### Start Frontend

```bash
npm install
npm run dev
```

---

## Sample Workflow

1. Upload a bank statement (CSV)
2. Transactions are parsed locally
3. Gemma categorizes spending
4. Financial summaries are generated
5. AI-powered insights are displayed
6. Data remains on the user's device throughout the process

---

## Future Improvements

* PDF bank statement support
* Multi-bank compatibility
* Budget planning
* Expense forecasting
* Investment tracking
* Personal finance chatbot powered by local Gemma
* Advanced anomaly detection

---

## Project Goal

This project is not simply a finance analyzer that uses AI.

It is a demonstration of how modern AI applications can be built using **local language models**, enabling intelligent analysis while preserving user privacy.

By combining financial analytics with Google's Gemma model, Private Finance Analyzer showcases a future where users do not have to trade privacy for intelligence.

---

## License

MIT License
