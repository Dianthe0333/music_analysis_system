import streamlit as st
import pymysql
import pandas as pd
from datetime import datetime, date, timedelta
import os

# ===================== 全局配置 =====================
st.set_page_config(
    page_title="音乐偏好分析系统",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS（st.image）
st.markdown("""
    <style>
    /* 全局背景 */
    .main {background-color: #bddde9 !important;}
    /* 隐藏默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* 页面容器（独立视觉） */
    .page-container {
        max-width: 1200px; margin: 0 auto; padding: 20px;
        min-height: 80vh; background: #bddde9;
    }
    /* TOP5/TOP10歌曲卡片（适配st.image） */
    .hot-song-card {
        background: white; border-radius: 15px; padding: 15px;
        margin: 10px; text-align: center; width: 180px;
    }
    .hot-song-card h3 {
        font-size: 16px; color: #2d3748; margin-top: 10px;
    }
    /* 曲风/歌手/个人中心样式 */
    .style-rank, .singer-book, .stat-card {
        max-width: 900px; margin: 0 auto; background: white;
        padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .style-item, .singer-item {
        padding: 15px; margin: 10px 0; border-radius: 8px;
        background: #f8f9fa; display: flex; justify-content: space-between;
        align-items: center;
    }
    .letter-title {
        font-size: 20px; font-weight: bold; color: #667eea;
        padding: 10px; border-bottom: 1px solid #e9ecef;
        margin-top: 20px;
    }
    /* 菜单按钮样式 */
    .sidebar-btn {
        width: 100%; padding: 12px; margin: 8px 0 !important;
        border: none; border-radius: 6px; font-size: 16px;
        background: #667eea; color: white; cursor: pointer;
    }
    .sidebar-btn:hover {background: #5a67d8;}
    /* 统计数据样式 */
    .stat-item {
        padding: 10px; margin: 5px 0; border-left: 4px solid #667eea;
        background: #f8f9fa;
    }
    </style>
""", unsafe_allow_html=True)

# ===================== 数据库配置 =====================
DB_CONFIG = {
    "host": "192.168.***.128",
    "port": 3306,
    "user": "******",
    "password": "******",
    "database": "music_analysis",
    "charset": "utf8mb4"
}


# 数据库查询函数
def get_db_data(sql):
    try:
        conn = pymysql.connect(**DB_CONFIG)
        df = pd.read_sql(sql, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"数据库错误：{str(e)}")
        return pd.DataFrame()


# ===================== 路径配置（本地封面路径） ========================
current_script_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_script_path)
song_covers_path = os.path.join(current_dir, "song_covers")

# 检查并创建封面文件夹
if not os.path.exists(song_covers_path):
    os.makedirs(song_covers_path)
    st.warning(f"已自动创建song_covers文件夹：{song_covers_path}")
else:
    st.success(f"找到song_covers文件夹：{song_covers_path} ✨")

# ===================== Session State初始化 =====================
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"  # 核心状态：当前页面
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""
if "selected_style" not in st.session_state:
    st.session_state.selected_style = ""
if "selected_singer_id" not in st.session_state:
    st.session_state.selected_singer_id = ""
if "selected_singer_name" not in st.session_state:
    st.session_state.selected_singer_name = ""


# ===================== 核心函数 =====================
def switch_page(page_name):
    st.session_state.current_page = page_name
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except AttributeError:
            st.session_state["_rerun_trigger"] = st.session_state.get("_rerun_trigger", 0) + 1


def user_login(user_id, password):
    """登录验证"""
    user_id = user_id.strip()
    password = password.strip()
    df = get_db_data(f"SELECT * FROM user_info WHERE user_id='{user_id}' AND password='{password}'")
    if not df.empty:
        st.session_state.logged_in = True
        st.session_state.current_user = user_id
        st.success(f"登录成功！欢迎 {df.iloc[0]['user_name']}")
        switch_page("home")
        return True
    else:
        st.error("账号密码错误！（U001/U002/U003，密码与账号相同）")
        return False


def user_logout():
    """退出登录"""
    st.session_state.logged_in = False
    st.session_state.current_user = ""
    st.success("已退出登录！")
    switch_page("home")


