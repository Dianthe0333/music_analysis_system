from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, sum, count, floor, desc, countDistinct
)

# 初始化 SparkSession（每行末尾加 \ 续行）
spark = SparkSession.builder \
    .appName("MusicBehaviorAnalysis") \
    .master("local[*]") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://192.168.222.128:9000") \
    .config("spark.sql.repl.eagerEval.enabled", True) \
    .getOrCreate()

# 一：读取 HDFS 上的行为数据
clean_df = spark.read.csv(
    path="hdfs://192.168.222.128:9000/music_log/clean",
    header=True,
    inferSchema=True,
    encoding="utf-8"
)

# 验证数据读取结果
print("=== 1. 原始数据预览 ===")
clean_df.show(10)
print("=== 数据字段名 ===")
print(clean_df.columns)
print("=== 数据字段类型 ===")
clean_df.printSchema()

# 二：数据清洗
clean_valid_df = clean_df.filter(
    (col("listen_dur") > 0) &
    (col("behavior_type").isNotNull()) &
    (col("song_style").isNotNull())
)
print("\n=== 2. 清洗后数据预览 ===")
clean_valid_df.show(10)

# 三：核心分析逻辑
## 3.1 按歌曲风格统计
style_analysis = clean_valid_df.groupBy("song_style") \
    .agg(
        sum("listen_dur").alias("total_listen_seconds"),
        count("song_id").alias("total_play_count"),
        countDistinct("song_id").alias("unique_song_count"),
        (sum("listen_dur") / 3600).alias("total_listen_hours")
    ) \
    .orderBy(desc("total_listen_seconds"))

print("\n=== 3. 按歌曲风格统计分析 ===")
style_analysis.show(truncate=False)

## 3.2 播放时长小时段分析
hour_segment_df = clean_valid_df.withColumn(
    "listen_hour_segment",
    floor(col("listen_dur") / 3600)
)

hour_analysis = hour_segment_df.groupBy("listen_hour_segment") \
    .agg(
        count("user_id").alias("play_count"),
        sum("listen_dur").alias("total_seconds")
    ) \
    .orderBy("listen_hour_segment")

print("\n=== 4. 按播放时长小时段统计 ===")
hour_analysis.show()

## 3.3 按行为类型统计
behavior_analysis = clean_valid_df.groupBy("behavior_type") \
    .agg(
        count("user_id").alias("behavior_count"),
        sum("listen_dur").alias("total_listen_seconds")
    )

print("\n=== 5. 按用户行为类型统计 ===")
behavior_analysis.show()

## 3.4 热门歌曲TOP3
hot_song_analysis = clean_valid_df.groupBy("song_id") \
    .agg(
        count("user_id").alias("play_count"),
        sum("listen_dur").alias("total_listen_seconds")
    ) \
    .orderBy(desc("play_count")) \
    .limit(3)

print("\n=== 6. 热门歌曲TOP3 ===")
hot_song_analysis.show()

# 四：分析结果写入HDFS
style_analysis.write \
    .mode("overwrite") \
    .csv("hdfs://192.168.222.128:9000/music_log/analysis/style_analysis", header=True)

# 五：停止SparkSession
spark.stop()