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

 Date: 23/12/2025 21:18:46
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

-- ----------------------------
-- Records of music_song
-- ----------------------------
INSERT INTO `music_song` VALUES (1, 'S001', 'Rolling in the Deep', 'G001', 'pop', 'D:/PyCharmMiscProject/music_project/data/song_covers/S001.png', 998, '2025-12-19 18:18:06');
INSERT INTO `music_song` VALUES (2, 'S002', 'Shake It Off', 'G008', 'pop', 'D:/PyCharmMiscProject/music_project/data/song_covers/S002.png', 997, '2025-12-19 18:18:06');
INSERT INTO `music_song` VALUES (3, 'S003', 'Sugar', 'G009', 'pop', 'D:/PyCharmMiscProject/music_project/data/song_covers/S003.png', 996, '2025-12-19 18:18:06');
INSERT INTO `music_song` VALUES (4, 'S004', 'Bohemian Rhapsody', 'G011', 'rock', 'D:/PyCharmMiscProject/music_project/data/song_covers/S004.png', 888, '2025-12-19 18:18:06');
INSERT INTO `music_song` VALUES (5, 'S005', 'Highway to Hell', 'G015', 'rock', 'D:/PyCharmMiscProject/music_project/data/song_covers/S005.png', 887, '2025-12-19 18:18:06');
INSERT INTO `music_song` VALUES (6, 'S006', 'Symphony No. 40', 'G010', 'classical', 'D:/PyCharmMiscProject/music_project/data/song_covers/S006.png', 777, '2025-12-19 18:18:06');
INSERT INTO `music_song` VALUES (7, 'S007', 'Moonlight Sonata', 'G013', 'classical', 'D:/PyCharmMiscProject/music_project/data/song_covers/S007.png', 776, '2025-12-19 18:18:06');
INSERT INTO `music_song` VALUES (8, 'S008', '爱爱爱', 'G003', 'R&B', 'D:/PyCharmMiscProject/music_project/data/song_covers/S008.png', 666, '2025-12-19 18:18:06');
INSERT INTO `music_song` VALUES (9, 'S009', '爱很简单', 'G007', 'R&B', 'D:/PyCharmMiscProject/music_project/data/song_covers/S009.png', 665, '2025-12-19 18:18:06');
INSERT INTO `music_song` VALUES (10, 'S010', 'Drunk', 'G005', 'R&B', 'D:/PyCharmMiscProject/music_project/data/song_covers/S010.png', 664, '2025-12-19 18:18:06');
INSERT INTO `music_song` VALUES (11, 'S011', 'Fly Me to the Moon', 'G012', 'jazz', 'D:/PyCharmMiscProject/music_project/data/song_covers/S011.png', 555, '2025-12-19 18:18:06');
INSERT INTO `music_song` VALUES (12, 'S012', 'What a Wonderful World', 'G014', 'jazz', 'D:/PyCharmMiscProject/music_project/data/song_covers/S012.png', 554, '2025-12-19 18:18:06');
INSERT INTO `music_song` VALUES (13, 'S013', 'Hello', 'G001', 'pop', 'D:/PyCharmMiscProject/music_project/data/song_covers/S013.png', 995, '2025-12-19 18:18:06');
INSERT INTO `music_song` VALUES (14, 'S014', 'We Will Rock You', 'G011', 'rock', 'D:/PyCharmMiscProject/music_project/data/song_covers/S014.png', 886, '2025-12-19 18:18:06');
INSERT INTO `music_song` VALUES (15, 'S015', 'Canon', 'G010', 'classical', 'D:/PyCharmMiscProject/music_project/data/song_covers/S015.png', 775, '2025-12-19 18:18:06');
INSERT INTO `music_song` VALUES (16, 'S016', '春风吹', 'G003', 'R&B', 'D:/PyCharmMiscProject/music_project/data/song_covers/S016.png', 663, '2025-12-19 18:18:06');
INSERT INTO `music_song` VALUES (17, 'S017', 'Lazy Song', 'G009', 'pop', 'D:/PyCharmMiscProject/music_project/data/song_covers/S017.png', 994, '2025-12-19 18:18:06');
INSERT INTO `music_song` VALUES (18, 'S018', 'Back in Black', 'G015', 'rock', 'D:/PyCharmMiscProject/music_project/data/song_covers/S018.png', 885, '2025-12-19 18:18:06');
INSERT INTO `music_song` VALUES (19, 'S019', 'Yesterday', 'G012', 'jazz', 'D:/PyCharmMiscProject/music_project/data/song_covers/S019.png', 553, '2025-12-19 18:18:06');
INSERT INTO `music_song` VALUES (20, 'S020', '普通朋友', 'G007', 'R&B', 'D:/PyCharmMiscProject/music_project/data/song_covers/S020.png', 662, '2025-12-19 18:18:06');
INSERT INTO `music_song` VALUES (21, 'S021', '致青春', 'G004', 'pop', 'D:/PyCharmMiscProject/music_project/data/song_covers/S021.png', 999, '2025-12-23 09:55:19');

SET FOREIGN_KEY_CHECKS = 1;
