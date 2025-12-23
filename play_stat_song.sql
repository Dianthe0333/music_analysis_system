/*
 Navicat Premium Dump SQL

 Source Server         : music_analysis
 Source Server Type    : MySQL
 Source Server Version : 80044 (8.0.44-0ubuntu0.24.04.2)
 Source Host           : 192.168.222.128:3306
 Source Schema         : music_analysis

 Target Server Type    : MySQL
 Target Server Version : 80044 (8.0.44-0ubuntu0.24.04.2)
 File Encoding         : 65001

 Date: 23/12/2025 21:29:20
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for play_stat_song
-- ----------------------------
DROP TABLE IF EXISTS `play_stat_song`;
CREATE TABLE `play_stat_song`  (
  `stat_song_id` int NOT NULL AUTO_INCREMENT COMMENT '统计记录ID',
  `user_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户ID（NULL表示全局统计）',
  `song_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '歌曲ID',
  `total_play_dur` bigint NOT NULL DEFAULT 0 COMMENT '总播放时长（秒）',
  `play_count` int NOT NULL DEFAULT 0 COMMENT '播放次数',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`stat_song_id`) USING BTREE,
  UNIQUE INDEX `uk_user_song`(`user_id` ASC, `song_id` ASC) USING BTREE,
  INDEX `idx_song_id`(`song_id` ASC) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4065 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '歌曲播放统计表（全局+用户）' ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
