from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, when

# 初始化SparkSession
spark = SparkSession.builder \
    .appName("MusicCleaning") \
    .master("local[*]") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://192.168.***.128:9000") \
    .getOrCreate()

# 读取数据
df = spark.read.csv(
    "hdfs://192.168.***.128:9000/music_data/raw_data.csv",
    header=True,
    inferSchema=True
)

# 数据清洗
df = df.withColumn("listen_time", to_timestamp(col("listen_time"), "yyyy-MM-dd HH:mm:ss"))
df = df.withColumn("listen_dur", when(col("listen_dur").isNull(), 0).otherwise(col("listen_dur")))
df = df.filter(col("listen_dur") >= 0)

# 保存结果
df.write.mode("overwrite").csv(
    "hdfs://192.168.***.128:9000/music_data/cleaned_data.csv",
    header=True
)


spark.stop()
