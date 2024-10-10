from kafka import KafkaProducer
import json
from dotenv import load_dotenv
import os
import finnhub
import time

# .env dosyasını yükleyin
load_dotenv()

# Environment değişkenini alın
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
KAFKA_BROKER_IP = os.getenv("KAFKA_BROKER")  # .env dosyanızda broker bilgisi olmalı
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")    # Gönderilecek Kafka topic'i

# Finnhub API client
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

# Kafka producer ayarları
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_IP,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # JSON veriyi encode et
)

# Finnhub API'den sembolleri al
symbols = finnhub_client.stock_symbols('US')

# Her bir sembol için döngüye gir ve veriyi çek
for symbol_data in symbols:
    symbol = symbol_data['symbol']
    try:
        # Hisse verilerini al
        stock_data = finnhub_client.quote(symbol)
        
        # Veriyi JSON formatında Kafka'ya gönderilecek şekilde hazırlayın
        message = {
            'symbol': symbol,
            'current_price': stock_data['c'],
            'open_price': stock_data['o'],
            'high_price': stock_data['h'],
            'low_price': stock_data['l'],
            'previous_close': stock_data['pc']
        }
        
        # Kafka topic'e veriyi gönder
        producer.send(KAFKA_TOPIC, value=message)
        print(f"Sent data for symbol {symbol}: {message}")
        
        # Mesajların gönderildiğinden emin olmak için flush yap
      #  producer.flush()
        
        # API rate limit'e takılmamak için bekleyin (opsiyonel)
        time.sleep(1)
        
    except Exception as e:
        print(f"Error fetching data for symbol {symbol}: {e}")

# Tüm mesajların gönderildiğinden emin olun
producer.flush()


