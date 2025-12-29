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

 Date: 29/12/2025 17:42:34
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user_play_record
-- ----------------------------
DROP TABLE IF EXISTS `user_play_record`;
CREATE TABLE `user_play_record`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联用户ID',
  `song_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联歌曲ID',
  `play_time` datetime NOT NULL COMMENT '播放时间',
  `play_dur` int NOT NULL COMMENT '播放时长（秒）',
  `source` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'app',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1501 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户播放记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Triggers structure for table user_play_record
-- ----------------------------
DROP TRIGGER IF EXISTS `trg_upr_after_insert`;
delimiter ;;
CREATE TRIGGER `trg_upr_after_insert` AFTER INSERT ON `user_play_record` FOR EACH ROW BEGIN
    -- 1. 更新用户-歌曲统计
    INSERT INTO play_stat_song (user_id, song_id, total_play_dur, play_count)
    VALUES (NEW.user_id, NEW.song_id, NEW.play_dur, 1)
    ON DUPLICATE KEY UPDATE
        total_play_dur = total_play_dur + NEW.play_dur,
        play_count = play_count + 1;
    
    -- 2. 更新全局歌曲统计
    INSERT INTO play_stat_song (user_id, song_id, total_play_dur, play_count)
    VALUES (NULL, NEW.song_id, NEW.play_dur, 1)
    ON DUPLICATE KEY UPDATE
        total_play_dur = total_play_dur + NEW.play_dur,
        play_count = play_count + 1;
    
    -- 3. 获取歌曲对应的曲风
    SELECT song_style INTO @style FROM music_song WHERE song_id = NEW.song_id;
    
    -- 4. 更新用户-曲风统计
    INSERT INTO play_stat_style (user_id, song_style, total_play_dur, play_count)
    VALUES (NEW.user_id, @style, NEW.play_dur, 1)
    ON DUPLICATE KEY UPDATE
        total_play_dur = total_play_dur + NEW.play_dur,
        play_count = play_count + 1;
    
    -- 5. 更新全局曲风统计
    INSERT INTO play_stat_style (user_id, song_style, total_play_dur, play_count)
    VALUES (NULL, @style, NEW.play_dur, 1)
    ON DUPLICATE KEY UPDATE
        total_play_dur = total_play_dur + NEW.play_dur,
        play_count = play_count + 1;
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
