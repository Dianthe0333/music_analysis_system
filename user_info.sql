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

 Date: 23/12/2025 21:29:41
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user_info
-- ----------------------------
DROP TABLE IF EXISTS `user_info`;
CREATE TABLE `user_info`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户账号',
  `password` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户密码',
  `user_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户名',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 101 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户信息表' ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
