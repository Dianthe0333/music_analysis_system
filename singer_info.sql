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

 Date: 23/12/2025 21:29:33
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for singer_info
-- ----------------------------
DROP TABLE IF EXISTS `singer_info`;
CREATE TABLE `singer_info`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `singer_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '歌手ID',
  `singer_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '歌手名',
  `initial` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '首字母（A-Z）',
  `song_style` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '代表曲风',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `singer_id`(`singer_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '歌手信息表' ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
