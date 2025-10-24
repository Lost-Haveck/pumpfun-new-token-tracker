# Pump.fun New Token Tracker

A Python WebSocket listener that detects newly launched tokens on **Pump.fun** before they appear on the website.  
It classifies tokens in real time as **Trusted**, **Suspect**, or **High Alert** based on market cap thresholds and logs each event to the console.

---

## 🚀 Features
- Real-time WebSocket connection to Pump.fun
- Auto-classifies tokens by market cap:
  - 🟥 **High Alert:** 100+ SOL
  - 🟪 **Trusted:** 30–99 SOL
  - 🟦 **Suspect:** 1–30 SOL
- Timestamped log output
- Auto-reconnect system with exponential backoff

---

## 🛠️ Requirements
Python 3.9 or later  
Install dependencies:
```bash
pip install -r requirements.txt
