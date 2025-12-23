## music_analysis_system音乐播放器听歌行为分析系统
大数据处理课程设计项目，基于Python+Streamlit+MySQL搭建的音乐听歌行为分析系统，覆盖数据生成、清洗、分析、可视化全流程。

## 技术栈
- 开发语言：Python3.8
- 前端/框架：Streamlit、Plotly
- 数据库：MySQL8.0
- 操作系统：Windows10、Ubuntu20.04

## 核心功能
1. 模拟生成用户播放日志数据并同步至MySQL；
2. 数据清洗与标准化，过滤脏数据；
3. 多维度用户听歌行为分析（时段、曲风偏好、歌曲热度）；
4. 交互式数据可视化展示。

## 运行说明
1. 安装依赖：'pip install streamlit pymysql pandas plotly paramiko'；
2. 配置MySQL连接信息；
3. 运行'generate.py'生成数据，运行'visualization1.py'启动可视化页面。
