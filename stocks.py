"""
Description: Fetch 5-year historical stock data from Nasdaq API and compute stats.
Author: Harneet Randhawa
Date: 02-06-2025
AI: ChatGPT
"""
import sys
import requests
import statistics
import json
from datetime import datetime

"""Calculate the date 'n' years ago from today. Handles leap years."""
def date_n_years_ago(n):
    today = datetime.today().date()
    try:
        past_date = today.replace(year=today.year - n)
    except ValueError:
        # Handle February 29 for non-leap years by adjusting day
        past_date = today.replace(year=today.year - n, day=today.day - 1)
    return past_date

"""Download historical stock data for a given ticker from Nasdaq."""
def download_data(ticker):
    start_date = date_n_years_ago(5).strftime("%Y-%m-%d")  # Start from 5 years ago
    url = f"https://api.nasdaq.com/api/quote/{ticker}/historical?assetclass=stocks&fromdate={start_date}&limit=9999"
    
    # Set headers to mimic a browser to avoid request blocking
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception if HTTP request failed
        return response.json()
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

"""Extract closing prices from the downloaded stock data, and compute min, max, average, and median statistics."""
def process_data(data):
    try:
        # Navigate to historical price records
        rows = data["data"]["tradesTable"]["rows"]
    except (KeyError, TypeError) as e:
        print(f"Data format error: {e}")
        return None

    closing_prices = []

    for entry in rows:
        if "close" in entry:
            price_str = entry["close"]
            try:
                # Remove $ and commas, convert to float
                price = float(price_str.replace("$", "").replace(",", "").strip())
                closing_prices.append(price)
            except ValueError:
                continue  # Skip if conversion fails

    if not closing_prices:
        return None  # No valid closing prices found

    # Calculate statistics
    stats = {
        "min": min(closing_prices),
        "max": max(closing_prices),
        "avg": statistics.mean(closing_prices),
        "median": statistics.median(closing_prices)
    }
    return stats

"""Save or update ticker statistics into a JSON file."""
def save_to_json(ticker, stats, filename="stocks.json"):
    try:
        # Load existing JSON file if it exists
        with open(filename, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []  # Start fresh if file not found or corrupted

    # Check if ticker already exists; update if it does
    updated = False
    for entry in data:
        if entry.get("ticker") == ticker:
            entry.update(stats)
            updated = True
            break

    # If ticker not found, append a new entry
    if not updated:
        new_entry = stats.copy()
        new_entry["ticker"] = ticker
        data.append(new_entry)

    # Write updated data back to the JSON file
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error writing to {filename}: {e}")

if __name__ == "__main__":
    # Entry point: handle command-line ticker symbols
    for ticker in sys.argv[1:]:
        ticker = ticker.upper().strip()  # Ensure ticker is uppercase and clean
        print(f"Processing {ticker}...")

        data = download_data(ticker)
        if data:
            stats = process_data(data)
            if stats:
                print(f"Stats for {ticker}: {stats}")
                save_to_json(ticker, stats)
            else:
                print(f"Failed to process stats for {ticker}")