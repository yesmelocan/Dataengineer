
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
         .config("spark.jars", "gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar") 
         # this package provide streaming between cloud and spark
         .getOrCreate())

# You can use the code below to check if the Kafka and BigQuery configurations have been loaded.
spark.sparkContext.getConf().getAll()

bucket = "kafka-gcp" #temporary station  data comes  from spark to bigquery it's the temporary station
spark.conf.set("temporaryGcsBucket", bucket) # Dataproc and my cluster should be in same zone
spark.conf.set("parentProject", "PROJECT_ID")#us central-1 / dont forget to change project name 

schema = StructType([
    StructField("symbol", StringType(), True),
    StructField("current_price", StringType(), True),
    StructField("open_price", StringType(), True),
    StructField("high_price", StringType(), True),
    StructField("low_price", StringType(), True),
    StructField("previous_close", StringType(), True),
])


kafkaDF = spark.readStream.format("kafka").option(
    "kafka.bootstrap.servers", "KAFKA_BROKER:9092").option(
    "subscribe", "Test").load()
#KAFKA_BROKER is my kafka vm ip

kafkaDF = kafkaDF.selectExpr("CAST(value AS STRING)")

# Converting JSON data to a DataFrame
json_df = kafkaDF.select(from_json(col("value"), schema).alias("data"))
# converting data into a table
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
    
    