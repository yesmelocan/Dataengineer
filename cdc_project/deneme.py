# JSON schema tanımı oluşturma
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
            StructField("id", IntegerType(), True),
            StructField("first_name", StringType(), True),
            StructField("last_name", StringType(), True),
            StructField("email", StringType(), True),
            StructField("phone", StringType(), True),
            StructField("created_at", LongType(), True)
        ]), True),
        StructField("after", StructType([
            StructField("id", IntegerType(), True),
            StructField("first_name", StringType(), True),
            StructField("last_name", StringType(), True),
            StructField("email", StringType(), True),
            StructField("phone", StringType(), True),
            StructField("created_at", LongType(), True)
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
            StructField("txId", LongType(), True),
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