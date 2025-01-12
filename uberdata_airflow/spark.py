from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StringType, IntegerType, FloatType, StructType, StructField, DateType, TimestampType

spark = SparkSession.builder.appName("uber_data_transform").getOrCreate()

schema = StructType([
    StructField("VendorID", IntegerType(), True),
    StructField("tpep_pickup_datetime", TimestampType(), True),
    StructField("tpep_dropoff_datetime", TimestampType(), True),
    StructField("passenger_count", IntegerType(), True),
    StructField("trip_distance", FloatType(), True),
    StructField("pickup_longitude", FloatType(), True),
    StructField("pickup_latitude", FloatType(), True),
    StructField("RatecodeID", IntegerType(), True),
    StructField("store_and_fwd_flag", StringType(), True),
    StructField("dropoff_longitude", FloatType(), True),
    StructField("dropoff_latitude", FloatType(), True),
    StructField("payment_type", IntegerType(), True),
    StructField("fare_amount", FloatType(), True),
    StructField("extra", FloatType(), True),
    StructField("mta_tax", FloatType(), True),
    StructField("tip_amount", FloatType(), True),
    StructField("tolls_amount", FloatType(), True),
    StructField("improvement_surcharge", FloatType(), True),
    StructField("total_amount", FloatType(), True)
])


bucket = "deneme1211"
spark.conf.set("temporaryGcsBucket", bucket)
# df = spark.read.csv("gs://deneme12121/uber_data.csv",header=True, inferSchema=True)
df = spark.read.csv("gs://deneme12121/uber_data.csv",header=True, schema=schema)




from pyspark.sql import functions as F

ssenger_count kolonundaki ortalama değeri döndürür
# first()[0] -> ortalama değeri almak için kullanılır
df = df.fillna({
    "passenger_count": df.agg(F.mean(col("passenger_count"))).first()[0],
    "trip_distance": df.agg(F.mean(col("trip_distance"))).first()[0]
})

df = df.fillna({"store_and_fwd_flag": "N"})




df = df.withColumn("trip_duration", 
                   F.unix_timestamp("tpep_dropoff_datetime") - F.unix_timestamp("tpep_pickup_datetime"))






df = df.filter((col("fare_amount") > 0) & (col("trip_distance") > 0))


df.write.format("bigquery") \
    .option("temporaryGcsBucket", bucket) \
    .option("createDisposition", "CREATE_IF_NEEDED") \
    .option("writeDisposition", "WRITE_TRUNCATE") \
    .option("table", "deneme12121.uber_data_transformed") \
    .save()