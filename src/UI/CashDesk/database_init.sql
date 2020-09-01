CREATE DATABASE IF NOT EXISTS `testDB`;
USE `testDB`;

DROP TABLE IF EXISTS `testT`;
CREATE TABLE `testT` (
	`id` int(10) unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT,
	`name` varchar(100) NOT NULL DEFAULT 'Hans',
	`height` float unsigned NOT NULL DEFAULT 0
);

CREATE USER IF NOT EXISTS 'testRD'@'%' IDENTIFIED BY 'Pa$sw0rd';
GRANT SELECT ON `testDB`.* TO 'testRD'@'%' IDENTIFIED BY 'Pa$sw0rd';

CREATE USER IF NOT EXISTS 'testRW'@'localhost' IDENTIFIED BY 'Pa$sw0rd';
GRANT ALL PRIVILEGES ON `testDB`.* TO 'testRW'@'localhost' IDENTIFIED BY 'Pa$sw0rd';

INSERT INTO `testT` (name,height) VALUES ('Marcel Livotto',182.5);
