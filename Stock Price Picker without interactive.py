import requests
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Fetch Stock Data from Alpha Vantage API
API_KEY = "S0G55PFNAHOY5XTQ"  # Replace with your API key
symbol = "AAPL"
url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=S0G55PFNAHOY5XTQ"

response = requests.get(url)
data = response.json()

# Check if the API returned data
if "Time Series (Daily)" not in data:
    print("Error fetching data. Please check your API key or symbol.")
    exit()

# Step 2: Process Data with Pandas
daily_data = data["Time Series (Daily)"]
df = pd.DataFrame.from_dict(daily_data, orient="index", dtype=float)
df = df.rename(columns={
    "1. open": "Open",
    "2. high": "High",
    "3. low": "Low",
    "4. close": "Close",
    "5. volume": "Volume"
})

# Convert index to datetime
df.index = pd.to_datetime(df.index)
df = df.sort_index()

# Step 3: Calculate Moving Averages
df["10-day MA"] = df["Close"].rolling(window=10).mean()
df["20-day MA"] = df["Close"].rolling(window=20).mean()

# Step 4: Visualize the Data
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
