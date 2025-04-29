"""
Description: Fetch 5-year historical stock data from Nasdaq API and compute stats.
Author: Harneet Randhawa
Date: 02-06-2025
AI: ChatGPT
"""
import sys
import requests
from datetime import datetime

def date_n_years_ago(n):
    today = datetime.today().date()
    try:
        past_date = today.replace(year=today.year - n)
    except ValueError:
        past_date = today.replace(year=today.year - n, day=today.day - 1)
    return past_date

def download_data(ticker):
    start_date = date_n_years_ago(5).strftime("%Y-%m-%d")
    url = f"https://api.nasdaq.com/api/quote/{ticker}/historical?assetclass=stocks&fromdate={start_date}&limit=9999"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

if __name__ == "__main__":
    for ticker in sys.argv[1:]:
        ticker = ticker.upper().strip()
        print(f"Fetching data for {ticker}...")
        data = download_data(ticker)
        if data:
            print(data)  # just print raw data for now