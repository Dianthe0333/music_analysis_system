from hdfs import InsecureClient
import os

# ==================== 核心配置 ====================
UBUNTU_IP = "192.168.222.128"
HDFS_PORT = 50070
HDFS_USER = "tang0333"
LOCAL_CSV_PATH = "/music_project/data/music_log.csv"
HDFS_TARGET_PATH = "/music_log/raw/music_log.csv"

# ==================== 连接HDFS并上传 ====================
try:
    # 1. 连接Ubuntu的HDFS
    client = InsecureClient(f"http://{UBUNTU_IP}:{HDFS_PORT}", user=HDFS_USER)

    # 2. 检查本地文件是否存在
    if not os.path.exists(LOCAL_CSV_PATH):
        raise FileNotFoundError(f"本地文件不存在：{LOCAL_CSV_PATH}")

    # 3. 创建HDFS目录（如果不存在）
    hdfs_dir = os.path.dirname(HDFS_TARGET_PATH)
    if not client.status(hdfs_dir, strict=False):
        client.makedirs(hdfs_dir)
        print(f"创建HDFS目录：{hdfs_dir}")

    # 4. 上传文件到HDFS
    client.upload(HDFS_TARGET_PATH, LOCAL_CSV_PATH, overwrite=True)
    print(f"✅ 文件上传成功！HDFS路径：{HDFS_TARGET_PATH}")

    # 5. 验证：列出HDFS目标目录的文件
    files = client.list(hdfs_dir)
    print(f"📂 HDFS目录文件列表：{files}")

except Exception as e:
    print(f"❌ 上传失败：{str(e)}")
    print("提示：请检查Ubuntu的HDFS是否启动、IP是否正确、50070端口是否放行")