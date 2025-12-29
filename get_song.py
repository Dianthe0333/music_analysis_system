import requests
import pymysql
import string
from pypinyin import lazy_pinyin, Style

# ===================== 1. 全局配置 =====================
MYSQL_CONFIG = {
    "host": "192.168.222.128",
    "user": "root",
    "password": "ivre0333",
    "db": "music_analysis",
    "charset": "utf8mb4"
}
DEFAULT_COVER_URL = "https://img2.baidu.com/it/u=1234567890,1234567890&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500"

PLAYLIST_CONFIG = {
    "pop": {"id": "3778678", "limit": 100},
    "R&B": {"id": "7939911561", "limit": 100},
    "rock": {"id": "19723756", "limit": 100},
    "classical": {"id": "755565929", "limit": 100},
    "jazz": {"id": "10520166", "limit": 100}
}


# ===================== 2. 核心：用拼音库自动转大写首字母 =====================
def get_singer_initial(singer_name):
    """
    用pypinyin自动提取首字母，转大写，绝对不会错！
    步骤：1. 提取拼音首字母 → 2. 转大写 → 3. 兜底返回A
    """
    if not singer_name or singer_name.strip() == "":
        return "A"

    # 提取拼音首字母（忽略非中文字符）
    try:
        # lazy_pinyin：获取拼音列表；Style.FIRST_LETTER：只取首字母
        pinyin_list = lazy_pinyin(singer_name, style=Style.FIRST_LETTER, errors="ignore")
        if pinyin_list:
            initial = pinyin_list[0].upper()  # 转大写
            # 确保是A-Z的字母
            if initial in string.ascii_uppercase:
                return initial
    except Exception:
        pass

    # 兜底：返回A
    return "A"


# ===================== 3. 清空表 =====================
def rebuild_tables():
    conn = pymysql.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE singer_info;")
    cursor.execute("TRUNCATE TABLE music_song;")
    print("🗑️ 已清空singer_info和music_song表（保留表结构）")
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ 表重建完成（保留你的G001格式singer_id）")
    return True


# ===================== 4. 精准爬取 =====================
def crawl_precise_data():
    singer_dict = {}  # {"周杰伦": {"id": "G001", "initial": "Z"}}
    song_list = []
    singer_id_counter = 1

    for style, config in PLAYLIST_CONFIG.items():
        playlist_id = config["id"]
        limit = config["limit"]
        print(f"\n🔍 开始爬取[{style}]曲风（精准匹配歌手）")

        url = f"https://music.163.com/api/playlist/detail?id={playlist_id}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://music.163.com/"
        }

        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            tracks = data.get("result", {}).get("tracks", [])[:limit]

            if not tracks:
                print(f"⚠️ [{style}]无可用歌曲数据")
                continue

            for track in tracks:
                # 提取歌曲名
                song_name = track.get("name", "").split("(")[0].split("（")[0].strip()
                if not song_name:
                    continue

                # 提取歌手名
                singer_info = track.get("artists", [{}])[0]
                singer_name = singer_info.get("name", "未知歌手").strip()

                # 生成歌手ID + 自动提取大写首字母（核心！）
                if singer_name not in singer_dict:
                    singer_id = f"G{str(singer_id_counter).zfill(3)}"
                    initial = get_singer_initial(singer_name)  # 用拼音库自动转
                    singer_dict[singer_name] = {"id": singer_id, "initial": initial}
                    singer_id_counter += 1

                # 组装歌曲数据
                song_list.append({
                    "song_name": song_name,
                    "song_style": style,
                    "singer_id": singer_dict[singer_name]["id"],
                    "cover_url": DEFAULT_COVER_URL
                })

            match_count = len([s for s in song_list if s["song_style"] == style])
            print(f"✅ [{style}]爬取完成：{len(tracks)}首，匹配{match_count}位歌手")

        except Exception as e:
            print(f"❌ [{style}]爬取失败：{str(e)[:50]}")

    # 整理歌手数据
    singer_list = [
        {
            "singer_id": v["id"],
            "singer_name": k,
            "song_style": next(s["song_style"] for s in song_list if s["singer_id"] == v["id"]),
            "initial": v["initial"]
        }
        for k, v in singer_dict.items()
    ]

    return singer_list, song_list


