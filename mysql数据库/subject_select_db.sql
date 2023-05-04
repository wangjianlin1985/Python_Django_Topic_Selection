/*
 Navicat Premium Data Transfer

 Source Server         : mysql5.6_20210415
 Source Server Type    : MySQL
 Source Server Version : 50620
 Source Host           : localhost:3306
 Source Schema         : subject_select_db

 Target Server Type    : MySQL
 Target Server Version : 50620
 File Encoding         : 65001

 Date: 27/04/2021 14:57:13
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_admin
-- ----------------------------
DROP TABLE IF EXISTS `t_admin`;
CREATE TABLE `t_admin`  (
  `username` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `password` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`username`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_admin
-- ----------------------------
INSERT INTO `t_admin` VALUES ('a', 'a');

-- ----------------------------
-- Table structure for t_classinfo
-- ----------------------------
DROP TABLE IF EXISTS `t_classinfo`;
CREATE TABLE `t_classinfo`  (
  `classNumber` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'classNumber',
  `specialName` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '所在专业',
  `className` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '班级名称',
  `startDate` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '成立日期',
  `headTeacher` varchar(12) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '班主任',
  PRIMARY KEY (`classNumber`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_classinfo
-- ----------------------------
INSERT INTO `t_classinfo` VALUES ('BJ001', '计算机科学与技术', '计科系21级3班', '2021-04-06', '王晓婷');
INSERT INTO `t_classinfo` VALUES ('BJ002', '计算机科学与技术', '计科系21级4班', '2021-04-14', '张笑天');

-- ----------------------------
-- Table structure for t_leaveword
-- ----------------------------
DROP TABLE IF EXISTS `t_leaveword`;
CREATE TABLE `t_leaveword`  (
  `leaveWordId` int(11) NOT NULL AUTO_INCREMENT COMMENT '留言id',
  `leaveTitle` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '留言标题',
  `leaveContent` varchar(2000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '留言内容',
  `userObj` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '留言人',
  `leaveTime` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '留言时间',
  `replyContent` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '管理回复',
  `replyTime` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '回复时间',
  PRIMARY KEY (`leaveWordId`) USING BTREE,
  INDEX `userObj`(`userObj`) USING BTREE,
  CONSTRAINT `t_leaveword_ibfk_1` FOREIGN KEY (`userObj`) REFERENCES `t_userinfo` (`user_name`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_leaveword
-- ----------------------------
INSERT INTO `t_leaveword` VALUES (1, '多开题目吧', '我感觉目前系统的题目太少，可以多搞点！', 'STU001', '2021-04-26 20:10:12', '收到你的请求！', '2021-04-26 20:10:16');
INSERT INTO `t_leaveword` VALUES (2, '我选的题目不想做了！', '我该怎么办呢，突然发现太难了', 'STU001', '2021-04-27 01:39:59', '可以找你的指导老师删除你的选题记录', '2021-04-27 14:46:02');
INSERT INTO `t_leaveword` VALUES (3, 'gafa', 'aga', 'STU002', '2021-04-27 12:23:00', '--', '--');

-- ----------------------------
-- Table structure for t_notice
-- ----------------------------
DROP TABLE IF EXISTS `t_notice`;
CREATE TABLE `t_notice`  (
  `noticeId` int(11) NOT NULL AUTO_INCREMENT COMMENT '公告id',
  `title` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '标题',
  `content` varchar(5000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '公告内容',
  `publishDate` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '发布时间',
  PRIMARY KEY (`noticeId`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_notice
-- ----------------------------
INSERT INTO `t_notice` VALUES (1, '毕业设计选题网站开通了', '<p>同学们以后要选择题目的话来这个平台开始起航吧！</p>', '2021-04-26 20:10:24');
INSERT INTO `t_notice` VALUES (2, '2021年毕业选题截止时间通告', '<p>还没有选题的同学请尽快来选题，3月15日后就不能给你选题了！</p>', '2021-04-27 14:50:44');

-- ----------------------------
-- Table structure for t_selectitem
-- ----------------------------
DROP TABLE IF EXISTS `t_selectitem`;
CREATE TABLE `t_selectitem`  (
  `selectItemId` int(11) NOT NULL AUTO_INCREMENT COMMENT '选题id',
  `subjectObj` int(11) NOT NULL COMMENT '论文题目',
  `teacherObj` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '指导老师',
  `studentObj` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '选题学生',
  `reason` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '选题原因',
  `selectTime` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '选题时间',
  `shenHeState` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '审核状态',
  `shenHeTime` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '审核时间',
  `teacherReply` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '老师回复',
  PRIMARY KEY (`selectItemId`) USING BTREE,
  INDEX `subjectObj`(`subjectObj`) USING BTREE,
  INDEX `teacherObj`(`teacherObj`) USING BTREE,
  INDEX `studentObj`(`studentObj`) USING BTREE,
  CONSTRAINT `t_selectitem_ibfk_1` FOREIGN KEY (`subjectObj`) REFERENCES `t_subject` (`subjectId`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `t_selectitem_ibfk_2` FOREIGN KEY (`teacherObj`) REFERENCES `t_teacher` (`teacherNumber`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `t_selectitem_ibfk_3` FOREIGN KEY (`studentObj`) REFERENCES `t_userinfo` (`user_name`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_selectitem
-- ----------------------------
INSERT INTO `t_selectitem` VALUES (1, 1, 'TH001', 'STU001', '对小程序熟悉', '2021-04-27 01:32:56', '审核通过', '2021-04-27 01:32:59', '可以');
INSERT INTO `t_selectitem` VALUES (2, 2, 'TH001', 'STU001', '想搞算法', '--', '待审核', '--', '--');
INSERT INTO `t_selectitem` VALUES (3, 1, 'TH001', 'STU002', '熟悉小程序', '2021-04-27 02:14:39', '待审核', '--', '--');
INSERT INTO `t_selectitem` VALUES (4, 2, 'TH002', 'STU002', '搞算法', '2021-04-27 12:22:44', '审核通过', '2021-04-27 12:23:36', 'fafasfa');

-- ----------------------------
-- Table structure for t_subject
-- ----------------------------
DROP TABLE IF EXISTS `t_subject`;
CREATE TABLE `t_subject`  (
  `subjectId` int(11) NOT NULL AUTO_INCREMENT COMMENT '题目编号',
  `subjectTypeObj` int(11) NOT NULL COMMENT '题目类型',
  `subjectName` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '题目名称',
  `subjectPhoto` varchar(60) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '题目图片',
  `content` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '题目内容',
  `subjectState` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '题目状态',
  `personNum` int(11) NOT NULL COMMENT '限选人数',
  `teacherObj` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '发布老师',
  `addTime` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '发布时间',
  PRIMARY KEY (`subjectId`) USING BTREE,
  INDEX `subjectTypeObj`(`subjectTypeObj`) USING BTREE,
  INDEX `teacherObj`(`teacherObj`) USING BTREE,
  CONSTRAINT `t_subject_ibfk_1` FOREIGN KEY (`subjectTypeObj`) REFERENCES `t_subjecttype` (`subjectTypeId`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `t_subject_ibfk_2` FOREIGN KEY (`teacherObj`) REFERENCES `t_teacher` (`teacherNumber`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_subject
-- ----------------------------
INSERT INTO `t_subject` VALUES (1, 2, '基于微信小程序图书系统设计', 'img/tushuguanli.jpg', '<p><span style=\"color: #666666; font-family: 宋体, arial; background-color: #fffff0;\">&nbsp; &nbsp;项目一共2个身份，管理员和读者身份。管理员在web端发布管理图书信息，小程序客户端用户打开后可以查询图书信息，查看热门图书信息，看中什么图书后可以去图书馆联系管理借阅图书。管理员办理读者的借阅登记和图书归还操作，客户端用户注册登录后可以查询自己的借阅记录。</span></p>', '可选', 3, 'TH001', '2021-04-26 11:22:41');
INSERT INTO `t_subject` VALUES (2, 1, '基于人脸识别考勤系统设计', 'img/renliankaoqin.jpg', '<p>设计一个安卓app,用于员工上班考勤，通过识别人脸实现考勤自动录入！</p>', '可选', 3, 'TH002', '2021-04-27 11:57:55');
INSERT INTO `t_subject` VALUES (3, 2, '基于Python旅游网站设计', 'img/lvyouwangzhan.jpg', '<p><span style=\"color: #666666; font-family: 宋体, arial; background-color: #fffff0;\">&nbsp; &nbsp;系统一共2个身份，用户和管理员。用户在前端可以根据省份，景区类型，景区名称关键词查询景区信息，景区详情里面一般有景区的联系电话，用户对景区有什么疑问也可以打电话给景区工作人员咨询或者预定门票等，用户注册登录后可以给管理员留言建议，管理到时候可以回复用户的留言;管理员登录网站后台后可以注册用户，发布景区信息，管理景区信息，查看管理用户留言，修改密码等!</span></p>', '可选', 5, 'TH002', '2021-04-27 14:41:14');

-- ----------------------------
-- Table structure for t_subjecttype
-- ----------------------------
DROP TABLE IF EXISTS `t_subjecttype`;
CREATE TABLE `t_subjecttype`  (
  `subjectTypeId` int(11) NOT NULL AUTO_INCREMENT COMMENT '类型编号',
  `subjectTypeName` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '类型名称',
  `subjectTypeDesc` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '类型说明',
  PRIMARY KEY (`subjectTypeId`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_subjecttype
-- ----------------------------
INSERT INTO `t_subjecttype` VALUES (1, '理论算法型', '偏重理论和算法的设计');
INSERT INTO `t_subjecttype` VALUES (2, '社会实践型', '偏向于实践操作类型');

-- ----------------------------
-- Table structure for t_teacher
-- ----------------------------
DROP TABLE IF EXISTS `t_teacher`;
CREATE TABLE `t_teacher`  (
  `teacherNumber` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'teacherNumber',
  `password` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '登录密码',
  `name` varchar(12) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '姓名',
  `sex` varchar(4) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '性别',
  `birthday` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '出生日期',
  `photo` varchar(60) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '教师照片',
  `professName` varchar(12) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '职称',
  `telephone` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '联系电话',
  `address` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '家庭地址',
  `inDate` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '入职日期',
  `introduce` varchar(5000) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '教师简介',
  PRIMARY KEY (`teacherNumber`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_teacher
-- ----------------------------
INSERT INTO `t_teacher` VALUES ('TH001', '123', '李梦婷', '女', '2021-03-31', 'img/2.jpg', '教授', '13508109342', '四川成都崔家店路10号', '2021-04-19', '<p class=\"p0 \" style=\"margin: 0px; padding: 0px; font-family: 微软雅黑; font-size: medium;\"><span style=\"margin: 0px; padding: 0px; font-size: 16px;\"><span style=\"margin: 0px; padding: 0px;\">最终学位：</span><span style=\"margin: 0px; padding: 0px;\">硕士</span></span></p>\r\n<p class=\"p0 \" style=\"margin: 0px; padding: 0px; font-family: 微软雅黑; font-size: medium;\"><span style=\"margin: 0px; padding: 0px;\">毕业学校：沈阳航空航天大学</span></p>\r\n<p class=\"p0 \" style=\"margin: 0px; padding: 0px; font-family: 微软雅黑; font-size: medium;\"><span style=\"margin: 0px; padding: 0px;\">从事专业：计算机应用</span></p>\r\n<p class=\"p0 \" style=\"margin: 0px; padding: 0px; font-family: 微软雅黑; font-size: medium;\"><span style=\"margin: 0px; padding: 0px; font-size: 16px;\"><span style=\"margin: 0px; padding: 0px;\">职&nbsp; &nbsp;务：</span><span style=\"margin: 0px; padding: 0px;\">副院长</span></span></p>\r\n<p class=\"p0 \" style=\"margin: 0px; padding: 0px; font-family: 微软雅黑; font-size: medium;\"><span style=\"margin: 0px; padding: 0px;\">所属院系：计算机学院</span></p>\r\n<p class=\"p0 \" style=\"margin: 0px; padding: 0px; font-family: 微软雅黑; font-size: medium;\"><span style=\"margin: 0px; padding: 0px;\">所属研究室：网络信息安全</span></p>\r\n<p class=\"p0 \" style=\"margin: 0px; padding: 0px; font-family: 微软雅黑; font-size: medium;\"><span style=\"margin: 0px; padding: 0px;\">职 &nbsp; &nbsp; 称：副教授</span></p>\r\n<p class=\"p0 \" style=\"margin: 0px; padding: 0px; font-family: 微软雅黑; font-size: medium;\"><span style=\"margin: 0px; padding: 0px; font-size: 16px;\"><span class=\"15 \" style=\"margin: 0px; padding: 0px;\">E-mail：gafafasf</span><span class=\"15 \" style=\"margin: 0px; padding: 0px;\">@163.com</span></span></p>\r\n<p class=\"p0 \" style=\"margin: 0px; padding: 0px; font-family: 微软雅黑; font-size: medium;\"><span style=\"margin: 0px; padding: 0px;\">简历：</span></p>\r\n<p class=\"p0 \" style=\"margin: 0px; padding: 0px; font-family: 微软雅黑; font-size: medium;\"><span style=\"margin: 0px; padding: 0px;\">1990.9-1993.7 辽宁营口市鲅鱼圈区高级中学，高中学习</span></p>\r\n<p class=\"p0 \" style=\"margin: 0px; padding: 0px; font-family: 微软雅黑; font-size: medium;\"><span style=\"margin: 0px; padding: 0px;\">1993.9-1997.7 沈阳航空航天大学，本科学习</span></p>\r\n<p class=\"p0 \" style=\"margin: 0px; padding: 0px; font-family: 微软雅黑; font-size: medium;\"><span style=\"margin: 0px; padding: 0px;\">1997.7-至今 沈阳航空航天大学计算机学院，教学</span></p>\r\n<p class=\"p0 \" style=\"margin: 0px; padding: 0px; font-family: 微软雅黑; font-size: medium;\"><span style=\"margin: 0px; padding: 0px;\">2002.9-2005.3 东北大学软件工程专业 硕士学习</span></p>\r\n<p class=\"p0 \" style=\"margin: 0px; padding: 0px; font-family: 微软雅黑; font-size: medium;\"><span style=\"margin: 0px; padding: 0px;\">2013.9-至今 东北大学信息学院 博士学习</span></p>\r\n<p><span style=\"margin: 0px; padding: 0px;\">&nbsp;</span></p>');
INSERT INTO `t_teacher` VALUES ('TH002', '123', '王涛', '男', '2021-03-31', 'img/20.jpg', '高级教师', '1350810834', '四川南充', '2021-04-06', '<p>2002年6月毕业于成都理工大学计算机科学与技术专业。2009年6月毕业于山东科技大学计算机应用技术专业。主要讲授大学计算机文化基础、Office 2000、C语言程序设计、SQL Server 2000数据库、Visual Basic程序设计等课程。</p>\r\n<p>主要成果</p>\r\n<p>1.教材或著作</p>\r\n<p>（1）《大学生计算机文化基础》（第二版）（副主编）；</p>\r\n<p>（2）《大学计算机应用基础》（副主编）；</p>\r\n<p>（3）《计算机应用基础项目化教程》（编委）。</p>\r\n<p>2.课题情况</p>\r\n<p>（1）主持校级课题&ldquo;信息化条件下高职计算机基础混合式教学模式研究&rdquo;；</p>\r\n<p>（2）主持校级课题&ldquo;基于应用型人才培养的Excel课程教学研究&rdquo;；</p>\r\n<p>（3）参与省级课题&ldquo;身体社会学视野下的高校体育与学生身体发展研究&rdquo;；</p>\r\n<p>（4）参与省级课题&ldquo;基于学生信息素质培养的民办高校计算机基础教学改革研究&rdquo;；</p>\r\n<p>（5）指导学生参加2018年山东省国家级大学生创新创业训练计划项目&ldquo;互联网+智能灌溉科技&rdquo;。</p>\r\n<p>3.发表论文</p>\r\n<p>（1）2013年09月，《Excel函数在学生成绩数据处理中的应用》发表于《电脑知识与技术》（1/2）；</p>\r\n<p>（2）2013年09月，《基于Excel函数的高校学生成绩表数据处理》发表于《青岛滨海学院学报》（1/2）；</p>\r\n<p>（3）2015年07月，《Two Dimension Threshold Image Segmentation Based on Improved Artificial Fish-Swarm Algorithm》发表于《Advances in Engineering Research》（国际期刊（EI源刊），1/3）（被CPCI-S(原ISTP）收录)；</p>\r\n<p>（4）2016年02月，《基于应用型人才培养的Excel课程教学研究》发表于《电脑知识与技术》（1/1）。</p>');

-- ----------------------------
-- Table structure for t_userinfo
-- ----------------------------
DROP TABLE IF EXISTS `t_userinfo`;
CREATE TABLE `t_userinfo`  (
  `user_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'user_name',
  `password` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '登录密码',
  `classObj` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '所在班级',
  `name` varchar(12) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '姓名',
  `sex` varchar(4) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '性别',
  `birthday` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '出生日期',
  `zzmm` varchar(15) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '政治面貌',
  `telephone` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '联系电话',
  `address` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '家庭地址',
  `photo` varchar(60) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '个人照片',
  PRIMARY KEY (`user_name`) USING BTREE,
  INDEX `classObj`(`classObj`) USING BTREE,
  CONSTRAINT `t_userinfo_ibfk_1` FOREIGN KEY (`classObj`) REFERENCES `t_classinfo` (`classNumber`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_userinfo
-- ----------------------------
INSERT INTO `t_userinfo` VALUES ('STU001', '123', 'BJ001', '李明涛', '男', '2021-03-31', '团员', '13058129342', '四川成都红星路5号', 'img/12.jpg');
INSERT INTO `t_userinfo` VALUES ('STU002', '123', 'BJ001', '黄晓婷', '女', '2021-04-13', '团员', '13058129342', '四川省成都二仙桥10号', 'img/13.jpg');

SET FOREIGN_KEY_CHECKS = 1;