# ===================== 左侧侧边栏菜单 =====================
with st.sidebar:
    if "_rerun_trigger" in st.session_state:
        st.markdown(f"<div style='display:none'>{st.session_state['_rerun_trigger']}</div>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align:center; color:#667eea'>🎵 音乐系统</h2>", unsafe_allow_html=True)
    st.markdown("---")

    # 登录/退出按钮
    if st.session_state.logged_in:
        st.markdown(f"<p style='text-align:center; color:#2d3748'>当前登录：{st.session_state.current_user}</p>",
                    unsafe_allow_html=True)
        if st.button("退出登录", use_container_width=True, key="logout_btn"):
            user_logout()
    else:
        if st.button("用户登录", use_container_width=True, key="login_btn"):
            switch_page("login")

    st.markdown("---")
    st.markdown("<h4 style='color:#2d3748'>📌 功能菜单</h4>", unsafe_allow_html=True)

    # 核心菜单按钮
    if st.button("🏠 首页", use_container_width=True, key="home_btn"):
        switch_page("home")
    if st.button("🌍 全局曲风统计", use_container_width=True, key="global_style_btn"):
        switch_page("global_style")
    if st.button("🎶 曲风排行", use_container_width=True, key="style_btn"):
        switch_page("style")
    if st.button("🎤 歌手列表", use_container_width=True, key="singer_btn"):
        switch_page("singer")
    if st.button("👤 个人中心", use_container_width=True, key="user_btn"):
        if st.session_state.logged_in:
            switch_page("user")
        else:
            switch_page("login")
            st.warning("请先登录！")

# ===================== 页面渲染（新增/修改功能） =====================
st.markdown("<div class='page-container'>", unsafe_allow_html=True)

