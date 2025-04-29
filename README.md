# Stock Data Analysis
This project fetches 5 years of historical stock data from Nasdaq, computes key statistics (min, max, average, median), and saves the results into a JSON file.

## How It Works
- Fetches stock data using requests
- Processes closing prices
- Handles API and file errors
- Saves results into stocks.json

## Usage
```
python stocks.py AAPL MSFT GOOGL
``` 
## Example Output
```
[
  {
    "ticker": "AAPL",
    "min": 56.09,
    "max": 259.02,
    "avg": 156.66,
    "median": 154.51
  }
]
```
## GitHub repo includes 3 tagged commits:
```
data-acquisition
data-processing
data-output