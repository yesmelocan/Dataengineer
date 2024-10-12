from kafka import KafkaProducer
import json
from dotenv import load_dotenv
import os
import finnhub
import time

# Load .env file

load_dotenv(override=True) # this override=True is so important when you change your ip it's simple avoid waste of time 
                            #Reloads the environment variables, overriding previous ones
# Retrieve environment variables
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
KAFKA_BROKER_IP = os.getenv("KAFKA_BROKER")  # Your .env file should contain broker information
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")    # The Kafka topic to send data to
# Finnhub API client
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
print (KAFKA_BROKER_IP)
# Kafka producer settings
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_IP,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  #  encode json data 
)

# Fetch symbols from Finnhub API
symbols = finnhub_client.stock_symbols('US')

# Loop through each symbol and fetch data

for symbol_data in symbols:
    symbol = symbol_data['symbol']
    try:
        # Fetch stock data
        stock_data = finnhub_client.quote(symbol)
        
        # Prepare data in JSON format for Kafka
        message = {
            'symbol': symbol,
            'current_price': stock_data['c'],
            'open_price': stock_data['o'],
            'high_price': stock_data['h'],
            'low_price': stock_data['l'],
            'previous_close': stock_data['pc']
        }
        
        # Send data to Kafka topic
        producer.send(KAFKA_TOPIC, value=message)
        print(f"Sent data for symbol {symbol}: {message}")
        
        # ensure messages are sent
        #  producer.flush()
        
        # Wait to avoid API rate limit (optional)
        time.sleep(1)
        
    except Exception as e:
        print(f"Error fetching data for symbol {symbol}: {e}")



