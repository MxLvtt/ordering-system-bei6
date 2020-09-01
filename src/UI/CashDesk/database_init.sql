# Create Database 'ordsys'
CREATE DATABASE IF NOT EXISTS `ordsys`;
USE `ordsys`;

# Create Table 'orders'
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
	`id` int unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT,
	`timestamp` int unsigned NOT NULL,
	`form` int unsigned NOT NULL DEFAULT 0,
	`state` int unsigned NOT NULL DEFAULT 0,
	`active` varchar(1) NOT NULL DEFAULT 'Y',
	`price` float unsigned DEFAULT 0,
	`meals` text NOT NULL
);

# Create Table 'meals'
DROP TABLE IF EXISTS `meals`;
CREATE TABLE `meals` (
	`id` int(10) unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT,
	`kategorie` varchar(200),
	`name` varchar(100) NOT NULL,
	`zutaten` varchar(200),
	`addons` varchar(200),
	`groessen` varchar(150),
	`price` float unsigned DEFAULT 0
);

# Create User for read-only access
DROP USER IF EXISTS 'ordsysRD'@'%';
CREATE USER IF NOT EXISTS 'ordsysRD'@'%' IDENTIFIED BY 'he=h5bY&x#Lb/=$';
GRANT SELECT ON `ordsys`.* TO 'ordsysRD'@'%' IDENTIFIED BY 'he=h5bY&x#Lb/=$';

# Create User for read-write access
DROP USER IF EXISTS 'ordsysRW'@'localhost';
CREATE USER IF NOT EXISTS 'ordsysRW'@'localhost' IDENTIFIED BY '#4}Yjen$]nP';
GRANT ALL PRIVILEGES ON `ordsys`.* TO 'ordsysRW'@'localhost' IDENTIFIED BY '#4}Yjen$]nP';
