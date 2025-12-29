import pymysql
import random
from datetime import datetime, timedelta

# ===================== 1. 全局配置 =====================
MYSQL_CONFIG = {
    "host": "192.168.222.128",
    "user": "root",
    "password": "ivre0333",
    "db": "music_analysis",
    "charset": "utf8mb4"
}

# 配置项：生成多少用户、多少条播放记录
CONFIG = {
    "user_count": 50,  # 生成50个用户
    "play_record_per_user": 15,  # 每个用户15条播放记录
    "start_date": datetime(2025, 12, 1),
    "end_date": datetime(2025, 12, 25)
}


# ===================== 2. 获取基础数据（歌曲、歌手） =====================
def get_base_data():
    """获取已有的真实歌曲、歌手数据"""
    conn = pymysql.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    # 获取所有歌曲ID
    cursor.execute("SELECT song_id FROM music_song;")
    song_ids = [row[0] for row in cursor.fetchall()]

    # 获取所有歌手ID（备用）
    cursor.execute("SELECT singer_id FROM singer_info;")
    singer_ids = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()
    return song_ids, singer_ids


# ===================== 3. 生成并填充user_play_record（用户播放记录） =====================
def fill_user_play_record(song_ids):
    """复用已有的user_id，只生成播放记录"""
    conn = pymysql.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    # 清空旧的播放记录（保留用户数据）
    cursor.execute("TRUNCATE TABLE user_play_record;")
    print("🗑️ 已清空user_play_record表（保留用户表数据）")

    # 第一步：从你已有的用户表（比如user_info）读取真实user_id，替代随机生成
    cursor.execute("SELECT user_id FROM user_info;")  # 假设你的用户表是user_info
    user_ids = [row[0] for row in cursor.fetchall()]
    if not user_ids:
        # 兜底：如果没用户数据，再按CONFIG生成
        user_ids = [f"U{str(i).zfill(3)}" for i in range(1, CONFIG["user_count"] + 1)]
    print(f"✅ 读取到{len(user_ids)}个已有用户ID")

    # 第二步：基于已有user_id + 真实song_id生成播放记录（逻辑不变）
    play_records = []
    for user_id in user_ids:
        for _ in range(CONFIG["play_record_per_user"]):
            song_id = random.choice(song_ids)
            play_time = CONFIG["start_date"] + timedelta(
                days=random.randint(0, (CONFIG["end_date"] - CONFIG["start_date"]).days),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            play_dur = random.randint(30, 300)
            source = random.choice(["app", "web", "pc_client", "mini_program"])

            play_records.append((user_id, song_id, play_time, play_dur, source))

    # 批量写入
    sql = """
        INSERT INTO user_play_record (user_id, song_id, play_time, play_dur, source)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.executemany(sql, play_records)
    conn.commit()
    print(f"✅ 为{len(user_ids)}个已有用户生成{len(play_records)}条播放记录")

    cursor.close()
    conn.close()
    return user_ids


# ===================== 4. 计算并填充play_stat_song（歌曲播放统计） =====================
def fill_play_stat_song():
    """基于user_play_record，计算歌曲的总播放时长、播放次数"""
    conn = pymysql.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    # 清空旧表
    cursor.execute("TRUNCATE TABLE play_stat_song;")
    print("🗑️ 已清空play_stat_song表")

    # 计算统计数据（按song_id分组）
    sql = """
        INSERT INTO play_stat_song (user_id, song_id, total_play_dur, play_count, update_time)
        SELECT 
            user_id,
            song_id,
            SUM(play_dur) AS total_play_dur,
            COUNT(*) AS play_count,
            NOW() AS update_time
        FROM user_play_record
        GROUP BY user_id, song_id;
    """
    cursor.execute(sql)
    conn.commit()

    # 统计写入数量
    cursor.execute("SELECT COUNT(*) FROM play_stat_song;")
    count = cursor.fetchone()[0]
    print(f"✅ 写入{count}条歌曲播放统计数据")

    cursor.close()
    conn.close()


# ===================== 5. 计算并填充play_stat_style（曲风播放统计） =====================
def fill_play_stat_style():
    """基于user_play_record+music_song，计算曲风的总播放时长、播放次数"""
    conn = pymysql.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    # 清空旧表
    cursor.execute("TRUNCATE TABLE play_stat_style;")
    print("🗑️ 已清空play_stat_style表")

    # 计算统计数据（关联music_song获取曲风）
    sql = """
        INSERT INTO play_stat_style (user_id, song_style, total_play_dur, play_count, update_time)
        SELECT 
            upr.user_id,
            ms.song_style,
            SUM(upr.play_dur) AS total_play_dur,
            COUNT(*) AS play_count,
            NOW() AS update_time
        FROM user_play_record upr
        LEFT JOIN music_song ms ON upr.song_id = ms.song_id
        GROUP BY upr.user_id, ms.song_style;
    """
    cursor.execute(sql)
    conn.commit()

    # 统计写入数量
    cursor.execute("SELECT COUNT(*) FROM play_stat_style;")
    count = cursor.fetchone()[0]
    print(f"✅ 写入{count}条曲风播放统计数据")

    cursor.close()
    conn.close()


# ===================== 6. 生成并填充daily_hot_song（每日热歌榜单） =====================
def fill_daily_hot_song():
    """生成每日热歌榜单（适配你的play_time字段）"""
    conn = pymysql.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    # 清空旧表
    cursor.execute("TRUNCATE TABLE daily_hot_song;")
    print("🗑️ 已清空daily_hot_song表")

    # 修复后的SQL（避免大小写/别名问题）
    sql = """
        INSERT INTO daily_hot_song (date, song_id, rank_num, hot_score)
        SELECT 
            t.play_date AS date,
            t.song_id,
            ROW_NUMBER() OVER (PARTITION BY t.play_date ORDER BY t.play_count DESC) AS rank_num,
            t.play_count * 10 AS hot_score
        FROM (
            -- 子查询明确计算日期+播放次数
            SELECT 
                song_id,
                DATE(play_time) AS play_date,
                COUNT(*) AS play_count
            FROM user_play_record
            WHERE play_time IS NOT NULL  -- 过滤空值
            GROUP BY song_id, DATE(play_time)
        ) AS t
        ORDER BY t.play_date, rank_num;
    """

    try:
        cursor.execute(sql)
        conn.commit()
        # 统计写入数量
        cursor.execute("SELECT COUNT(*) FROM daily_hot_song;")
        count = cursor.fetchone()[0]
        print(f"✅ 写入{count}条每日热歌数据")
    except Exception as e:
        print(f"❌ 写入每日热歌失败：{str(e)[:50]}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


# ===================== 7. 主函数（一键填充所有表） =====================
if __name__ == "__main__":
    # 步骤1：获取已有的真实歌曲ID
    song_ids, _ = get_base_data()
    if not song_ids:
        print("❌ 未找到music_song表中的歌曲数据，请先运行之前的爬取代码！")
        exit(1)

    # 步骤2：填充用户播放记录
    user_ids = fill_user_play_record(song_ids)

    # 步骤3：填充歌曲播放统计
    fill_play_stat_song()

    # 步骤4：填充曲风播放统计
    fill_play_stat_style()

    # 步骤5：填充每日热歌榜单
    fill_daily_hot_song()

    print("\n🎉 所有业务表数据填充完成！")