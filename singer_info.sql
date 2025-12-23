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

 Date: 23/12/2025 21:18:13
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

-- ----------------------------
-- Records of singer_info
-- ----------------------------
INSERT INTO `singer_info` VALUES (1, 'G001', 'Adele', 'A', 'pop');
INSERT INTO `singer_info` VALUES (2, 'G002', 'Avicii', 'A', 'pop');
INSERT INTO `singer_info` VALUES (3, 'G003', '方大同', 'F', 'R&B');
INSERT INTO `singer_info` VALUES (4, 'G004', '王菲', 'F', 'pop');
INSERT INTO `singer_info` VALUES (5, 'G005', 'Keshi', 'K', 'R&B');
INSERT INTO `singer_info` VALUES (6, 'G006', 'Katy Perry', 'K', 'pop');
INSERT INTO `singer_info` VALUES (7, 'G007', '陶喆', 'T', 'R&B');
INSERT INTO `singer_info` VALUES (8, 'G008', 'Taylor Swift', 'T', 'pop');
INSERT INTO `singer_info` VALUES (9, 'G009', 'Maroon5', 'M', 'pop');
INSERT INTO `singer_info` VALUES (10, 'G010', 'Mozart', 'M', 'classical');
INSERT INTO `singer_info` VALUES (11, 'G011', 'Queen', 'Q', 'rock');
INSERT INTO `singer_info` VALUES (12, 'G012', 'Ella Fitzgerald', 'E', 'jazz');
INSERT INTO `singer_info` VALUES (13, 'G013', 'Beethoven', 'B', 'classical');
INSERT INTO `singer_info` VALUES (14, 'G014', 'Louis Armstrong', 'L', 'jazz');
INSERT INTO `singer_info` VALUES (15, 'G015', 'AC/DC', 'A', 'rock');

SET FOREIGN_KEY_CHECKS = 1;
