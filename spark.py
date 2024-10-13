
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType, IntegerType, FloatType

# pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar
#if .pynb doesnt work we use terminal we start with upper code 
# spark = SparkSession.builder.appName("Streaming").getOrCreate() 
#in terminal we used upper code (it doesnt work in my project i couldnt use kernels)
spark = (SparkSession.builder
         .appName("MyApp") # declared my app name
         .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2") # include kafka to our system
         .config("spark.jars", "gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar") # this package provide streaming between cloud and spark
         .getOrCreate())

# kafka ve bigquery konfigurasyonları yüklenip yüklenmediğini kontrol etmek için aşağıdaki kodu kullanabilirsiniz.
spark.sparkContext.getConf().getAll()

bucket = "kafka-gcp" #temporary station  data comes  from spark to bigquery it's the temporary station
spark.conf.set("temporaryGcsBucket", bucket) # Dataproc and my cluster should be in same zone
spark.conf.set("parentProject", "angelic-gift-431019-i2")#us central-1 / dont forget to change project name 

schema = StructType([
    StructField("symbol", StringType(), True),
    StructField("current_price", StringType(), True),
    StructField("open_price", StringType(), True),
    StructField("high_price", StringType(), True),
    StructField("low_price", StringType(), True),
    StructField("previous_close", StringType(), True),
])


kafkaDF = spark.readStream.format("kafka").option(
    "kafka.bootstrap.servers", "35.225.77.55:9092").option(
    "subscribe", "Test").load()

#   
kafkaDF = kafkaDF.selectExpr("CAST(value AS STRING)")

# JSON verilerini DataFrame'e dönüştürme
json_df = kafkaDF.select(from_json(col("value"), schema).alias("data"))


# Verileri tablo haline getirme
json_df = json_df.select(
    col("data.symbol"),
    col("data.current_price"),
    col("data.open_price"),
    col("data.high_price"),
    col("data.low_price"),
    col("data.previous_close"),
)


df = (json_df
      .withColumn("current_price", col("current_price").cast(FloatType()))
      .withColumn("open_price", col("open_price").cast(FloatType()))
      .withColumn("high_price", col("high_price").cast(FloatType()))
      .withColumn("low_price", col("low_price").cast(FloatType()))
      .withColumn("previous_close", col("previous_close").cast(FloatType()))
)




#de_stock.stock create tale in de_stock as name stock
#"failOnDataLoss", False  if data comes false it will continue

# model_write_console = df.writeStream.outputMode("append").format("console").start().awaitTermination()
# #we control our structure is it working right or not we do that in the terminal not pyconsole



save_data = df.writeStream\
    .outputMode("append").format("bigquery")\
    .option("table", "de_stock.stock")\
    .option("checkpointLocation", "/path/to/checkpoint/dir/in/hdfs")\
    .option("failOnDataLoss", False)\
    .option("truncate", False)\
    .start().awaitTermination()