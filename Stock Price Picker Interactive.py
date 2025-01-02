import requests
import pandas as pd
import matplotlib.pyplot as plt

def fetch_stock_data(symbol, S0G55PFNAHOY5XTQ):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=S0G55PFNAHOY5XTQ"
    response = requests.get(url)
    data = response.json()
    if "Time Series (Daily)" not in data:
        raise ValueError("Error fetching data. Please check your API key or symbol.")
    return data["Time Series (Daily)"]

def process_data(daily_data):
    df = pd.DataFrame.from_dict(daily_data, orient="index", dtype=float)
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    return df

def calculate_moving_averages(df):
    df["10-day MA"] = df["Close"].rolling(window=10).mean()
    df["20-day MA"] = df["Close"].rolling(window=20).mean()
    return df

def visualize_data(df, symbol):
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["Close"], label="Close Price", linewidth=2)
    plt.plot(df.index, df["10-day MA"], label="10-day Moving Average", linestyle="--")
    plt.plot(df.index, df["20-day MA"], label="20-day Moving Average", linestyle="--")

    plt.title(f"Stock Prices and Moving Averages for {symbol}")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid()
    plt.show()

def main():
    API_KEY = input("Enter your Alpha Vantage API Key: ").strip()
    symbol = input("Enter the stock symbol (e.g., AAPL): ").strip().upper()

    try:
        print("Fetching stock data...")
        daily_data = fetch_stock_data(symbol, API_KEY)
        print("Processing data...")
        df = process_data(daily_data)
        df = calculate_moving_averages(df)
        print("Visualizing data...")
        visualize_data(df, symbol)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
