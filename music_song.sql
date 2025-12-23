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

 Date: 23/12/2025 21:29:15
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for music_song
-- ----------------------------
DROP TABLE IF EXISTS `music_song`;
CREATE TABLE `music_song`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `song_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '歌曲ID',
  `song_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '歌曲名',
  `singer_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联歌手ID',
  `song_style` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '曲风（rock/pop/classical/R&B/jazz）',
  `cover_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '歌曲封面链接',
  `hot_score` int NULL DEFAULT 0 COMMENT '歌曲热度值',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `song_id`(`song_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 22 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '歌曲信息表' ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
