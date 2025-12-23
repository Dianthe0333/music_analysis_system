import pandas as pd
import os
import random
from datetime import datetime, timedelta
import paramiko
import pymysql

# ==================== MySQL配置 ====================
MYSQL_HOST = "192.168.222.128"
MYSQL_USER = "root"
MYSQL_PWD = "ivre0333"
MYSQL_DB = "music_analysis"
local_path = "D:/PyCharmMiscProject/music_project/data/music_log.csv"
# ==================== 生成用户数据并插入user_info表 ====================
def generate_and_insert_users(user_num=100):
    """
    生成用户数据并插入user_info表
    :param user_num: 生成的用户数量，默认100个（U001~U100）
    :return: 生成的用户ID列表（如['U001', 'U002', ...]）
    """
    # 1. 生成用户数据
    user_data = []
    for i in range(1, user_num + 1):
        user_id = f"U{str(i).zfill(3)}"  # 大写U开头，补零到3位：U001~U100
        password = user_id  # 密码和用户ID一致
        user_name = f"用户{str(i).zfill(3)}"  # 用户名：用户001~用户100
        user_data.append([user_id, user_name, password])

    # 2. 转换为DataFrame
    user_df = pd.DataFrame(user_data, columns=["user_id", "user_name", "password"])

    # 3. 插入MySQL的user_info表
    try:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PWD,
            database=MYSQL_DB,
            charset="utf8"
        )
        cursor = conn.cursor()

        # 先清空user_info表旧数据
        cursor.execute("TRUNCATE TABLE user_info")

        # 批量插入用户数据
        insert_user_sql = """
            INSERT INTO user_info (user_id, user_name, password)
            VALUES (%s, %s, %s)
        """
        user_tuples = [tuple(row) for row in user_df.values]
        cursor.executemany(insert_user_sql, user_tuples)
        conn.commit()

        print(f"✅ 成功生成并插入{cursor.rowcount}个用户到user_info表！（U001~U{str(user_num).zfill(3)}）")
        cursor.close()
        conn.close()

        # 返回生成的用户ID列表
        return [f"U{str(i).zfill(3)}" for i in range(1, user_num + 1)]
    except Exception as e:
        print(f"❌ 生成/插入用户失败：{str(e)}")
        return []

# 执行用户生成（生成100个用户）
user_ids = generate_and_insert_users(user_num=100)
if not user_ids:  # 若用户生成失败，直接退出
    exit()

# ==================== 读取music_song表中实际存在的歌曲ID ====================
def get_existing_song_ids():
    """读取music_song表中所有song_id，避免生成不存在的歌曲"""
    try:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PWD,
            database=MYSQL_DB,
            charset="utf8"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT song_id FROM music_song")
        song_ids = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return song_ids
    except Exception as e:
        print(f"❌ 读取歌曲ID失败：{str(e)}")
        return []

# 获取歌曲ID列表（S001~S021）
song_ids = get_existing_song_ids()
if not song_ids:  # 若读取失败，直接退出
    exit()

# ==================== 生成播放记录并插入user_play_record表 ====================
def generate_and_insert_play_records(log_num=1000, user_ids=None, song_ids=None):
    """
    生成播放记录并插入user_play_record表
    :param log_num: 生成的播放记录数量，默认1000条
    :param user_ids: 可选的用户ID列表（从这些用户中随机选）
    :param song_ids: 可选的歌曲ID列表（从这些歌曲中随机选）
    """
    if not user_ids or not song_ids:
        print("❌ 用户ID/歌曲ID列表为空，无法生成播放记录！")
        return

    # 1. 定义基础数据
    sources = ["app", "web", "mini_program", "pc_client"]  # 播放来源
    start_date = datetime(2025, 12, 1)  # 日志起始日期

    # 2. 生成播放记录数据
    log_data = []
    for _ in range(log_num):
        user_id = random.choice(user_ids)  # 从生成的用户中随机选
        song_id = random.choice(song_ids)  # 从表中存在的歌曲中随机选
        play_dur = random.randint(30, 300)  # 播放时长：30~300秒
        # 随机播放时间（近15天，带时分秒）
        play_date = start_date + timedelta(
            days=random.randint(0, 15),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        play_time = play_date.strftime("%Y-%m-%d %H:%M:%S")  # 时间戳格式
        source = random.choice(sources)  # 随机播放来源
        # 数据顺序匹配user_play_record表字段：user_id, song_id, play_time, play_dur, source
        log_data.append([user_id, song_id, play_time, play_dur, source])

    # 3. 转换为DataFrame
    log_df = pd.DataFrame(
        log_data,
        columns=["user_id", "song_id", "play_time", "play_dur", "source"]
    )

    # 4. 保存到本地CSV
    local_path = "D:/PyCharmMiscProject/music_project/data/music_log.csv"
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    log_df.to_csv(local_path, index=False, encoding="utf-8")
    print(f"✅ 播放记录本地保存成功！文件路径：{local_path}")

    # 5. 插入MySQL的user_play_record表
    try:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PWD,
            database=MYSQL_DB,
            charset="utf8"
        )
        cursor = conn.cursor()

        # 先清空播放记录表旧数据
        cursor.execute("TRUNCATE TABLE user_play_record")

        # 批量插入播放记录
        insert_log_sql = """
            INSERT INTO user_play_record (user_id, song_id, play_time, play_dur, source)
            VALUES (%s, %s, %s, %s, %s)
        """
        log_tuples = [tuple(row) for row in log_df.values]
        cursor.executemany(insert_log_sql, log_tuples)
        conn.commit()

        print(f"✅ 成功插入{cursor.rowcount}条播放记录到user_play_record表！")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ 插入播放记录失败：{str(e)}")

# 执行播放记录生成（生成1000条）
generate_and_insert_play_records(log_num=1000, user_ids=user_ids, song_ids=song_ids)

# ==================== 自动上传CSV到Ubuntu ====================
UBUNTU_IP = "192.168.222.128"
UBUNTU_USER = "tang0333"
UBUNTU_PWD = "123456"
REMOTE_PATH = "/home/tang0333/music_project/data/music_log.csv"
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(UBUNTU_IP, username=UBUNTU_USER, password=UBUNTU_PWD)
    ssh.exec_command(f"mkdir -p /home/tang0333/music_project/data")
    sftp = ssh.open_sftp()
    sftp.put(local_path, REMOTE_PATH)
    sftp.close()
    ssh.close()
    print(f"✅ 上传到Ubuntu成功！远程路径：{REMOTE_PATH}")
except Exception as e:
    print(f"❌ 上传失败：{str(e)}")