# ---------- 1. 首页  -----------
if st.session_state.current_page == "home":
    st.markdown("<h1 style='text-align:center; color:#2d3748'>🎵 全局歌曲播放时长TOP10</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # 查询全局歌曲播放统计
    hot_songs_sql = """
        SELECT ps.song_id, ms.song_name, ms.cover_url, ps.total_play_dur, ps.play_count
        FROM play_stat_song ps
        JOIN music_song ms ON ps.song_id = ms.song_id
        WHERE ps.user_id IS NULL
        ORDER BY ps.total_play_dur DESC
        LIMIT 10;
    """
    hot_songs = get_db_data(hot_songs_sql)

    if not hot_songs.empty:
        # 分两行显示，每行5个
        cols1 = st.columns(5)
        for idx in range(5):
            if idx < len(hot_songs):
                row = hot_songs.iloc[idx]
                with cols1[idx]:
                    st.markdown(f"<div class='hot-song-card'>", unsafe_allow_html=True)
                    st.image(row['cover_url'], width=150)
                    st.markdown(f"<h3>TOP{idx + 1} {row['song_name']}</h3>", unsafe_allow_html=True)
                    st.caption(f"总时长：{round(row['total_play_dur'] / 60, 1)}分钟")
                    st.caption(f"播放次数：{row['play_count']}次")
                    st.markdown("</div>", unsafe_allow_html=True)

        cols2 = st.columns(5)
        for idx in range(5, 10):
            if idx < len(hot_songs):
                row = hot_songs.iloc[idx]
                with cols2[idx - 5]:
                    st.markdown(f"<div class='hot-song-card'>", unsafe_allow_html=True)
                    st.image(row['cover_url'], width=150)
                    st.markdown(f"<h3>TOP{idx + 1} {row['song_name']}</h3>", unsafe_allow_html=True)
                    st.caption(f"总时长：{round(row['total_play_dur'] / 60, 1)}分钟")
                    st.caption(f"播放次数：{row['play_count']}次")
                    st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='text-align:center; color:#2d3748'>暂无歌曲播放数据！</p>", unsafe_allow_html=True)

# ---------- 2. 登录页 ----------
elif st.session_state.current_page == "login":
    st.markdown("<h1 style='text-align:center; color:#2d3748'>🎵 用户登录</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # 居中登录表单
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user_id = st.text_input("账号", placeholder="U001/U002/U003", key="login_user")
        password = st.text_input("密码", type="password", placeholder="初始密码与账号相同", key="login_pwd")

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("登录", use_container_width=True):
                user_login(user_id, password)
        with col_btn2:
            if st.button("返回首页", use_container_width=True):
                switch_page("home")

# ---------- 3. 全局曲风统计页面 ----------
elif st.session_state.current_page == "global_style":
    st.markdown("<h1 style='text-align:center; color:#2d3748'>🌍 全局曲风播放统计</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div class='style-rank'>", unsafe_allow_html=True)

    # 查询全局曲风统计数据
    style_stat_sql = """
        SELECT song_style, total_play_dur, play_count
        FROM play_stat_style
        WHERE user_id IS NULL
        ORDER BY total_play_dur DESC;
    """
    style_stat = get_db_data(style_stat_sql)

    if not style_stat.empty:
        for idx, (_, row) in enumerate(style_stat.iterrows(), 1):
            st.markdown(f"""
                <div class='stat-item'>
                    <h4>TOP{idx}：{row['song_style']}</h4>
                    <p>总播放时长：{round(row['total_play_dur'] / 60, 1)}分钟 | 播放次数：{row['play_count']}次</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("---")
    else:
        st.markdown("<p style='text-align:center; color:#2d3748'>暂无曲风播放数据！</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("返回首页", use_container_width=True):
        switch_page("home")

# ---------- 4. 曲风排行页  ----------
elif st.session_state.current_page == "style":
    st.markdown("<h1 style='text-align:center; color:#2d3748'>🎵 曲风热度排行</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div class='style-rank'>", unsafe_allow_html=True)

    style_rank = get_db_data("""
        SELECT s.song_style, SUM(s.hot_score) as total_hot, COUNT(DISTINCT s.song_id) as song_count
        FROM music_song s GROUP BY s.song_style ORDER BY total_hot DESC
    """)

    if not style_rank.empty:
        for _, row in style_rank.iterrows():
            style_name = row['song_style']
            st.markdown(f"""
                <div class='style-item'>
                    <div>
                        <div style='font-size:18px; font-weight:500'>{style_name}</div>
                        <div style='color:#667eea'>总热度：{row['total_hot']} | 歌曲数：{row['song_count']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            if st.button(f"查看{style_name} TOP10", key=f"style_{style_name}", use_container_width=True):
                st.session_state.selected_style = style_name
                switch_page("style_detail")
    else:
        st.markdown("<p style='text-align:center; color:#2d3748'>暂无曲风数据！</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("返回首页", use_container_width=True):
        switch_page("home")

# ---------- 5. 曲风TOP10详情页 ----------
elif st.session_state.current_page == "style_detail":
    selected_style = st.session_state.selected_style
    st.markdown(f"<h1 style='text-align:center; color:#2d3748'>{selected_style} 曲风 TOP10 歌曲</h1>",
                unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div class='style-rank'>", unsafe_allow_html=True)

    style_songs = get_db_data(f"""
        SELECT s.song_name, s.cover_url, s.hot_score
        FROM music_song s WHERE s.song_style = '{selected_style}'
        ORDER BY s.hot_score DESC LIMIT 10
    """)

    if not style_songs.empty:
        for idx, (_, row) in enumerate(style_songs.iterrows(), 1):
            col_img, col_info = st.columns([1, 5])
            with col_img:
                st.image(row['cover_url'], width=60)  # 小封面
            with col_info:
                st.write(f"**TOP{idx}：{row['song_name']}**")
                st.caption(f"热度：{row['hot_score']}")
            st.markdown("---")
    else:
        st.markdown(f"<p style='text-align:center; color:#2d3748'>暂无{selected_style}曲风数据！</p>",
                    unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("返回曲风排行", use_container_width=True):
            switch_page("style")
    with col2:
        if st.button("返回首页", use_container_width=True):
            switch_page("home")

# ---------- 6. 歌手列表页 ----------
elif st.session_state.current_page == "singer":
    st.markdown("<h1 style='text-align:center; color:#2d3748'>🎤 歌手</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div class='singer-book'>", unsafe_allow_html=True)

    all_singers = get_db_data("""
        SELECT singer_id, singer_name, initial, song_style
        FROM singer_info ORDER BY initial, singer_name
    """)

    if not all_singers.empty:
        current_letter = ""
        for _, row in all_singers.iterrows():
            letter = row['initial']
            if letter != current_letter:
                current_letter = letter
                st.markdown(f"<div class='letter-title'>{current_letter}</div>", unsafe_allow_html=True)

            if st.button(f"🎤 {row['singer_name']} - 代表曲风：{row['song_style']}",
                         key=f"singer_{row['singer_id']}", use_container_width=True):
                st.session_state.selected_singer_id = row['singer_id']
                st.session_state.selected_singer_name = row['singer_name']
                switch_page("singer_detail")
    else:
        st.markdown("<p style='text-align:center; color:#2d3748'>暂无歌手数据！</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("返回首页", use_container_width=True):
        switch_page("home")

# ---------- 7. 歌手TOP10详情页  ----------
elif st.session_state.current_page == "singer_detail":
    singer_name = st.session_state.selected_singer_name
    singer_id = st.session_state.selected_singer_id
    st.markdown(f"<h1 style='text-align:center; color:#2d3748'>{singer_name} TOP10 热门歌曲</h1>",
                unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div class='style-rank'>", unsafe_allow_html=True)

    singer_songs = get_db_data(f"""
        SELECT s.song_name, s.cover_url, s.hot_score
        FROM music_song s WHERE s.singer_id = '{singer_id}'
        ORDER BY s.hot_score DESC LIMIT 10
    """)

    if not singer_songs.empty:
        for idx, (_, row) in enumerate(singer_songs.iterrows(), 1):
            col_img, col_info = st.columns([1, 5])
            with col_img:
                st.image(row['cover_url'], width=60)  # 小封面
            with col_info:
                st.write(f"**TOP{idx}：{row['song_name']}**")
                st.caption(f"热度：{row['hot_score']}")
            st.markdown("---")
    else:
        st.markdown(f"<p style='text-align:center; color:#2d3748'>暂无{singer_name}的歌曲数据！</p>",
                    unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("返回歌手列表", use_container_width=True):
            switch_page("singer")
    with col2:
        if st.button("返回首页", use_container_width=True):
            switch_page("home")

# ---------- 8. 个人中心  ----------
elif st.session_state.current_page == "user":
    if not st.session_state.logged_in:
        switch_page("login")
        st.stop()

    current_user = st.session_state.current_user
    st.markdown(f"<h1 style='text-align:center; color:#2d3748'>👤 个人中心 - {current_user}</h1>",
                unsafe_allow_html=True)
    st.markdown("---")

    # 分标签页显示：个人歌曲统计、个人曲风统计、最近播放记录
    tab1, tab2, tab3 = st.tabs(["🎵 我的歌曲播放统计", "🎶 我的曲风播放统计", "🕒 最近播放记录"])

    # 标签1：个人歌曲播放统计（从play_stat_song查询）
    with tab1:
        st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
        st.subheader("我的歌曲播放时长TOP10")

        user_song_sql = f"""
            SELECT ps.song_id, ms.song_name, ms.cover_url, ps.total_play_dur, ps.play_count
            FROM play_stat_song ps
            JOIN music_song ms ON ps.song_id = ms.song_id
            WHERE ps.user_id = '{current_user}'
            ORDER BY ps.total_play_dur DESC
            LIMIT 10;
        """
        user_song_stat = get_db_data(user_song_sql)

        if not user_song_stat.empty:
            for idx, (_, row) in enumerate(user_song_stat.iterrows(), 1):
                col_img, col_info = st.columns([1, 5])
                with col_img:
                    st.image(row['cover_url'], width=60)
                with col_info:
                    st.write(f"**TOP{idx}：{row['song_name']}**")
                    st.caption(f"总时长：{round(row['total_play_dur'] / 60, 1)}分钟 | 播放次数：{row['play_count']}次")
                st.markdown("---")
        else:
            st.write("暂无歌曲播放记录！")
        st.markdown("</div>", unsafe_allow_html=True)

    # 标签2：个人曲风播放统计（从play_stat_style查询 + 饼图+树状图）
    with tab2:
        st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
        st.subheader("我的曲风播放时长排行")

        user_style_sql = f"""
            SELECT song_style, total_play_dur, play_count
            FROM play_stat_style
            WHERE user_id = '{current_user}'
            ORDER BY total_play_dur DESC;
        """
        user_style_stat = get_db_data(user_style_sql)

        if not user_style_stat.empty:
            # 1. 展示文字统计数据
            for idx, (_, row) in enumerate(user_style_stat.iterrows(), 1):
                st.markdown(f"""
                    <div class='stat-item'>
                        <h4>TOP{idx}：{row['song_style']}</h4>
                        <p>总播放时长：{round(row['total_play_dur'] / 60, 1)}分钟 | 播放次数：{row['play_count']}次</p>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown("---")

            # 2.曲风播放时长饼图（占比）
            st.subheader("🎯 我的曲风播放占比（饼图）")
            import plotly.express as px

            # 数据处理：转换时长为分钟，添加占比标签
            user_style_stat['duration_min'] = user_style_stat['total_play_dur'] / 60
            user_style_stat['percent'] = (user_style_stat['total_play_dur'] / user_style_stat[
                'total_play_dur'].sum() * 100).round(1).astype(str) + '%'

            # 绘制饼图
            pie_fig = px.pie(
                user_style_stat,
                values='total_play_dur',
                names='song_style',
                title=f'{current_user}的曲风播放时长占比',
                hover_data=['duration_min', 'play_count', 'percent'],
                labels={'duration_min': '总时长(分钟)', 'play_count': '播放次数', 'percent': '占比'}
            )
            # 美化饼图
            pie_fig.update_traces(textposition='inside', textinfo='percent+label')
            pie_fig.update_layout(height=400)
            st.plotly_chart(pie_fig, use_container_width=True)

            # 3.曲风-歌曲层级树状图（旭日图）
            st.subheader("🌳 曲风-歌曲播放时长层级（树状图）")
            # 查询用户的曲风-歌曲关联数据
            song_style_tree_sql = f"""
                SELECT 
                    ms.song_style,  # 正确：从music_song表获取曲风
                    ms.song_name,
                    ps.total_play_dur
                FROM play_stat_song ps
                JOIN music_song ms ON ps.song_id = ms.song_id
                WHERE ps.user_id = '{current_user}'
                ORDER BY ps.total_play_dur DESC;
            """
            song_style_tree = get_db_data(song_style_tree_sql)

            if not song_style_tree.empty:
                # 数据处理：转换时长为分钟
                song_style_tree['duration_min'] = song_style_tree['total_play_dur'] / 60
                # 绘制旭日图（树状图）
                tree_fig = px.sunburst(
                    song_style_tree,
                    path=['song_style', 'song_name'],  # 层级：曲风→歌曲
                    values='total_play_dur',
                    title=f'{current_user}的曲风-歌曲播放时长层级',
                    hover_data=['duration_min'],
                    labels={'duration_min': '总时长(分钟)'}
                )
                tree_fig.update_layout(height=500)
                st.plotly_chart(tree_fig, use_container_width=True)
            else:
                st.info("暂无曲风-歌曲的详细数据，无法生成树状图～")
        else:
            st.write("暂无曲风播放记录！")
            # 无数据时显示空图表提示
            st.info("暂无数据，无法生成可视化图表～")
        st.markdown("</div>", unsafe_allow_html=True)

    # 标签3：新增最近播放记录（从user_play_record查询）
    with tab3:
        st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
        st.subheader("最近播放的10首歌曲")

        # 查询最近播放记录（按播放时间倒序）
        play_history_sql = f"""
            SELECT upr.play_time, ms.song_name, ms.cover_url, upr.play_dur
            FROM user_play_record upr
            JOIN music_song ms ON upr.song_id = ms.song_id
            WHERE upr.user_id = '{current_user}'
            ORDER BY upr.play_time DESC
            LIMIT 10;
        """
        play_history = get_db_data(play_history_sql)

        if not play_history.empty:
            for _, row in play_history.iterrows():
                # 格式化播放时间和时长
                play_time = row['play_time'].strftime("%Y-%m-%d %H:%M:%S")
                play_dur = round(row['play_dur'] / 60, 1)

                col_img, col_info = st.columns([1, 5])
                with col_img:
                    st.image(row['cover_url'], width=60)
                with col_info:
                    st.write(f"**{row['song_name']}**")
                    st.caption(f"播放时间：{play_time}")
                    st.caption(f"播放时长：{play_dur}分钟")
                st.markdown("---")
        else:
            st.write("暂无播放历史记录！")
        st.markdown("</div>", unsafe_allow_html=True)

    # 退出/返回按钮（添加唯一key）
    col1, col2 = st.columns(2)
    with col1:
        if st.button("退出登录", use_container_width=True, key="user_center_logout_btn"):  # 唯一key
            user_logout()
    with col2:
        if st.button("返回首页", use_container_width=True, key="user_center_home_btn"):  # 唯一key
            switch_page("home")


st.markdown("</div>", unsafe_allow_html=True)