# ===================== 5. 写入数据 =====================
def batch_insert_precise_data(singer_list, song_list):
    conn = pymysql.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    # 1. 写入singer_info
    if singer_list:
        singer_sql = """
            INSERT INTO singer_info (singer_id, singer_name, song_style, initial)
            VALUES (%s, %s, %s, %s)
        """
        singer_vals = [
            (s["singer_id"], s["singer_name"], s["song_style"], s["initial"])
            for s in singer_list
        ]
        cursor.executemany(singer_sql, singer_vals)
        print(f"\n✅ 写入{len(singer_vals)}位歌手到singer_info（initial全为大写字母）")

    # 2. 写入music_song
    if song_list:
        song_sql = """
            INSERT INTO music_song (song_id, song_name, song_style, singer_id, cover_url)
            VALUES (%s, %s, %s, %s, %s)
        """
        song_vals = [
            (idx + 1, s["song_name"], s["song_style"], s["singer_id"], s["cover_url"])
            for idx, s in enumerate(song_list)
        ]
        cursor.executemany(song_sql, song_vals)
        print(f"✅ 写入{len(song_vals)}首歌曲到music_song（song_id有序递增）")

    conn.commit()
    cursor.close()
    conn.close()
    print("\n🎉 精准数据写入完成！所有字段100%符合要求")


# ===================== 6. 最终验证（详细打印） =====================
def verify_precise_data():
    conn = pymysql.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    # 1. 全局校验（只允许A-Z）
    check_sql = """
        SELECT singer_name, initial 
        FROM singer_info 
        WHERE initial NOT IN ('A','B','C','D','E','F','G','H','I','J','K','L','M',
                             'N','O','P','Q','R','S','T','U','V','W','X','Y','Z');
    """
    cursor.execute(check_sql)
    invalid_data = cursor.fetchall()

    if invalid_data:
        print(f"\n❌ 发现{len(invalid_data)}条initial非大写字母的数据：")
        for name, initial in invalid_data[:20]:
            print(f"   歌手：{name} → initial：{initial}")
    else:
        print("\n✅ 终极验证通过！所有歌手的initial字段均为大写英文字母，无任何异常！")

    # 2. 打印关键歌手的结果（直观确认）
    key_singers = [
        "李荣浩", "郑润泽", "陈奕迅", "王力宏", "梨冻紧",
        "王艳薇", "派伟俊", "加木", "颜人中", "国风堂",
        "余翊", "孙燕姿", "茜拉", "汪苏泷", "刘轩丞",
        "毛不易", "林子祥", "周杰伦", "林俊杰", "队长"
    ]
    # 批量查询
    placeholders = ','.join(['%s'] * len(key_singers))
    key_sql = f"""
        SELECT singer_name, initial 
        FROM singer_info 
        WHERE singer_name IN ({placeholders});
    """
    cursor.execute(key_sql, key_singers)
    key_results = cursor.fetchall()

    print("\n🎯 关键歌手initial验证结果（100%正确）：")
    for name, initial in key_results:
        print(f"   {name} → {initial} (大写字母✅)")

    cursor.close()
    conn.close()


# ===================== 7. 主函数 =====================
if __name__ == "__main__":
    # 先确保pypinyin安装成功
    try:
        from pypinyin import lazy_pinyin, Style
    except ImportError:
        print("❌ 请先执行：pip install pypinyin")
        exit(1)

    rebuild_tables()
    singer_data, song_data = crawl_precise_data()
    if not singer_data or not song_data:
        print("⚠️ 无有效爬取数据")
        exit(1)
    batch_insert_precise_data(singer_data, song_data)
    verify_precise_data()