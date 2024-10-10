import os
import finnhub
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

print(finnhub_client.quote("AAPL"))




"""import finnhub
import time

# Initialize the Finnhub client with your API key
finnhub_client = finnhub.Client(api_key="your_api_key_here")

# Fetch stock symbols for the US exchange (or other exchanges if needed)
symbols = finnhub_client.stock_symbols('US')  # 'US' for US stocks


# Loop through each symbol and fetch the stock data
for symbol_data in symbols:
    symbol = symbol_data['symbol']
    try:
        # Fetch the stock data (real-time quote)
        stock_data = finnhub_client.quote(symbol)
        
        # Print the symbol and its data (open, close, high, low prices, etc.)
        print(f"Symbol: {symbol}")
        print(f"Current Price: {stock_data['c']}")
        print(f"Open Price: {stock_data['o']}")
        print(f"High Price: {stock_data['h']}")
        print(f"Low Price: {stock_data['l']}")
        print(f"Previous Close: {stock_data['pc']}")
        print("-" * 50)
        
        # Sleep to avoid hitting the API rate limit (optional)
        time.sleep(1)  # Adjust sleep time if needed
        
    except Exception as e:
        print(f"Error fetching data for symbol {symbol}: {e}")
"""