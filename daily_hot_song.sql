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

 Date: 23/12/2025 21:18:53
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for daily_hot_song
-- ----------------------------
DROP TABLE IF EXISTS `daily_hot_song`;
CREATE TABLE `daily_hot_song`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `date` date NOT NULL COMMENT '日期',
  `song_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联歌曲ID',
  `rank_num` int NOT NULL COMMENT '当日排名',
  `hot_score` int NULL DEFAULT 0 COMMENT '当日热度',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_date_song`(`date` ASC, `song_id` ASC) USING BTREE COMMENT '日期+歌曲唯一索引'
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '每日热门歌曲表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of daily_hot_song
-- ----------------------------
INSERT INTO `daily_hot_song` VALUES (1, '2025-12-19', 'S001', 1, 998);
INSERT INTO `daily_hot_song` VALUES (2, '2025-12-19', 'S004', 2, 888);
INSERT INTO `daily_hot_song` VALUES (3, '2025-12-19', 'S006', 3, 777);
INSERT INTO `daily_hot_song` VALUES (4, '2025-12-19', 'S008', 4, 666);
INSERT INTO `daily_hot_song` VALUES (5, '2025-12-19', 'S011', 5, 555);

SET FOREIGN_KEY_CHECKS = 1;
