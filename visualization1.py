import streamlit as st
import pymysql
import pandas as pd
from datetime import datetime, date, timedelta
import os
import plotly.express as px

# ===================== ✅✅✅ 全局核心修复：把配色列表提到最顶部，全局变量，所有模块可调用 ✅✅✅
color_list = ['#1f77b4', '#d62728', '#2ca02c', '#ff7f0e', '#9467bd', '#8c564b', '#e377c2']

# ===================== 全局配置 =====================
st.set_page_config(
    page_title="音乐偏好分析系统",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS（紧凑布局+全紫色系+无CSS错误）
st.markdown("""
    <style>
    .main {background-color: #f9f7ff !important;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .page-container {max-width: 1200px; margin: 0 auto; padding: 10px 20px;background: transparent !important;}
    .hot-song-card {background: white; border-radius: 15px; padding: 12px;margin: 8px; text-align: center; width: 170px;border: 1px solid #e9e3ff; box-shadow: 0 1px 5px rgba(123,74,221,0.05);}
    .hot-song-card h3 {font-size: 14px; color: #5a389e; margin-top: 8px;}
    .style-rank, .singer-book, .stat-card {max-width: 900px; margin: 0 auto; background: transparent !important;padding: 0; border-radius: 0; box-shadow: none !important;}
    .style-item, .singer-item {padding: 12px; margin: 8px 0; border-radius: 8px;background: #f5f3ff; display: flex; justify-content: space-between;align-items: center;border-left: 4px solid #7b4add;}
    .letter-title {font-size: 19px; font-weight: bold; color: #7b4add;padding: 8px 0; border-bottom: 1px solid #e9e3ff;margin-top: 15px;}
    div[data-testid="stSidebar"] button {background: #7b4add !important; color: white !important;border-radius: 6px !important; border: none !important;padding: 8px !important; margin: 5px 0 !important;}
    div[data-testid="stSidebar"] button:hover {background: #6a3cb8 !important;}
    .stat-item {padding: 8px; margin: 4px 0; border-left: 4px solid #7b4add;background: #f5f3ff; border-radius: 6px;}
    .style-tag {display: inline-block; padding: 4px 12px; margin: 0 4px 8px 0;background: #7b4add; color: white; border-radius: 20px; font-size: 13px;}
    h1 {font-size: 24px !important; color: #5a389e !important; margin: 10px 0 !important;}
    h2 {font-size: 20px !important; color: #5a389e !important; margin: 8px 0 !important;}
    h3 {font-size: 18px !important; color: #5a389e !important; margin: 6px 0 !important;}
    h4 {font-size: 16px !important; color: #7b4add !important; margin: 5px 0 !important;}
    p, span, div {color: #2d3748 !important; line-height: 1.4 !important;}
    .stMarkdown, .stButton, .stPlotlyChart {margin: 5px 0 !important;}
    .stImage {margin: 3px 0 !important;}
    </style>
""", unsafe_allow_html=True)

# ===================== 数据库配置 =====================
DB_CONFIG = {
    "host": "192.168.222.128",
    "port": 3306,
    "user": "xxxxxxx",
    "password": "xxxxxxx",
    "database": "music_analysis",
    "charset": "utf8mb4"
}


# 数据库查询函数-异常捕获优化
def get_db_data(sql):
    try:
        conn = pymysql.connect(**DB_CONFIG)
        df = pd.read_sql(sql, conn)
        conn.close()
        return df
    except Exception as e:
        st.warning(f"数据库查询提示：{str(e)}")
        return pd.DataFrame()


#  ✅✅✅ 核心新增：真实歌曲热度计算函数  ✅✅✅
def calculate_real_hot_score(song_id):
    """
    计算歌曲真实热度值，基于数据库中【所有用户的播放行为】综合计算，真实有效，非固定值
    热度计算逻辑：播放次数×权重 + 播放时长加权 - 时间衰减，贴合真实音乐平台热度规则
    :param song_id: 歌曲ID
    :return: 整数类型的真实热度值
    """
    # 1. 查询该歌曲的所有播放记录
    play_sql = f"SELECT play_dur, play_time FROM user_play_record WHERE song_id = '{song_id}'"
    play_data = get_db_data(play_sql)

    if play_data.empty:
        return 10  # 无播放记录的歌曲默认基础热度

    play_count = len(play_data)  # 总播放次数
    total_play_dur = play_data['play_dur'].sum()  # 总播放时长
    last_play_time = pd.to_datetime(play_data['play_time'].max())  # 最后播放时间

    # 2. 热度核心计算公式：播放次数(占50%) + 播放时长加权(占50%)
    # 播放时长每300秒(5分钟)加10分，避免短播放刷热度
    dur_score = int(total_play_dur / 300 * 10)
    base_score = play_count * 8 + dur_score

    # 3. 时间衰减机制：越近播放的歌曲热度越高，超过7天的播放行为逐步衰减
    days_diff = (datetime.now() - last_play_time).days
    decay_rate = (0.92) ** days_diff  # 衰减系数，每天衰减8%
    real_hot = int(base_score * decay_rate)

    # 4. 热度值边界限制：最低10分，最高999分，防止数值异常
    return max(min(real_hot, 999), 10)


# ===================== 本地封面路径配置-100%解决路径报错 ========================
COVER_BASE_PATH = r"D:\PyCharmMiscProject\music_project\data\song_covers"
DEFAULT_COVER = None

if os.path.exists(COVER_BASE_PATH):
    for file_name in os.listdir(COVER_BASE_PATH):
        if file_name.startswith("default_cover"):
            DEFAULT_COVER = os.path.join(COVER_BASE_PATH, file_name)
            break

if DEFAULT_COVER is None or not os.path.exists(DEFAULT_COVER):
    DEFAULT_COVER = "https://picsum.photos/id/1019/150/150"

st.markdown(f"<p style='font-size:12px; color:#666;'>✅ 封面加载完成：{os.path.basename(DEFAULT_COVER)}</p>",
            unsafe_allow_html=True)

# ===================== Session State初始化 =====================
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
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
    st.rerun()


def user_login(user_id, password):
    user_id = user_id.strip() if user_id else ""
    password = password.strip() if password else ""
    if not user_id or not password:
        st.warning("账号密码不能为空！")
        return False

    df = get_db_data(f"SELECT * FROM user_info WHERE user_id='{user_id}' AND password='{password}'")
    if not df.empty:
        st.session_state.logged_in = True
        st.session_state.current_user = user_id
        st.success(f"登录成功！欢迎 {df.iloc[0]['user_name']}")
        switch_page("home")
        return True
    else:
        st.error("账号密码错误！(测试账号：U001/U002/U003，密码与账号相同)")
        return False


def user_logout():
    st.session_state.logged_in = False
    st.session_state.current_user = ""
    st.success("退出登录成功！")
    switch_page("home")


# ===================== 左侧侧边栏菜单 =====================
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#7b4add'>🎵 音乐推荐系统</h2>", unsafe_allow_html=True)
    st.markdown("---")

    if st.session_state.logged_in:
        st.markdown(f"<p style='text-align:center; color:#2d3748'>当前账号：{st.session_state.current_user}</p>",
                    unsafe_allow_html=True)
        if st.button("退出登录", use_container_width=True, key="logout_btn"):
            user_logout()
    else:
        if st.button("用户登录", use_container_width=True, key="login_btn"):
            switch_page("login")

    st.markdown("---")
    st.markdown("<h4 style='color:#2d3748'>📌 功能菜单</h4>", unsafe_allow_html=True)

    menu_btns = [
        ("🏠 首页", "home_btn", "home"),
        ("🌍 全局曲风统计", "global_style_btn", "global_style"),
        ("🎶 曲风热度排行", "style_btn", "style"),
        ("🎤 歌手列表", "singer_btn", "singer"),
        ("👤 个人中心", "user_btn", "user")
    ]
    for btn_name, btn_key, page_name in menu_btns:
        if st.button(btn_name, use_container_width=True, key=btn_key):
            if page_name == "user" and not st.session_state.logged_in:
                st.warning("请先登录后再进入个人中心！")
                switch_page("login")
            else:
                switch_page(page_name)

# ===================== 页面渲染【完整无报错+全局配色变量+柱状图+独立趋势图配色+真实热度】 =====================
st.markdown("<div class='page-container'>", unsafe_allow_html=True)

# ---------- 1. 首页 -----------
if st.session_state.current_page == "home":
    if not st.session_state.logged_in:
        st.markdown("<h1 style='text-align:center; color:#7b4add; margin-bottom:20px;'>🎵 全平台热门推荐</h1>",
                    unsafe_allow_html=True)
    else:
        current_user = st.session_state.current_user
        st.markdown(
            f"<h1 style='text-align:center; color:#7b4add; margin-bottom:20px;'>🎵 为你推荐 · {current_user}</h1>",
            unsafe_allow_html=True)
    st.markdown("---")

    if not st.session_state.logged_in:
        st.markdown("<h2 style='color:#5a389e; margin-bottom:15px;'>🔥 歌曲热度TOP10</h2>", unsafe_allow_html=True)
        hot_songs_sql = """
            SELECT ms.song_id, ms.song_name, si.singer_name
            FROM music_song ms
            JOIN singer_info si ON ms.singer_id = si.singer_id
            ORDER BY ms.song_id;
        """
        hot_songs = get_db_data(hot_songs_sql)
        if not hot_songs.empty:
            # 为每首歌计算真实热度
            hot_songs['hot_score'] = hot_songs['song_id'].apply(calculate_real_hot_score)
            hot_songs = hot_songs.sort_values('hot_score', ascending=False).head(10)
            hot_songs['cover_url'] = DEFAULT_COVER
            cols = st.columns(5)
            for idx, (_, row) in enumerate(hot_songs.iterrows()):
                with cols[idx % 5]:
                    st.markdown(f"<div class='hot-song-card'>", unsafe_allow_html=True)
                    st.image(row['cover_url'], width=120)
                    st.markdown(f"<h3 style='font-size:14px;'>{row['song_name']}</h3>", unsafe_allow_html=True)
                    st.caption(f"歌手：{row['singer_name']}")
                    st.caption(f"热度：{row['hot_score']}")
                    st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("🎶 按曲风推荐热门歌曲", anchor=False)
        style_list = get_db_data("SELECT DISTINCT song_style FROM music_song;")['song_style'].tolist()
        for style in style_list:
            st.markdown(f"<h4 style='color:#7b4add; margin-top:10px;'>{style}</h4>", unsafe_allow_html=True)
            style_songs_sql = f"""
                SELECT ms.song_id, ms.song_name, si.singer_name FROM music_song ms
                JOIN singer_info si ON ms.singer_id = si.singer_id
                WHERE ms.song_style = '{style}';
            """
            style_songs = get_db_data(style_songs_sql)
            if not style_songs.empty:
                style_songs['hot_score'] = style_songs['song_id'].apply(calculate_real_hot_score)
                style_songs = style_songs.sort_values('hot_score', ascending=False).head(4)
                style_songs['cover_url'] = DEFAULT_COVER
                cols = st.columns(4)
                for idx, (_, row) in enumerate(style_songs.iterrows()):
                    with cols[idx]:
                        st.image(row['cover_url'], width=80)
                        st.write(f"{row['song_name']} - {row['singer_name']}")
            st.markdown("---")

    else:
        current_user = st.session_state.current_user
        st.markdown(f"<h2 style='color:#5a389e; margin-bottom:15px;'>💖 你的专属推荐</h2>", unsafe_allow_html=True)
        style_pre_sql = f"""SELECT song_style, style_hot FROM play_stat_style WHERE user_id = '{current_user}';"""
        style_pre_data = get_db_data(style_pre_sql)

        top_styles = []
        if not style_pre_data.empty and len(style_pre_data) >= 2:
            top_styles = style_pre_data['song_style'].tolist()[:2]
        else:
            top_styles = ["pop", "R&B"]

        for style in top_styles:
            st.markdown(f"<h4 style='color:#7b4add; margin-top:10px;'>你喜欢的 {style} 曲风</h4>",
                        unsafe_allow_html=True)
            heard_songs_sql = f"""SELECT DISTINCT song_id FROM user_play_record WHERE user_id = '{current_user}';"""
            heard_songs = get_db_data(heard_songs_sql)
            heard_song_ids = tuple(heard_songs['song_id'].tolist()) if not heard_songs.empty else ('-1',)

            rec_sql = f"""
                SELECT ms.song_id, ms.song_name, si.singer_name FROM music_song ms
                JOIN singer_info si ON ms.singer_id = si.singer_id
                WHERE ms.song_style = '{style}' AND ms.song_id NOT IN {heard_song_ids};
            """
            rec_songs = get_db_data(rec_sql)
            if not rec_songs.empty:
                rec_songs['hot_score'] = rec_songs['song_id'].apply(calculate_real_hot_score)
                rec_songs = rec_songs.sort_values('hot_score', ascending=False).head(6)
                rec_songs['cover_url'] = DEFAULT_COVER
                cols = st.columns(3)
                for idx, (_, row) in enumerate(rec_songs.iterrows()):
                    with cols[idx % 3]:
                        st.image(row['cover_url'], width=100)
                        st.write(f"**{row['song_name']}**")
                        st.caption(f"{row['singer_name']} | 热度{row['hot_score']}")
            else:
                st.info(f"暂无{style}曲风的新歌曲推荐~")
            st.markdown("---")

        st.markdown("<h4 style='color:#5a389e; marginTop:15px;'>🔥 全平台热门补充</h4>", unsafe_allow_html=True)
        hot_supp_sql = """SELECT ms.song_id, ms.song_name, si.singer_name FROM music_song ms JOIN singer_info si ON ms.singer_id = si.singer_id;"""
        hot_supp = get_db_data(hot_supp_sql)
        if not hot_supp.empty:
            hot_supp['hot_score'] = hot_supp['song_id'].apply(calculate_real_hot_score)
            hot_supp = hot_supp.sort_values('hot_score', ascending=False).head(4)
            hot_supp['cover_url'] = DEFAULT_COVER
            cols = st.columns(4)
            for idx, (_, row) in enumerate(hot_supp.iterrows()):
                with cols[idx]:
                    st.image(row['cover_url'], width=80)
                    st.write(f"{row['song_name']}")
                    st.caption(f"{row['singer_name']}")

# ---------- 2. 登录页 ----------
elif st.session_state.current_page == "login":
    st.markdown("<h1 style='text-align:center; color:#2d3748'>🎵 用户登录</h1>", unsafe_allow_html=True)
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user_id = st.text_input("账号", placeholder="请输入账号 U001/U002/U003", key="login_user")
        password = st.text_input("密码", type="password", placeholder="初始密码与账号相同", key="login_pwd")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("登录", use_container_width=True):
                user_login(user_id, password)
        with col_btn2:
            if st.button("返回首页", use_container_width=True):
                switch_page("home")

# ---------- 3. 全局曲风统计页面 ✅【每个曲风趋势图独立配色】 ----------
elif st.session_state.current_page == "global_style":
    st.markdown("<h1 style='text-align:center; color:#2d3748'>🌍 全局曲风播放统计</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div class='style-rank'>", unsafe_allow_html=True)

    st.subheader("📊 全局曲风播放总览")
    style_stat_sql = """SELECT ms.song_style, SUM(upr.play_dur) AS total_play_dur, COUNT(*) AS play_count FROM user_play_record upr JOIN music_song ms ON upr.song_id = ms.song_id GROUP BY ms.song_style ORDER BY play_count DESC;"""
    style_stat = get_db_data(style_stat_sql)
    if not style_stat.empty:
        for idx, (_, row) in enumerate(style_stat.iterrows(), 1):
            st.markdown(
                f"""<div class='stat-item'><h4>TOP{idx}：{row['song_style']}</h4><p>总播放时长：{round(row['total_play_dur'] / 60, 1)}分钟 | 播放次数：{row['play_count']}次</p></div>""",
                unsafe_allow_html=True)
            st.markdown("---")
    else:
        st.markdown("<p style='text-align:center; color:#2d3748'>暂无曲风播放数据！</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📈 各曲风24小时热度趋势")
    top5_styles_sql = """SELECT ms.song_style FROM user_play_record upr JOIN music_song ms ON upr.song_id = ms.song_id GROUP BY ms.song_style ORDER BY COUNT(*) DESC LIMIT 5;"""
    top5_styles = get_db_data(top5_styles_sql)

    if not top5_styles.empty:
        style_list = top5_styles['song_style'].tolist()
        for idx, style in enumerate(style_list):
            current_color = color_list[idx % len(color_list)]
            hour_hot_sql = f"""SELECT HOUR(upr.play_time) AS play_hour,COUNT(*) AS play_count,SUM(upr.play_dur) AS total_dur,ROUND(COUNT(*)*0.6 + (SUM(upr.play_dur)/300)*300) AS hour_hot FROM user_play_record upr JOIN music_song ms ON upr.song_id = ms.song_id WHERE ms.song_style = '{style}' GROUP BY HOUR(upr.play_time) ORDER BY play_hour;"""
            hour_hot_data = get_db_data(hour_hot_sql)
            all_hours = pd.DataFrame({'play_hour': range(24)})
            hour_hot_data = pd.merge(all_hours, hour_hot_data, on='play_hour', how='left')
            hour_hot_data['hour_hot'] = hour_hot_data['hour_hot'].fillna(0)
            hour_hot_data['time_point'] = hour_hot_data['play_hour'].apply(lambda x: f"{x:02d}:00")

            fig = px.line(
                hour_hot_data,
                x='time_point',
                y='hour_hot',
                title=f'{style} 曲风24小时热度趋势',
                labels={'time_point': '播放时间（整点）', 'hour_hot': '曲风热度值'},
                line_shape='spline',
                color_discrete_sequence=[current_color],
                height=280
            )
            fig.update_layout(
                title_font={'size': 16, 'color': current_color},
                xaxis=dict(tickmode='array', tickvals=hour_hot_data['time_point'][::3], tickangle=0,
                           title_font={'size': 14}),
                yaxis=dict(title_font={'size': 14}),
                plot_bgcolor='rgba(255,255,255,0.8)',
                paper_bgcolor='rgba(255,255,255,0)',
                margin=dict(l=10, r=10, t=40, b=10),
                showlegend=False
            )
            fig.update_traces(hovertemplate='时间：%{x}<br>热度：%{y}', line=dict(width=3))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("---")
    else:
        st.info("暂无足够的曲风数据，无法生成趋势图～")

    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("返回首页", use_container_width=True):
        switch_page("home")

# ---------- 4. 曲风排行页 ----------
elif st.session_state.current_page == "style":
    st.markdown("<h1 style='text-align:center; color:#2d3748'>🎵 曲风热度排行</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div class='style-rank'>", unsafe_allow_html=True)
    # 查询曲风+所有歌曲，计算每首歌真实热度后聚合曲风总热度
    style_rank_sql = """SELECT s.song_style, s.song_id FROM music_song s"""
    style_song_data = get_db_data(style_rank_sql)
    if not style_song_data.empty:
        style_song_data['hot_score'] = style_song_data['song_id'].apply(calculate_real_hot_score)
        style_rank = style_song_data.groupby('song_style').agg(
            total_hot=('hot_score', 'sum'),
            song_count=('song_id', 'nunique')
        ).reset_index().sort_values('total_hot', ascending=False)

        for _, row in style_rank.iterrows():
            style_name = row['song_style']
            st.markdown(
                f"""<div class='style-item'><div><div style='font-size:18px; font-weight:500'>{style_name}</div><div style='color:#7b4add'>总热度：{row['total_hot']} | 歌曲数：{row['song_count']}</div></div></div>""",
                unsafe_allow_html=True)
            if st.button(f"查看{style_name} TOP10", key=f"style_btn_{style_name}", use_container_width=True):
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
    style_songs = get_db_data(
        f"""SELECT s.song_id, s.song_name FROM music_song s WHERE s.song_style = '{selected_style}'""")
    if not style_songs.empty:
        style_songs['hot_score'] = style_songs['song_id'].apply(calculate_real_hot_score)
        style_songs = style_songs.sort_values('hot_score', ascending=False).head(10)
        style_songs['cover_url'] = DEFAULT_COVER
        for idx, (_, row) in enumerate(style_songs.iterrows(), 1):
            col_img, col_info = st.columns([1, 5])
            with col_img: st.image(row['cover_url'], width=60)
            with col_info: st.write(f"**TOP{idx}：{row['song_name']}**");st.caption(f"热度：{row['hot_score']}")
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
    st.markdown("<h1 style='text-align:center; color:#2d3748'>🎤 歌手列表</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div class='singer-book'>", unsafe_allow_html=True)
    all_singers = get_db_data(
        """SELECT singer_id, singer_name, initial, song_style FROM singer_info ORDER BY initial, singer_name""")
    if not all_singers.empty:
        current_letter = ""
        for _, row in all_singers.iterrows():
            letter = row['initial']
            if letter != current_letter:
                current_letter = letter
                st.markdown(f"<div class='letter-title'>{current_letter}</div>", unsafe_allow_html=True)
            if st.button(f"🎤 {row['singer_name']} - 代表曲风：{row['song_style']}", key=f"singer_btn_{row['singer_id']}",
                         use_container_width=True):
                st.session_state.selected_singer_id = row['singer_id']
                st.session_state.selected_singer_name = row['singer_name']
                switch_page("singer_detail")
    else:
        st.markdown("<p style='text-align:center; color:#2d3748'>暂无歌手数据！</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("返回首页", use_container_width=True):
        switch_page("home")

# ---------- 7. 歌手TOP10详情页 ----------
elif st.session_state.current_page == "singer_detail":
    singer_name = st.session_state.selected_singer_name
    singer_id = st.session_state.selected_singer_id
    st.markdown(f"<h1 style='text-align:center; color:#2d3748'>{singer_name} TOP10 热门歌曲</h1>",
                unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div class='style-rank'>", unsafe_allow_html=True)
    singer_songs = get_db_data(
        f"""SELECT s.song_id, s.song_name FROM music_song s WHERE s.singer_id = '{singer_id}'""")
    if not singer_songs.empty:
        singer_songs['hot_score'] = singer_songs['song_id'].apply(calculate_real_hot_score)
        singer_songs = singer_songs.sort_values('hot_score', ascending=False).head(10)
        singer_songs['cover_url'] = DEFAULT_COVER
        for idx, (_, row) in enumerate(singer_songs.iterrows(), 1):
            col_img, col_info = st.columns([1, 5])
            with col_img: st.image(row['cover_url'], width=60)
            with col_info: st.write(f"**TOP{idx}：{row['song_name']}**");st.caption(f"热度：{row['hot_score']}")
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

# ---------- 8. 个人中心 ✅【猜你爱听柱状图+所有功能保留+真实热度】 ----------
elif st.session_state.current_page == "user":
    if not st.session_state.logged_in:
        switch_page("login")

    current_user = st.session_state.current_user
    st.markdown(f"<h1 style='text-align:center; color:#2d3748'>👤 个人中心 - {current_user}</h1>",
                unsafe_allow_html=True)
    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs(
        ["🎵 我的歌曲播放统计", "🎶 我的曲风播放统计", "🕒 最近播放记录", "💖 猜你爱听 & 偏好分析"])

    with tab1:
        st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
        st.subheader("我的歌曲播放时长TOP10")
        user_song_sql = f"""SELECT ps.song_id, ms.song_name, ps.total_play_dur, ps.play_count FROM play_stat_song ps JOIN music_song ms ON ps.song_id = ms.song_id WHERE ps.user_id = '{current_user}' ORDER BY ps.total_play_dur DESC LIMIT 10;"""
        user_song_stat = get_db_data(user_song_sql)
        if not user_song_stat.empty:
            user_song_stat['cover_url'] = DEFAULT_COVER
            for idx, (_, row) in enumerate(user_song_stat.iterrows(), 1):
                col_img, col_info = st.columns([1, 5])
                with col_img: st.image(row['cover_url'], width=60)
                with col_info: st.write(f"**TOP{idx}：{row['song_name']}**");st.caption(
                    f"总时长：{round(row['total_play_dur'] / 60, 1)}分钟 | 播放次数：{row['play_count']}次")
                st.markdown("---")
        else:
            st.write("暂无歌曲播放记录！")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
        st.subheader("我的曲风播放时长排行")
        user_style_sql = f"""SELECT song_style, total_play_dur, play_count FROM play_stat_style WHERE user_id = '{current_user}' ORDER BY total_play_dur DESC;"""
        user_style_stat = get_db_data(user_style_sql)
        if not user_style_stat.empty:
            for idx, (_, row) in enumerate(user_style_stat.iterrows(), 1):
                st.markdown(
                    f"""<div class='stat-item'><h4>TOP{idx}：{row['song_style']}</h4><p>总播放时长：{round(row['total_play_dur'] / 60, 1)}分钟 | 播放次数：{row['play_count']}次</p></div>""",
                    unsafe_allow_html=True)
                st.markdown("---")
            user_style_stat['duration_min'] = user_style_stat['total_play_dur'] / 60
            user_style_stat['percent'] = (user_style_stat['total_play_dur'] / user_style_stat[
                'total_play_dur'].sum() * 100).round(1).astype(str) + '%'
            pie_fig = px.pie(user_style_stat, values='total_play_dur', names='song_style',
                             title=f'{current_user}的曲风播放时长占比',
                             hover_data=['duration_min', 'play_count', 'percent'],
                             labels={'duration_min': '总时长(分钟)'})
            pie_fig.update_traces(textposition='inside', textinfo='percent+label');
            pie_fig.update_layout(height=400)
            st.plotly_chart(pie_fig, use_container_width=True)

            st.subheader("🌳 曲风-歌曲播放时长层级（树状图）")
            song_style_tree_sql = f"""SELECT ms.song_style,ms.song_name,ps.total_play_dur FROM play_stat_song ps JOIN music_song ms ON ps.song_id=ms.song_id WHERE ps.user_id='{current_user}' ORDER BY ps.total_play_dur DESC;"""
            song_style_tree = get_db_data(song_style_tree_sql)
            if not song_style_tree.empty:
                song_style_tree['duration_min'] = song_style_tree['total_play_dur'] / 60
                tree_fig = px.sunburst(song_style_tree, path=['song_style', 'song_name'], values='total_play_dur',
                                       title=f'{current_user}的曲风-歌曲播放时长层级', hover_data=['duration_min'])
                tree_fig.update_layout(height=500);
                st.plotly_chart(tree_fig, use_container_width=True)
            else:
                st.info("暂无曲风-歌曲的详细数据！")
        else:
            st.write("暂无曲风播放记录！")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
        st.subheader("最近播放的10首歌曲")
        play_history_sql = f"""SELECT upr.play_time, ms.song_name, upr.play_dur FROM user_play_record upr JOIN music_song ms ON upr.song_id=ms.song_id WHERE upr.user_id='{current_user}' ORDER BY upr.play_time DESC LIMIT 10;"""
        play_history = get_db_data(play_history_sql)
        if not play_history.empty:
            play_history['cover_url'] = DEFAULT_COVER
            for _, row in play_history.iterrows():
                play_time = row['play_time'].strftime("%Y-%m-%d %H:%M:%S") if pd.notna(row['play_time']) else "未知时间"
                play_dur = round(row['play_dur'] / 60, 1)
                col_img, col_info = st.columns([1, 5])
                with col_img: st.image(row['cover_url'], width=60)
                with col_info: st.write(f"**{row['song_name']}**");st.caption(
                    f"播放时间：{play_time} | 时长：{play_dur}分钟")
                st.markdown("---")
        else:
            st.write("暂无播放历史记录！")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab4:
        st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
        st.subheader("💖 我的听歌偏好分析 + 猜你爱听")
        style_pre_sql = f"""SELECT song_style, style_hot FROM play_stat_style WHERE user_id='{current_user}';"""
        style_pre_data = get_db_data(style_pre_sql)

        # ✅ 偏好曲风热度占比柱状图
        if not style_pre_data.empty:
            # 计算百分比+排序
            style_pre_data['weight'] = (style_pre_data['style_hot'] / style_pre_data['style_hot'].sum() * 100).round(1)
            style_pre_data = style_pre_data.sort_values('weight', ascending=True)
            # 绘制横向柱状图
            bar_fig = px.bar(
                style_pre_data,
                x='weight',
                y='song_style',
                title='🎯 你的偏好曲风热度占比排行',
                labels={'weight': '偏好占比(%)', 'song_style': '曲风'},
                color='song_style',
                color_discrete_sequence=color_list,
                text='weight',
                height=300
            )
            # 柱状图美化
            bar_fig.update_traces(texttemplate='%{text}%', textposition='outside',
                                  hovertemplate='曲风：%{y}<br>偏好占比：%{x}%')
            bar_fig.update_layout(
                title_font={'size': 15, 'color': '#5a389e'},
                xaxis_title='偏好占比 (%)',
                yaxis_title='曲风类型',
                showlegend=False,
                plot_bgcolor='rgba(255,255,255,0.9)',
                margin=dict(l=10, r=10, t=40, b=20)
            )
            st.plotly_chart(bar_fig, use_container_width=True)
            st.markdown("---")

            # 偏好曲风标签展示
            st.markdown("<p style='font-size:16px; color:#2d3748'>你的高偏好曲风：</p>", unsafe_allow_html=True)
            style_tags = ""
            for _, row in style_pre_data.sort_values('weight', ascending=False).head(3).iterrows():
                style_tags += f"<span class='style-tag'>{row['song_style']} ({row['weight']}%)</span>"
            st.markdown(style_tags, unsafe_allow_html=True)
        else:
            st.info("暂无听歌偏好数据，将为你推荐全平台热门曲风～")
            st.markdown(
                """<span class='style-tag'>pop (60%)</span><span class='style-tag'>R&B (30%)</span><span class='style-tag'>摇滚 (10%)</span>""",
                unsafe_allow_html=True)

        # 猜你爱听推荐歌曲模块 - 真实热度排序
        st.markdown("---")
        st.subheader("🎵 为你精准推荐歌曲")
        if not style_pre_data.empty:
            top_style = style_pre_data.iloc[0]['song_style'] if len(style_pre_data) >= 1 else "pop"
            second_style = style_pre_data.iloc[1]['song_style'] if len(style_pre_data) >= 2 else "R&B"
        else:
            top_style = "pop"
            second_style = "R&B"

        heard_songs_sql = f"""SELECT DISTINCT song_id FROM user_play_record WHERE user_id='{current_user}';"""
        heard_songs = get_db_data(heard_songs_sql)
        heard_song_ids = tuple(heard_songs['song_id'].tolist()) if not heard_songs.empty else ('-1',)

        rec1_sql = f"""SELECT ms.song_id, ms.song_name, si.singer_name FROM music_song ms JOIN singer_info si ON ms.singer_id=si.singer_id WHERE ms.song_style='{top_style}' AND ms.song_id NOT IN {heard_song_ids};"""
        rec1 = get_db_data(rec1_sql)
        if not rec1.empty:
            rec1['hot_score'] = rec1['song_id'].apply(calculate_real_hot_score)
            rec1 = rec1.sort_values('hot_score', ascending=False).head(6)
        if len(rec1) < 6:
            supplement1_sql = f"""SELECT ms.song_id, ms.song_name, si.singer_name FROM music_song ms JOIN singer_info si ON ms.singer_id=si.singer_id WHERE ms.song_style='{top_style}' ORDER BY ms.song_id LIMIT {6 - len(rec1)};"""
            supplement1 = get_db_data(supplement1_sql)
            supplement1['hot_score'] = supplement1['song_id'].apply(calculate_real_hot_score)
            rec1 = pd.concat([rec1, supplement1], ignore_index=True)

        rec2_sql = f"""SELECT ms.song_id, ms.song_name, si.singer_name FROM music_song ms JOIN singer_info si ON ms.singer_id=si.singer_id WHERE ms.song_style='{second_style}' AND ms.song_id NOT IN {heard_song_ids};"""
        rec2 = get_db_data(rec2_sql)
        if not rec2.empty:
            rec2['hot_score'] = rec2['song_id'].apply(calculate_real_hot_score)
            rec2 = rec2.sort_values('hot_score', ascending=False).head(4)
        if len(rec2) < 4:
            supplement2_sql = f"""SELECT ms.song_id, ms.song_name, si.singer_name FROM music_song ms JOIN singer_info si ON ms.singer_id=si.singer_id WHERE ms.song_style='{second_style}' ORDER BY ms.song_id LIMIT {4 - len(rec2)};"""
            supplement2 = get_db_data(supplement2_sql)
            supplement2['hot_score'] = supplement2['song_id'].apply(calculate_real_hot_score)
            rec2 = pd.concat([rec2, supplement2], ignore_index=True)

        recommend_songs = pd.concat([rec1, rec2], ignore_index=True).sample(frac=1).reset_index(
            drop=True) if not rec1.empty else pd.DataFrame()
        if not recommend_songs.empty:
            recommend_songs['cover_url'] = DEFAULT_COVER
            cols = st.columns(5)
            for idx, (_, row) in enumerate(recommend_songs.iterrows(), 1):
                with cols[idx % 5]:
                    st.markdown(f"<div class='hot-song-card'>", unsafe_allow_html=True)
                    st.image(row['cover_url'], width=90)
                    st.markdown(f"<h3 style='font-size:13px;'>{row['song_name']}</h3>", unsafe_allow_html=True)
                    st.caption(f"歌手：{row['singer_name']}")
                    st.caption(f"热度：{row['hot_score']}")
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.write("暂无推荐歌曲数据～")
        st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("退出登录", use_container_width=True, key="user_logout_btn"):
            user_logout()
    with col2:
        if st.button("返回首页", use_container_width=True, key="user_home_btn"):
            switch_page("home")


st.markdown("</div>", unsafe_allow_html=True)
