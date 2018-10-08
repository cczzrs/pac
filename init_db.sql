/*
Navicat MySQL Data Transfer

Source Server         : 0-0.cc
Source Server Version : 50624
Source Host           : 0-0.cc:3306
Source Database       : pac

Target Server Type    : MYSQL
Target Server Version : 50624
File Encoding         : 65001

Date: 2018-09-29 17:21:21
*/

USER pac;

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for operation_record
-- ----------------------------
DROP TABLE IF EXISTS `operation_record`;
CREATE TABLE `operation_record` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT '操作记录表',
  `hash_id` varchar(64) DEFAULT NULL,
  `resolve_date_begin` datetime DEFAULT NULL COMMENT '解析数据的时间范围-开始',
  `resolve_date_end` datetime DEFAULT NULL COMMENT '解析数据的时间范围-结束',
  `run_time` datetime DEFAULT NULL COMMENT '运行时间',
  `service_type` varchar(100) DEFAULT NULL COMMENT '业务类型',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间数据',
  `base_sources` varchar(5000) DEFAULT NULL COMMENT '解析源集合',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for spiders_base_source
-- ----------------------------
DROP TABLE IF EXISTS `spiders_base_source`;
CREATE TABLE `spiders_base_source` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `hash_id` varchar(64) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL COMMENT '城市',
  `province` varchar(100) DEFAULT NULL COMMENT '省份',
  `area` varchar(500) DEFAULT NULL COMMENT '地区',
  `service_type` varchar(100) DEFAULT NULL COMMENT '业务类型',
  `tags` varchar(255) DEFAULT NULL COMMENT '标签['''','''','''']多个',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间数据',
  `url_source` varchar(500) DEFAULT NULL COMMENT 'url地址',
  `url_type` varchar(2) DEFAULT NULL COMMENT 'url类型',
  `resolve_type` varchar(2) DEFAULT NULL COMMENT '解析类型',
  `resolve_rule` varchar(50) DEFAULT NULL COMMENT '解析规则',
  `resolve_source` varchar(5000) DEFAULT NULL COMMENT '解析源数据',
  `resolve_next_page` varchar(500) DEFAULT NULL COMMENT '下一页解析源',
  `resolve_page_wait` varchar(500) DEFAULT NULL COMMENT '页面加载等待',
  `run_time` datetime DEFAULT NULL COMMENT '最后运行时间',
  `run_count` int(10) unsigned zerofill DEFAULT NULL COMMENT '运行总次数',
  `content_page_rule` varchar(5000) DEFAULT NULL COMMENT '主体数据解析，子解析',
  `bz1` varchar(255) DEFAULT NULL COMMENT '备注',
  `bz2` varchar(255) DEFAULT NULL COMMENT '备注',
  `resolve_sources` varchar(5000) DEFAULT NULL COMMENT 'url地址',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=313 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for spiders_base_source_bef
-- ----------------------------
DROP TABLE IF EXISTS `spiders_base_source_bef`;
CREATE TABLE `spiders_base_source_bef` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `hash_id` varchar(64) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL COMMENT '城市',
  `province` varchar(100) DEFAULT NULL COMMENT '省份',
  `area` varchar(500) DEFAULT NULL COMMENT '地区',
  `service_type` varchar(100) DEFAULT NULL COMMENT '业务类型',
  `tags` varchar(255) DEFAULT NULL COMMENT '标签['''','''','''']多个',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间数据',
  `url_source` varchar(500) DEFAULT NULL COMMENT 'url地址',
  `url_type` varchar(2) DEFAULT NULL COMMENT 'url类型',
  `resolve_type` varchar(2) DEFAULT NULL COMMENT '解析类型',
  `resolve_rule` varchar(50) DEFAULT NULL COMMENT '解析规则',
  `resolve_source` varchar(5000) DEFAULT NULL COMMENT '解析源数据',
  `resolve_next_page` varchar(500) DEFAULT NULL COMMENT '下一页解析源',
  `resolve_page_wait` varchar(500) DEFAULT NULL COMMENT '页面加载等待',
  `run_time` datetime DEFAULT NULL COMMENT '最后运行时间',
  `run_count` int(10) unsigned zerofill DEFAULT NULL COMMENT '运行总次数',
  `content_page_rule` varchar(5000) DEFAULT NULL COMMENT '主体数据解析，子解析',
  `bz1` varchar(255) DEFAULT NULL COMMENT '备注',
  `bz2` varchar(255) DEFAULT NULL COMMENT '备注',
  `resolve_sources` varchar(5000) DEFAULT NULL COMMENT 'url地址',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=313 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for spiders_news
-- ----------------------------
DROP TABLE IF EXISTS `spiders_news`;
CREATE TABLE `spiders_news` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `hash_id` varchar(64) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL COMMENT '所在地区',
  `organization` varchar(255) DEFAULT NULL COMMENT '组织机构',
  `news_title` longtext COMMENT '文章标题',
  `news_type` varchar(255) DEFAULT NULL COMMENT '文章类型',
  `news_date` datetime DEFAULT NULL COMMENT '时间数据',
  `url_source` varchar(255) DEFAULT '' COMMENT 'url地址',
  `url_type` varchar(255) DEFAULT NULL,
  `resolve_type` varchar(255) DEFAULT NULL COMMENT '解析类型',
  `resolve_rule` varchar(255) DEFAULT NULL COMMENT '解析规则',
  `resolve_source` varchar(255) DEFAULT NULL COMMENT '解析源数据',
  `update_time` datetime DEFAULT NULL COMMENT '创建/更新时间',
  `bz1` varchar(255) DEFAULT NULL COMMENT '备注',
  `bz2` varchar(255) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3469 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

-- ----------------------------
-- Table structure for spiders_news_content
-- ----------------------------
DROP TABLE IF EXISTS `spiders_news_content`;
CREATE TABLE `spiders_news_content` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `hash_id` varchar(64) DEFAULT NULL,
  `news_content` longtext COMMENT '文章内容',
  `news_type` varchar(255) DEFAULT NULL COMMENT '文章类型',
  `update_time` datetime DEFAULT NULL,
  `url_source` varchar(255) DEFAULT '' COMMENT 'url地址',
  `url_type` varchar(255) DEFAULT NULL,
  `bz1` varchar(255) DEFAULT NULL COMMENT '备注',
  `bz2` varchar(255) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2616 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
