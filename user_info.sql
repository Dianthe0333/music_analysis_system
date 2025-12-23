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

 Date: 23/12/2025 21:17:51
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

-- ----------------------------
-- Records of user_info
-- ----------------------------
INSERT INTO `user_info` VALUES (1, 'U001', 'U001', '用户001');
INSERT INTO `user_info` VALUES (2, 'U002', 'U002', '用户002');
INSERT INTO `user_info` VALUES (3, 'U003', 'U003', '用户003');
INSERT INTO `user_info` VALUES (4, 'U004', 'U004', '用户004');
INSERT INTO `user_info` VALUES (5, 'U005', 'U005', '用户005');
INSERT INTO `user_info` VALUES (6, 'U006', 'U006', '用户006');
INSERT INTO `user_info` VALUES (7, 'U007', 'U007', '用户007');
INSERT INTO `user_info` VALUES (8, 'U008', 'U008', '用户008');
INSERT INTO `user_info` VALUES (9, 'U009', 'U009', '用户009');
INSERT INTO `user_info` VALUES (10, 'U010', 'U010', '用户010');
INSERT INTO `user_info` VALUES (11, 'U011', 'U011', '用户011');
INSERT INTO `user_info` VALUES (12, 'U012', 'U012', '用户012');
INSERT INTO `user_info` VALUES (13, 'U013', 'U013', '用户013');
INSERT INTO `user_info` VALUES (14, 'U014', 'U014', '用户014');
INSERT INTO `user_info` VALUES (15, 'U015', 'U015', '用户015');
INSERT INTO `user_info` VALUES (16, 'U016', 'U016', '用户016');
INSERT INTO `user_info` VALUES (17, 'U017', 'U017', '用户017');
INSERT INTO `user_info` VALUES (18, 'U018', 'U018', '用户018');
INSERT INTO `user_info` VALUES (19, 'U019', 'U019', '用户019');
INSERT INTO `user_info` VALUES (20, 'U020', 'U020', '用户020');
INSERT INTO `user_info` VALUES (21, 'U021', 'U021', '用户021');
INSERT INTO `user_info` VALUES (22, 'U022', 'U022', '用户022');
INSERT INTO `user_info` VALUES (23, 'U023', 'U023', '用户023');
INSERT INTO `user_info` VALUES (24, 'U024', 'U024', '用户024');
INSERT INTO `user_info` VALUES (25, 'U025', 'U025', '用户025');
INSERT INTO `user_info` VALUES (26, 'U026', 'U026', '用户026');
INSERT INTO `user_info` VALUES (27, 'U027', 'U027', '用户027');
INSERT INTO `user_info` VALUES (28, 'U028', 'U028', '用户028');
INSERT INTO `user_info` VALUES (29, 'U029', 'U029', '用户029');
INSERT INTO `user_info` VALUES (30, 'U030', 'U030', '用户030');
INSERT INTO `user_info` VALUES (31, 'U031', 'U031', '用户031');
INSERT INTO `user_info` VALUES (32, 'U032', 'U032', '用户032');
INSERT INTO `user_info` VALUES (33, 'U033', 'U033', '用户033');
INSERT INTO `user_info` VALUES (34, 'U034', 'U034', '用户034');
INSERT INTO `user_info` VALUES (35, 'U035', 'U035', '用户035');
INSERT INTO `user_info` VALUES (36, 'U036', 'U036', '用户036');
INSERT INTO `user_info` VALUES (37, 'U037', 'U037', '用户037');
INSERT INTO `user_info` VALUES (38, 'U038', 'U038', '用户038');
INSERT INTO `user_info` VALUES (39, 'U039', 'U039', '用户039');
INSERT INTO `user_info` VALUES (40, 'U040', 'U040', '用户040');
INSERT INTO `user_info` VALUES (41, 'U041', 'U041', '用户041');
INSERT INTO `user_info` VALUES (42, 'U042', 'U042', '用户042');
INSERT INTO `user_info` VALUES (43, 'U043', 'U043', '用户043');
INSERT INTO `user_info` VALUES (44, 'U044', 'U044', '用户044');
INSERT INTO `user_info` VALUES (45, 'U045', 'U045', '用户045');
INSERT INTO `user_info` VALUES (46, 'U046', 'U046', '用户046');
INSERT INTO `user_info` VALUES (47, 'U047', 'U047', '用户047');
INSERT INTO `user_info` VALUES (48, 'U048', 'U048', '用户048');
INSERT INTO `user_info` VALUES (49, 'U049', 'U049', '用户049');
INSERT INTO `user_info` VALUES (50, 'U050', 'U050', '用户050');
INSERT INTO `user_info` VALUES (51, 'U051', 'U051', '用户051');
INSERT INTO `user_info` VALUES (52, 'U052', 'U052', '用户052');
INSERT INTO `user_info` VALUES (53, 'U053', 'U053', '用户053');
INSERT INTO `user_info` VALUES (54, 'U054', 'U054', '用户054');
INSERT INTO `user_info` VALUES (55, 'U055', 'U055', '用户055');
INSERT INTO `user_info` VALUES (56, 'U056', 'U056', '用户056');
INSERT INTO `user_info` VALUES (57, 'U057', 'U057', '用户057');
INSERT INTO `user_info` VALUES (58, 'U058', 'U058', '用户058');
INSERT INTO `user_info` VALUES (59, 'U059', 'U059', '用户059');
INSERT INTO `user_info` VALUES (60, 'U060', 'U060', '用户060');
INSERT INTO `user_info` VALUES (61, 'U061', 'U061', '用户061');
INSERT INTO `user_info` VALUES (62, 'U062', 'U062', '用户062');
INSERT INTO `user_info` VALUES (63, 'U063', 'U063', '用户063');
INSERT INTO `user_info` VALUES (64, 'U064', 'U064', '用户064');
INSERT INTO `user_info` VALUES (65, 'U065', 'U065', '用户065');
INSERT INTO `user_info` VALUES (66, 'U066', 'U066', '用户066');
INSERT INTO `user_info` VALUES (67, 'U067', 'U067', '用户067');
INSERT INTO `user_info` VALUES (68, 'U068', 'U068', '用户068');
INSERT INTO `user_info` VALUES (69, 'U069', 'U069', '用户069');
INSERT INTO `user_info` VALUES (70, 'U070', 'U070', '用户070');
INSERT INTO `user_info` VALUES (71, 'U071', 'U071', '用户071');
INSERT INTO `user_info` VALUES (72, 'U072', 'U072', '用户072');
INSERT INTO `user_info` VALUES (73, 'U073', 'U073', '用户073');
INSERT INTO `user_info` VALUES (74, 'U074', 'U074', '用户074');
INSERT INTO `user_info` VALUES (75, 'U075', 'U075', '用户075');
INSERT INTO `user_info` VALUES (76, 'U076', 'U076', '用户076');
INSERT INTO `user_info` VALUES (77, 'U077', 'U077', '用户077');
INSERT INTO `user_info` VALUES (78, 'U078', 'U078', '用户078');
INSERT INTO `user_info` VALUES (79, 'U079', 'U079', '用户079');
INSERT INTO `user_info` VALUES (80, 'U080', 'U080', '用户080');
INSERT INTO `user_info` VALUES (81, 'U081', 'U081', '用户081');
INSERT INTO `user_info` VALUES (82, 'U082', 'U082', '用户082');
INSERT INTO `user_info` VALUES (83, 'U083', 'U083', '用户083');
INSERT INTO `user_info` VALUES (84, 'U084', 'U084', '用户084');
INSERT INTO `user_info` VALUES (85, 'U085', 'U085', '用户085');
INSERT INTO `user_info` VALUES (86, 'U086', 'U086', '用户086');
INSERT INTO `user_info` VALUES (87, 'U087', 'U087', '用户087');
INSERT INTO `user_info` VALUES (88, 'U088', 'U088', '用户088');
INSERT INTO `user_info` VALUES (89, 'U089', 'U089', '用户089');
INSERT INTO `user_info` VALUES (90, 'U090', 'U090', '用户090');
INSERT INTO `user_info` VALUES (91, 'U091', 'U091', '用户091');
INSERT INTO `user_info` VALUES (92, 'U092', 'U092', '用户092');
INSERT INTO `user_info` VALUES (93, 'U093', 'U093', '用户093');
INSERT INTO `user_info` VALUES (94, 'U094', 'U094', '用户094');
INSERT INTO `user_info` VALUES (95, 'U095', 'U095', '用户095');
INSERT INTO `user_info` VALUES (96, 'U096', 'U096', '用户096');
INSERT INTO `user_info` VALUES (97, 'U097', 'U097', '用户097');
INSERT INTO `user_info` VALUES (98, 'U098', 'U098', '用户098');
INSERT INTO `user_info` VALUES (99, 'U099', 'U099', '用户099');
INSERT INTO `user_info` VALUES (100, 'U100', 'U100', '用户100');

SET FOREIGN_KEY_CHECKS = 1;
