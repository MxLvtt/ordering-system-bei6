# Create Database 'ordsys'
CREATE DATABASE IF NOT EXISTS `ordsys2`;
USE `ordsys2`;

# Create Table 'orders'
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
	`id` int(10) unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT,
	`timestamp` int(10) unsigned NOT NULL,
	`form` int(10) unsigned NOT NULL DEFAULT 0,
	`state` int(10) unsigned NOT NULL DEFAULT 0,
	`active` varchar(1) NOT NULL DEFAULT 'Y',
	`price` float unsigned NOT NULL DEFAULT 0,
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
	`price` float unsigned DEFAULT 0,
);

# Create User for read-only access
CREATE USER IF NOT EXISTS 'ordsys2RD'@'%' IDENTIFIED BY 'Pa$sw0rd';
GRANT SELECT ON `ordsys2`.* TO 'ordsys2RD'@'%' IDENTIFIED BY 'Pa$sw0rd';

# Create User for read-write access
CREATE USER IF NOT EXISTS 'ordsys2RW'@'localhost' IDENTIFIED BY 'Pa$sw0rd';
GRANT ALL PRIVILEGES ON `ordsys2`.* TO 'ordsys2RW'@'localhost' IDENTIFIED BY 'Pa$sw0rd';

# Fill 'meals' Table
INSERT INTO `meals` (kategorie,name,price) VALUES ('Essen',			'Currywurst mit Pommes',		5.5);
INSERT INTO `meals` (kategorie,name,price) VALUES ('Essen',			'Döner Box',					4);
INSERT INTO `meals` (kategorie,name,price) VALUES ('Essen',			'Döner Teller',					7);
INSERT INTO `meals` (kategorie,name,price) VALUES ('Essen/Burger',	'Cheeseburger mit Pommes',		6.8);
INSERT INTO `meals` (kategorie,name,price) VALUES ('Essen/Burger',	'Cheeseburger',					4.5);
INSERT INTO `meals` (kategorie,name,price) VALUES ('Essen/Burger',	'Cheeseburger mit Bacon',		4.8);
INSERT INTO `meals` (kategorie,name,price) VALUES ('Essen/Burger',	'Cheeseburger Bacon Pommes',	6.8);
INSERT INTO `meals` (kategorie,name,price) VALUES ('Essen/Burger',	'Chickenburger mit Pommes',		6.8);
INSERT INTO `meals` (kategorie,name,price) VALUES ('Essen/Burger',	'Chickenburger',				4.8);
INSERT INTO `meals` (kategorie,name,price) VALUES ('Essen/Burger',	'Whiteburger mit Pommes',		8);
INSERT INTO `meals` (kategorie,name,price) VALUES ('Essen/Burger',	'Whiteburger',					6);
INSERT INTO `meals` (kategorie,name,price) VALUES ('Essen/Burger',	'Veggieburger mit Pommes',		6.8);
INSERT INTO `meals` (kategorie,name,price) VALUES ('Essen/Burger',	'Veggieburger',					4.8);
INSERT INTO `meals` (kategorie,name,price) VALUES ('Essen',			'Pommes Groß',					3);
INSERT INTO `meals` (kategorie,name,price) VALUES ('Essen',			'Pommes Klein',					2);

exit;
