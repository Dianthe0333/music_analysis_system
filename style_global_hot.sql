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

 Date: 27/12/2025 17:07:19
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for style_global_hot
-- ----------------------------
DROP TABLE IF EXISTS `style_global_hot`;
CREATE TABLE `style_global_hot`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `song_style` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '曲风名称',
  `total_style_hot` int NULL DEFAULT 0 COMMENT '全平台该曲风总热度',
  `play_user_count` int NULL DEFAULT 0 COMMENT '听过该曲风的用户数',
  `avg_user_hot` decimal(5, 1) NULL DEFAULT 0.0 COMMENT '平均用户偏好热度',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_style`(`song_style` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '全平台曲风热度统计表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of style_global_hot
-- ----------------------------
INSERT INTO `style_global_hot` VALUES (1, 'classical', 2148, 31, 69.3, '2025-12-26 20:29:32');
INSERT INTO `style_global_hot` VALUES (2, 'jazz', 8424, 60, 140.4, '2025-12-26 20:29:32');
INSERT INTO `style_global_hot` VALUES (3, 'pop', 65917, 100, 659.2, '2025-12-26 20:29:32');
INSERT INTO `style_global_hot` VALUES (4, 'r&b', 2763, 39, 70.8, '2025-12-26 20:29:32');
INSERT INTO `style_global_hot` VALUES (5, 'rock', 66820, 100, 668.2, '2025-12-26 20:29:32');

SET FOREIGN_KEY_CHECKS = 1;
