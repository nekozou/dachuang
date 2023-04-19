/*
 Navicat Premium Data Transfer

 Source Server         : zounuo
 Source Server Type    : MySQL
 Source Server Version : 80031
 Source Host           : localhost:3306
 Source Schema         : dachuang

 Target Server Type    : MySQL
 Target Server Version : 80031
 File Encoding         : 65001

 Date: 15/03/2023 11:47:25
*/
CREATE TABLE dc (
  time1 DATE,
  temp DOUBLE,
  humi INT,
	noin INT,
	wd INT,
	ws DOUBLE,
	ap DOUBLE,
	rainfull DOUBLE,
	noise DOUBLE,
	ui DOUBLE,
	o2 DOUBLE
);
LOAD DATA LOCAL INFILE '/media/hhm/E2A46D1CA46CF487/Document/大创/dachuang/chenyanhong/dachuang_1/data.csv' INTO TABLE mytable;
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

