import os

from dotenv import load_dotenv

from pyspark.sql.functions import from_json, col, to_timestamp, to_date
from pyspark.sql.types import StructType, StringType, IntegerType, LongType


load_dotenv()

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SaveTransactionsToHDFS").getOrCreate()

schema = (
    StructType()
    .add("id", StringType())
    .add("sender_id", IntegerType())
    .add("sender_name", StringType())
    .add("amount", IntegerType())
    .add("timestamp", LongType())
    .add("ip", StringType())
    .add("receiver_id", IntegerType())
    .add("receiver_name", StringType())
)

df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "transaction-events")
    .load()
)

parsed = (
    df.selectExpr("CAST(value AS STRING) as json_str")
    .select(from_json(col("json_str"), schema).alias("data"))
    .select("data.*")
    .withColumn("event_time", to_timestamp((col("timestamp") / 1000).cast("long")))
    .withColumn("event_date", to_date(col("event_time")))
)

# 저장
query = (
    parsed.writeStream.partitionBy("event_date")
    .format("parquet")
    .option("path", "hdfs://localhost:9000/warehouse/transactions/")
    .option("checkpointLocation", "checkpoints/save-transactions")
    .outputMode("append")
    .start()
)

query.awaitTermination()
