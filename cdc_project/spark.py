from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType


# start spark session 
spark = SparkSession.builder \
    .appName("KafkaDebezium") \
    .getOrCreate()

# define JSON schema 
# define JSON schema 
schema = StructType([
    StructField("schema", StructType([
        StructField("type", StringType(), True),
        StructField("fields", StructType([
            StructField("type", StringType(), True),
            StructField("optional", StringType(), True),
            StructField("default", StringType(), True),
            StructField("field", StringType(), True)
        ]), True),
        StructField("optional", StringType(), True),
        StructField("name", StringType(), True),
        StructField("version", StringType(), True)
    ]), True),

    StructField("payload", StructType([
        StructField("before", StructType([
            StructField("userid", StringType(), True),
            StructField("sessionid", StringType(), True),
            StructField("timestamp", StringType(), True),
            StructField("page_url", StringType(), True),
            StructField("action", StringType(), True),
            StructField("referrer_url", StringType(), True),
            StructField("device", StringType(), True),
            StructField("browser", StringType(), True)
        ]), True),
        StructField("after", StructType([
            StructField("userid", StringType(), True),
            StructField("sessionid", StringType(), True),
            StructField("timestamp", StringType(), True),
            StructField("page_url", StringType(), True),
            StructField("action", StringType(), True),
            StructField("referrer_url", StringType(), True),
            StructField("device", StringType(), True),
            StructField("browser", StringType(), True)
        ]), True),
        StructField("source", StructType([
            StructField("version", StringType(), True),
            StructField("connector", StringType(), True),
            StructField("name", StringType(), True),
            StructField("ts_ms", LongType(), True),
            StructField("snapshot", StringType(), True),
            StructField("db", StringType(), True),
            StructField("sequence", StringType(), True),
            StructField("schema", StringType(), True),
            StructField("table", StringType(), True),
            StructField("txid", LongType(), True),
            StructField("lsn", LongType(), True),
            StructField("xmin", LongType(), True)
        ]), True),
        StructField("op", StringType(), True),
        StructField("ts_ms", LongType(), True),
        StructField("transaction", StructType([
            StructField("id", StringType(), True),
            StructField("total_order", LongType(), True),
            StructField("data_collection_order", LongType(), True)
        ]), True)
    ]), True)
])

# read data from Kafka
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "34.170.38.47:9092") \
    .option("subscribe", "dbserver1.public.user_activity") \
    .load()

# converting messages to strings
kafka_df = kafka_df.selectExpr("CAST(value AS STRING)")

# # Converting JSON data to a DataFrame
json_df = kafka_df.select(from_json(col("value"), schema).alias("data"))

# filter only creates
json_df = json_df.filter(col("data.payload.op") == "c")

# converting data to a DataFrame
json_df = json_df.select(
    col("data.payload.after.userid").alias("userid"),
    col("data.payload.after.sessionid").alias("sessionid"),
    col("data.payload.after.timestamp").alias("timestamp"),
    col("data.payload.after.page_url").alias("page_url"),
    col("data.payload.after.action").alias("action"),
    col("data.payload.after.referrer_url").alias("referrer_url"),
    col("data.payload.after.device").alias("device"),
    col("data.payload.after.browser").alias("browser")
)

# holding the data on ram
json_df.writeStream \
    .outputMode("append") \
    .format("memory") \
    .queryName("user_activity") \
    .start()
    
# SQL query
spark.sql("SELECT * FROM user_activity").show()