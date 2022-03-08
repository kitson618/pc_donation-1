-- MySQL dump 10.13  Distrib 5.5.62, for Linux (x86_64)
--
-- Host: project-share-test.mysql.database.azure.com    Database: pc_donation
-- ------------------------------------------------------
-- Server version	5.6.47.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin_permission`
--

DROP TABLE IF EXISTS `admin_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `apply_status_id` int(11) DEFAULT NULL,
  `idtime` varchar(60) COLLATE utf8_unicode_ci DEFAULT NULL,
  `permission_admin_id` int(11) DEFAULT NULL,
  `permission_status` tinyint(1) DEFAULT NULL,
  `school_name` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL,
  `username` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `office_phone_number` int(11) DEFAULT NULL,
  `email` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL,
  `school_address` varchar(240) COLLATE utf8_unicode_ci DEFAULT NULL,
  `phone_number` int(11) DEFAULT NULL,
  `school_website` varchar(240) COLLATE utf8_unicode_ci DEFAULT NULL,
  `full_name` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_admin_permission_email` (`email`),
  UNIQUE KEY `ix_admin_permission_office_phone_number` (`office_phone_number`),
  UNIQUE KEY `ix_admin_permission_school_website` (`school_website`),
  UNIQUE KEY `ix_admin_permission_username` (`username`),
  KEY `apply_status_id` (`apply_status_id`),
  KEY `permission_admin_id` (`permission_admin_id`),
  KEY `ix_admin_permission_full_name` (`full_name`),
  KEY `ix_admin_permission_phone_number` (`phone_number`),
  KEY `ix_admin_permission_school_address` (`school_address`),
  KEY `ix_admin_permission_school_name` (`school_name`),
  CONSTRAINT `admin_permission_ibfk_1` FOREIGN KEY (`apply_status_id`) REFERENCES `apply_status` (`id`),
  CONSTRAINT `admin_permission_ibfk_2` FOREIGN KEY (`permission_admin_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_permission`
--

LOCK TABLES `admin_permission` WRITE;
/*!40000 ALTER TABLE `admin_permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `admin_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('c4031611fdc7');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `application`
--

DROP TABLE IF EXISTS `application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `application` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `story` varchar(140) COLLATE utf8_unicode_ci DEFAULT NULL,
  `apply_photo` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `idtime` varchar(60) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `status_id` int(11) DEFAULT NULL,
  `form_submission` tinyint(1) DEFAULT NULL,
  `apply_status_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `apply_status_id` (`apply_status_id`),
  KEY `status_id` (`status_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `application_ibfk_1` FOREIGN KEY (`apply_status_id`) REFERENCES `apply_status` (`id`),
  CONSTRAINT `application_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`),
  CONSTRAINT `application_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `application`
--

LOCK TABLES `application` WRITE;
/*!40000 ALTER TABLE `application` DISABLE KEYS */;
INSERT INTO `application` VALUES (57,'DEMO 1','DEMO story ','DemoA_21_34_28U77P22T1D235502F1DT20140107173834.jpg','2021-03-08 21:35:31',21,NULL,1,2),(58,'DEMO 2','DEMO story ','DemoB_21_34_28U77P22T1D235502F1DT20140107173834.jpg','2021-03-08 21:39:11',23,NULL,1,2),(59,'DEMO 3','DEMO story ','DemoD_21_34_28U77P22T1D235502F1DT20140107173834.jpg','2021-03-08 21:41:04',30,NULL,1,2),(60,'DEMO 4','DEMO story ','DemoA_21_34_28U77P22T1D235502F1DT20140107173834.jpg','2021-03-08 21:42:33',21,NULL,1,2),(61,'DEMO 5','DEMO story ','DemoA_21_34_28U77P22T1D235502F1DT20140107173834.jpg','2021-03-08 21:43:00',21,NULL,1,2),(62,'DEMO 6','DEMO story ','DemoA_21_34_28U77P22T1D235502F1DT20140107173834.jpg','2021-03-08 21:43:38',21,NULL,1,2),(63,'DEMO 7','DEMO story ','DemoA_21_34_28U77P22T1D235502F1DT20140107173834.jpg','2021-03-08 21:43:55',21,NULL,1,2),(64,'DEMO 8','DEMO story ','DemoA_21_34_28U77P22T1D235502F1DT20140107173834.jpg','2021-03-08 21:44:25',21,NULL,1,2),(65,'DEMO 9','DEMO story ','DemoA_21_34_28U77P22T1D235502F1DT20140107173834.jpg','2021-03-08 21:44:48',21,NULL,1,2),(66,'DEMO 10','DEMO story ','DemoA_21_34_28U77P22T1D235502F1DT20140107173834.jpg','2021-03-08 21:45:11',21,NULL,1,2),(67,'DEMO 11','DEMO story ','DemoA_21_34_28U77P22T1D235502F1DT20140107173834.jpg','2021-03-08 21:45:41',21,NULL,1,2),(68,'DEMO 12','DEMO story ','DemoA_21_34_28U77P22T1D235502F1DT20140107173834.jpg','2021-03-08 21:45:57',21,NULL,1,2),(69,'DEMO 13','DEMO story ','DemoA_21_34_28U77P22T1D235502F1DT20140107173834.jpg','2021-03-08 21:46:27',21,NULL,1,2),(70,'DEMO 14','DEMO story ','DemoA_21_34_28U77P22T1D235502F1DT20140107173834.jpg','2021-03-08 21:47:57',21,NULL,1,2),(71,'DEMO 15','DEMO story ','DemoA_21_34_28U77P22T1D235502F1DT20140107173834.jpg','2021-03-08 21:48:15',21,NULL,1,2),(72,'DEMO 16','DEMO story ','DemoA_21_34_28U77P22T1D235502F1DT20140107173834.jpg','2021-03-08 21:48:34',21,NULL,1,2),(73,'DEMO 17','DEMO story ','DemoA_21_34_28U77P22T1D235502F1DT20140107173834.jpg','2021-03-08 21:48:51',21,NULL,1,2),(74,'DEMO 18','DEMO story ','DemoA_21_34_28U77P22T1D235502F1DT20140107173834.jpg','2021-03-08 21:49:25',21,NULL,1,2),(75,'DEMO 19','DEMO story ','DemoA_21_34_28U77P22T1D235502F1DT20140107173834.jpg','2021-03-08 21:49:44',21,NULL,1,2),(76,'DEMO 20','DEMO story ','DemoA_21_34_28U77P22T1D235502F1DT20140107173834.jpg','2021-03-08 21:49:59',21,NULL,1,2),(77,'DEMO 21','DEMO story ','DemoA_21_34_28U77P22T1D235502F1DT20140107173834.jpg','2021-03-08 21:50:15',21,NULL,1,2),(78,'DEMO 22','DEMO story ','DemoA_21_34_28U77P22T1D235502F1DT20140107173834.jpg','2021-03-08 21:50:48',21,NULL,1,2),(79,'DEMO 23','DEMO story ','DemoA_21_34_28U77P22T1D235502F1DT20140107173834.jpg','2021-03-08 21:51:12',21,NULL,1,5),(80,'DEMO 23 test','DEMO 23 test','DemoA_22_53_44_apply_U77P22T1D235502F1DT20140107173834.jpg','2021-03-09 12:03:17',21,NULL,0,1),(81,'DEMO 24','DEMO 24','DemoD_12_07_20U77P22T1D235502F1DT20140107173834.jpg','2021-03-09 12:18:19',30,1,0,2),(82,'DEMO 25','DEMO 25','DemoD_12_30_25U77P22T1D235502F1DT20140107173834.jpg','2021-03-09 12:31:34',30,1,0,2),(83,'DEMO 26','DEMO 26','DemoD_12_36_40U77P22T1D235502F1DT20140107173834.jpg','2021-03-09 12:37:39',30,1,0,2),(84,'DEMO 27','DEMO 27','DemoD_12_42_18U77P22T1D235502F1DT20140107173834.jpg','2021-03-09 12:43:41',30,1,0,4);
/*!40000 ALTER TABLE `application` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `application_item`
--

DROP TABLE IF EXISTS `application_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `application_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `application_id` int(11) DEFAULT NULL,
  `donator_id` int(11) DEFAULT NULL,
  `obtained_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `application_id` (`application_id`),
  KEY `donator_id` (`donator_id`),
  KEY `item_id` (`item_id`),
  KEY `obtained_id` (`obtained_id`),
  CONSTRAINT `application_item_ibfk_1` FOREIGN KEY (`application_id`) REFERENCES `application` (`id`),
  CONSTRAINT `application_item_ibfk_2` FOREIGN KEY (`donator_id`) REFERENCES `user` (`id`),
  CONSTRAINT `application_item_ibfk_3` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`),
  CONSTRAINT `application_item_ibfk_4` FOREIGN KEY (`obtained_id`) REFERENCES `item_obtain` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=108 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `application_item`
--

LOCK TABLES `application_item` WRITE;
/*!40000 ALTER TABLE `application_item` DISABLE KEYS */;
INSERT INTO `application_item` VALUES (77,1,1,57,1,1),(78,1,1,58,1,1),(79,3,1,58,1,1),(80,1,1,59,1,1),(81,1,1,60,1,1),(82,1,1,61,1,1),(83,3,1,61,1,1),(84,1,1,62,1,1),(85,1,1,63,1,1),(86,1,1,64,1,1),(87,1,1,65,1,1),(88,1,1,66,1,1),(89,1,1,67,1,1),(90,1,1,68,1,1),(91,1,1,69,1,1),(92,1,1,70,1,1),(93,1,1,71,1,1),(94,1,1,72,1,1),(95,1,1,73,1,1),(96,2,1,74,1,1),(97,2,1,75,2,1),(98,2,1,76,1,1),(99,2,1,77,1,1),(100,2,1,78,1,1),(101,2,1,79,2,1),(102,1,1,80,1,1),(103,1,1,81,1,1),(104,1,1,82,1,1),(105,1,1,83,1,1),(106,1,1,84,88,2),(107,3,1,80,1,1);
/*!40000 ALTER TABLE `application_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apply_repair`
--

DROP TABLE IF EXISTS `apply_repair`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apply_repair` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `description` varchar(140) COLLATE utf8_unicode_ci DEFAULT NULL,
  `apply_status_id` int(11) DEFAULT NULL,
  `apply_repair_photo` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `address` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL,
  `idtime` varchar(60) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `volunteer_id` int(11) DEFAULT NULL,
  `confirm_button` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `apply_status_id` (`apply_status_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `apply_repair_ibfk_1` FOREIGN KEY (`apply_status_id`) REFERENCES `apply_status` (`id`),
  CONSTRAINT `apply_repair_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apply_repair`
--

LOCK TABLES `apply_repair` WRITE;
/*!40000 ALTER TABLE `apply_repair` DISABLE KEYS */;
INSERT INTO `apply_repair` VALUES (15,'bad windows','bad windows',1,'DemoA_12_39_52_repair_1200px-Bsodwindows10.png','27 Wood Road Wan Chai Hong Kong','2021-01-19 12:55:03',21,1,0),(16,'blue','blue',1,'DemoA_12_39_52_repair_1200px-Bsodwindows10.png','3 King Ling Road Tseung Kwan O New Territories','2021-01-19 12:57:19',21,1,1),(17,'blue','blue',1,'DemoA_12_39_52_repair_1200px-Bsodwindows10.png','30 Shing Tai Road Chai Wan Hong Kong','2021-01-19 12:57:55',21,1,0),(18,'blue','blue',1,'DemoA_12_39_52_repair_1200px-Bsodwindows10.png','702 Lai Chi Kok Road Cheung Sha Wan Kowloon','2021-01-19 12:58:40',21,1,0),(19,'blue','blue',1,'DemoA_12_39_52_repair_1200px-Bsodwindows10.png','20 Tsing Yi Road Tsing Yi Island New Territories','2021-01-19 12:59:18',21,1,0),(20,'blue','blue',1,'DemoA_12_39_52_repair_1200px-Bsodwindows10.png','18 Tsing Wun Road Tuen Mun New Territories','2021-01-19 13:00:12',21,1,0),(21,'blue','blue',1,'DemoA_12_39_52_repair_1200px-Bsodwindows10.png','20 Hing Shing Road Kwai Chung New Territories','2021-01-19 13:00:54',21,1,0),(22,'blue','blue',1,'DemoA_12_39_52_repair_1200px-Bsodwindows10.png','21 Yuen Wo Road Sha Tin New Territories','2021-01-19 13:01:35',21,1,0),(23,'blue','blue',1,'DemoA_12_39_52_repair_1200px-Bsodwindows10.png','25 Hiu Ming Street Kwun Tong Kowloon','2021-01-19 13:02:16',21,1,0),(24,'blue','blue',1,'DemoA_12_39_52_repair_1200px-Bsodwindows10.png','Level 6 46 Tai Yip Street, Kowloon Bay Kowloon','2021-01-19 13:03:08',21,1,0),(25,'blue','blue',4,'DemoA_12_39_52_repair_1200px-Bsodwindows10.png','7/F VTC Pokfulam Complex 145 Pokfulam Road Hong Kong','2021-01-19 13:04:11',21,6,1),(26,'blue','blue',1,'DemoA_12_39_52_repair_1200px-Bsodwindows10.png','11 Tin Ho Road, Tin Shui Wai New Territories','2021-01-19 13:05:09',21,1,0),(27,'Sasasdsd','asdsadas',1,'student_10_45_07_repair_DemoA_12_39_52pc.jpg','Mira Place Tower A 132 Nathan Road Tsim Sha Tsui Kowloon','2021-02-10 10:45:38',3,1,0),(28,'ts','ts',1,'DemoA_14_42_43_repair_300px-ANA_777-300_Taking_off_from_JFK.jpg','102 Pok Fu Lam Road Pok Fu Lam Hong Kong Island Hong Kong','2021-02-10 14:44:25',21,1,0),(31,'blue','blue',4,'DemoD_18_11_24_repair_1200px-Bsodwindows10.png','27 Wood Road Wan Chai Hong Kong','2021-03-09 18:12:15',30,6,1);
/*!40000 ALTER TABLE `apply_repair` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apply_status`
--

DROP TABLE IF EXISTS `apply_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apply_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_apply_status_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apply_status`
--

LOCK TABLES `apply_status` WRITE;
/*!40000 ALTER TABLE `apply_status` DISABLE KEYS */;
INSERT INTO `apply_status` VALUES (2,'Approved'),(4,'Completed'),(5,'Date and time confirming'),(8,'Draft status'),(1,'Need approval'),(6,'Reject'),(7,'Waiting for repair service'),(3,'Waiting for transaction');
/*!40000 ALTER TABLE `apply_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appointment_time`
--

DROP TABLE IF EXISTS `appointment_time`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `appointment_time` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `student_address` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `phone_number` int(11) DEFAULT NULL,
  `title` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `description` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `appointment_data` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `appointment_time` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `appointment_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `appointment_id` (`appointment_id`),
  CONSTRAINT `appointment_time_ibfk_1` FOREIGN KEY (`appointment_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointment_time`
--

LOCK TABLES `appointment_time` WRITE;
/*!40000 ALTER TABLE `appointment_time` DISABLE KEYS */;
INSERT INTO `appointment_time` VALUES (1,'student',' 133 Nathan Road Tsim Sha Tsui Kowloon',12345678,' Desktop burning',' All component not working','2020-12-31','05:51',5),(2,' student',' 134 Nathan Road Tsim Sha Tsui Kowloon',12345678,' Bad Computer',' Bad battery','2021-01-22','18:52',15),(3,' StudentDemoA',' 138 Nathan Road Tsim Sha Tsui Kowloon',56191162,' Bad Computer',' Computer battery can not use','2021-02-06','19:55',15),(4,'student',' 133 Nathan Road Tsim Sha Tsui Kowloon',12345678,' Desktop burning',' All component not working','2021-01-22','12:58',6),(5,'student',' 133 Nathan Road Tsim Sha Tsui Kowloon',12345678,' Desktop burning',' All component not working','2021-01-15','15:55',6),(6,'student',' 133 Nathan Road Tsim Sha Tsui Kowloon',12345678,' Desktop burning',' All component not working','2021-01-14','15:57',6),(7,'student',' 133 Nathan Road Tsim Sha Tsui Kowloon',12345678,' Desktop burning',' All component not working','2021-01-14','18:59',6),(8,'student',' 133 Nathan Road Tsim Sha Tsui Kowloon',12345678,' Desktop burning',' All component not working','2021-01-14','13:09',6),(9,'StudentDemoF','136 Nathan Road Tsim Sha Tsui Kowloon',12354542,'bad','bad','2021-01-18','21:46',6),(10,'StudentDemoB','3 King Ling Road Tiu Keng Leng Tseung Kwan O',12354568,'blue','blue','2021-01-18','21:54',6),(11,'StudentDemoA','3 King Ling Road Tiu Keng Leng Tseung Kwan O',56191162,'TEST','TEST','2021-01-18','22:56',6),(12,'DemoA','3 King Ling Road Tseung Kwan O New Territories',56191121,'blue','blue','2021-01-12','13:13',6),(13,'DemoA','7/F VTC Pokfulam Complex 145 Pokfulam Road Hong Kong',56191121,'blue','blue','2021-01-04','13:21',6),(14,'DemoD','27 Wood Road Wan Chai Hong Kong',88662345,'blue','blue','2021-03-10','18:15',6);
/*!40000 ALTER TABLE `appointment_time` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coordinates`
--

DROP TABLE IF EXISTS `coordinates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coordinates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `locations` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `locations` (`locations`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coordinates`
--

LOCK TABLES `coordinates` WRITE;
/*!40000 ALTER TABLE `coordinates` DISABLE KEYS */;
/*!40000 ALTER TABLE `coordinates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donate`
--

DROP TABLE IF EXISTS `donate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `donate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `item_id` int(11) DEFAULT NULL,
  `item_status_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `photo` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `application_id` int(11) DEFAULT NULL,
  `donate_status_id` int(11) DEFAULT NULL,
  `transaction_date` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `transaction_time` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `item_id` (`item_id`),
  KEY `item_status_id` (`item_status_id`),
  KEY `user_id` (`user_id`),
  KEY `application_id` (`application_id`),
  KEY `donate_status_id` (`donate_status_id`),
  CONSTRAINT `donate_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`),
  CONSTRAINT `donate_ibfk_2` FOREIGN KEY (`item_status_id`) REFERENCES `item_status` (`id`),
  CONSTRAINT `donate_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `donate_ibfk_4` FOREIGN KEY (`application_id`) REFERENCES `application` (`id`),
  CONSTRAINT `donate_ibfk_5` FOREIGN KEY (`donate_status_id`) REFERENCES `donate_status` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=95 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donate`
--

LOCK TABLES `donate` WRITE;
/*!40000 ALTER TABLE `donate` DISABLE KEYS */;
INSERT INTO `donate` VALUES (85,'09/03/2021 12:07:20',1,1,88,22.280995590482604,114.1858434677124,'DonateDemoB_12_07_20pc.jpg',84,3,'2021-03-09','12:49'),(94,'09/03/2021 20:06:54',2,1,2,22.264626216604004,114.23713803291321,'donate_20_06_54laptop.jpg',79,3,'2021-03-13','15:00');
/*!40000 ALTER TABLE `donate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donate_data`
--

DROP TABLE IF EXISTS `donate_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `donate_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL,
  `phone_number` int(11) DEFAULT NULL,
  `address` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_id` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_donate_data_email` (`email`),
  UNIQUE KEY `ix_donate_data_phone_number` (`phone_number`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `donate_data_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donate_data`
--

LOCK TABLES `donate_data` WRITE;
/*!40000 ALTER TABLE `donate_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `donate_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donate_status`
--

DROP TABLE IF EXISTS `donate_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `donate_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_donate_status_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donate_status`
--

LOCK TABLES `donate_status` WRITE;
/*!40000 ALTER TABLE `donate_status` DISABLE KEYS */;
INSERT INTO `donate_status` VALUES (4,'Donate successful'),(1,'Not chosen for donation'),(3,'Pending for donate / Waiting for transaction'),(2,'Selected for donate');
/*!40000 ALTER TABLE `donate_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donate_student`
--

DROP TABLE IF EXISTS `donate_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `donate_student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `donate_id` int(11) DEFAULT NULL,
  `student_id` int(11) DEFAULT NULL,
  `application_id` int(11) DEFAULT NULL,
  `transaction_id` int(11) DEFAULT NULL,
  `stu_address` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `application_id` (`application_id`),
  KEY `donate_id` (`donate_id`),
  KEY `student_id` (`student_id`),
  KEY `transaction_id` (`transaction_id`),
  CONSTRAINT `donate_student_ibfk_1` FOREIGN KEY (`application_id`) REFERENCES `application` (`id`),
  CONSTRAINT `donate_student_ibfk_2` FOREIGN KEY (`donate_id`) REFERENCES `donate` (`id`),
  CONSTRAINT `donate_student_ibfk_3` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`),
  CONSTRAINT `donate_student_ibfk_4` FOREIGN KEY (`transaction_id`) REFERENCES `donate_trans` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donate_student`
--

LOCK TABLES `donate_student` WRITE;
/*!40000 ALTER TABLE `donate_student` DISABLE KEYS */;
/*!40000 ALTER TABLE `donate_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donate_trans`
--

DROP TABLE IF EXISTS `donate_trans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `donate_trans` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `transaction_date` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `transaction_time` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `transaction_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `transaction_id` (`transaction_id`),
  CONSTRAINT `donate_trans_ibfk_1` FOREIGN KEY (`transaction_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donate_trans`
--

LOCK TABLES `donate_trans` WRITE;
/*!40000 ALTER TABLE `donate_trans` DISABLE KEYS */;
INSERT INTO `donate_trans` VALUES (1,'2020-12-31','03:50',2),(2,'2020-12-31','06:58',2),(3,'2020-12-31','17:03',2),(4,'2021-01-14','12:42',2),(5,'2021-01-22','12:48',2),(6,'2021-01-14','12:47',2),(7,'2021-01-15','15:48',2),(8,'2021-01-14','15:51',2),(9,'2021-01-14','16:05',2);
/*!40000 ALTER TABLE `donate_trans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `followers`
--

DROP TABLE IF EXISTS `followers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `followers` (
  `follower_id` int(11) DEFAULT NULL,
  `followed_id` int(11) DEFAULT NULL,
  KEY `followed_id` (`followed_id`),
  KEY `follower_id` (`follower_id`),
  CONSTRAINT `followers_ibfk_1` FOREIGN KEY (`followed_id`) REFERENCES `user` (`id`),
  CONSTRAINT `followers_ibfk_2` FOREIGN KEY (`follower_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `followers`
--

LOCK TABLES `followers` WRITE;
/*!40000 ALTER TABLE `followers` DISABLE KEYS */;
/*!40000 ALTER TABLE `followers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `introduction`
--

DROP TABLE IF EXISTS `introduction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `introduction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `intro` varchar(240) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_introduction_intro` (`intro`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `introduction`
--

LOCK TABLES `introduction` WRITE;
/*!40000 ALTER TABLE `introduction` DISABLE KEYS */;
/*!40000 ALTER TABLE `introduction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item`
--

DROP TABLE IF EXISTS `item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_name` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_item_item_name` (`item_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item`
--

LOCK TABLES `item` WRITE;
/*!40000 ALTER TABLE `item` DISABLE KEYS */;
INSERT INTO `item` VALUES (1,'Desktop'),(2,'Laptop'),(3,'Router');
/*!40000 ALTER TABLE `item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item_obtain`
--

DROP TABLE IF EXISTS `item_obtain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `item_obtain` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `obtain` varchar(60) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item_obtain`
--

LOCK TABLES `item_obtain` WRITE;
/*!40000 ALTER TABLE `item_obtain` DISABLE KEYS */;
INSERT INTO `item_obtain` VALUES (1,'❌'),(2,'✔');
/*!40000 ALTER TABLE `item_obtain` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item_status`
--

DROP TABLE IF EXISTS `item_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `item_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_Status` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_item_status_item_Status` (`item_Status`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item_status`
--

LOCK TABLES `item_status` WRITE;
/*!40000 ALTER TABLE `item_status` DISABLE KEYS */;
INSERT INTO `item_status` VALUES (1,'100%'),(4,'70%'),(3,'80%'),(2,'90%');
/*!40000 ALTER TABLE `item_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `permission_status` tinyint(1) DEFAULT NULL,
  `permission_status_id` int(11) DEFAULT NULL,
  `story` varchar(140) COLLATE utf8_unicode_ci DEFAULT NULL,
  `student_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `title` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `permission_id` int(11) DEFAULT NULL,
  `item_name` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `idtime` varchar(60) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `permission_status_id` (`permission_status_id`),
  KEY `permission_id` (`permission_id`),
  CONSTRAINT `permission_ibfk_1` FOREIGN KEY (`permission_status_id`) REFERENCES `application` (`id`),
  CONSTRAINT `permission_ibfk_2` FOREIGN KEY (`permission_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permission`
--

LOCK TABLES `permission` WRITE;
/*!40000 ALTER TABLE `permission` DISABLE KEYS */;
INSERT INTO `permission` VALUES (1,1,NULL,'I do not have money to buy it','StudentDemoF','i want to have lapto',16,'Laptop','2021-01-14 03:03:07'),(2,1,NULL,'I do not have money to buy it','StudentDemoY','i want to have lapto',14,'Laptop','2021-01-14 03:07:46'),(3,1,NULL,'DEMO A','DemoA','DEMO A',20,'Desktop','2021-01-19 13:12:16'),(4,1,NULL,'DemoA','DemoA','DemoA',20,'Desktop','2021-01-19 15:55:11'),(5,1,NULL,'demoa','DemoB','demoa',20,'Desktop','2021-01-19 17:55:26'),(6,1,NULL,'DEMO 24','DemoD','DEMO 24',20,'Desktop','2021-03-09 12:19:13'),(7,1,NULL,'DEMO 25','DemoD','DEMO 25',20,'Desktop','2021-03-09 12:33:04'),(8,1,NULL,'DEMO 26','DemoD','DEMO 26',20,'Desktop','2021-03-09 12:41:48'),(9,1,NULL,'DEMO 27','DemoD','DEMO 27',20,'Desktop','2021-03-09 12:45:19');
/*!40000 ALTER TABLE `permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `region`
--

DROP TABLE IF EXISTS `region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `region` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `region` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_region_region` (`region`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `region`
--

LOCK TABLES `region` WRITE;
/*!40000 ALTER TABLE `region` DISABLE KEYS */;
INSERT INTO `region` VALUES (1,'Central and Western'),(2,'Eastern'),(10,'Islands'),(5,'Kowloon City'),(11,'Kwai Tsing'),(6,'Kwun Tong'),(12,'North'),(13,'Sai Kung'),(14,'Sha Tin'),(7,'Sham Shui Po'),(3,'Southern'),(15,'Tai Po'),(16,'Tsuen Wan'),(17,'Tuen Mun'),(4,'Wan Chai'),(8,'Wong Tai Sin'),(9,'Yau Tsim Mong'),(18,'Yuen Long');
/*!40000 ALTER TABLE `region` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_student`
--

DROP TABLE IF EXISTS `role_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role_student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `role_student_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_student`
--

LOCK TABLES `role_student` WRITE;
/*!40000 ALTER TABLE `role_student` DISABLE KEYS */;
/*!40000 ALTER TABLE `role_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_teacher`
--

DROP TABLE IF EXISTS `role_teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role_teacher` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `role_teacher_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_teacher`
--

LOCK TABLES `role_teacher` WRITE;
/*!40000 ALTER TABLE `role_teacher` DISABLE KEYS */;
/*!40000 ALTER TABLE `role_teacher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_status_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status`
--

LOCK TABLES `status` WRITE;
/*!40000 ALTER TABLE `status` DISABLE KEYS */;
INSERT INTO `status` VALUES (2,'False'),(1,'True');
/*!40000 ALTER TABLE `status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stu_map`
--

DROP TABLE IF EXISTS `stu_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stu_map` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `application_id` int(11) DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `application_id` (`application_id`),
  CONSTRAINT `stu_map_ibfk_1` FOREIGN KEY (`application_id`) REFERENCES `application` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stu_map`
--

LOCK TABLES `stu_map` WRITE;
/*!40000 ALTER TABLE `stu_map` DISABLE KEYS */;
INSERT INTO `stu_map` VALUES (34,57,22.36268511968641,114.1313932007684),(35,58,22.302772376726107,114.18174760231095),(36,59,22.373338447372635,114.11776604228224),(37,60,22.35690256759022,114.12769317626953),(38,61,22.37231636816729,114.17834258736508),(39,62,22.340033508529753,114.20167922973633),(40,63,22.335428893048217,114.15623188018799),(41,64,22.33078442859172,114.16224002838135),(42,65,22.32467096613321,114.1682481765747),(43,66,22.313376235212022,114.17056560516357),(44,67,22.28556229157457,114.14271354675293),(45,68,22.286166453381952,114.15215525801516),(46,69,22.28039992282237,114.18502807617188),(47,70,22.27758039480211,114.17314052581787),(48,71,22.28834194964208,114.19382572174072),(49,72,22.297573988653266,114.17219638824463),(50,73,22.348448447339248,114.12614822387695),(51,74,22.332134117965225,114.16872024536133),(52,75,22.374761697997258,114.185950756073),(53,76,22.304264353991908,114.2526626586914),(54,77,22.30744067638816,114.25987243652344),(55,78,22.307817859874035,114.25957202911377),(56,79,22.264633663305023,114.23704147338867),(57,80,22.36388774466001,114.17078018188477),(58,81,22.287905149891845,114.20974731445312),(59,82,22.284767584539903,114.2161619381678),(60,83,22.28242518251432,114.19172286987305),(61,84,22.280995590482604,114.1858434677124);
/*!40000 ALTER TABLE `stu_map` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `teacher_email` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `school_name` varchar(140) COLLATE utf8_unicode_ci DEFAULT NULL,
  `school_address` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `student_address` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `school_URL` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `student_card_photo` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_username` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_username` (`user_username`),
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`user_username`) REFERENCES `user` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (1,'pcdonationdemo@gmail.com','vtc','1 King Ling Road Tseung Kwan O New Territories',NULL,'XD','student_student_card_StudentA_student_card_png.png','student'),(3,'makfung818@gmail.com','VTC','VTC',NULL,'VTC.COM','StudentDemoA_student_card_test1.jpeg','StudentDemoA'),(4,'samlam0206jp@yahoo.com','vtc hk','135 Nathan Road Tsim Sha Tsui Kowloon',NULL,'http://127.0.0.1:5000/auth/','StudentDemoB_student_card_volunteerx_volunteer_photo_test1.jpeg','StudentDemoB'),(5,'190337259@stu.vtc.edu.hk','vtc tw','135 Nathan Road Tsim Sha Tsui Kowloon',NULL,'http://127.0.0.1:5000/','StudentDemoD_student_card_volunteerx_volunteer_photo_test1.jpeg','StudentDemoD'),(6,'190337259@stu.vtc.edu.hk','vtc','120 Nathan Road Tsim Sha Tsui Kowloon',NULL,'http://127.0.0.1:5000/auth/student','StudentDemoF_student_card_StudentA_student_card_png.png','StudentDemoF'),(7,'190337259@stu.vtc.edu.hk','vtc','180 Nathan Road Tsim Sha Tsui Kowloon',NULL,'http://127.0.0.1:5000/auth/student','StudentDemoY_student_card_volunteerx_volunteer_photo_test1.jpeg','StudentDemoY'),(8,'m8521@yahoo.com','vtc','27 Wood Road Wan Chai Hong Kong',NULL,'vtc','DemoA_student_card_test1.jpeg','DemoA'),(9,'m8521@yahoo.com','vtc','27 Wood Road Wan Chai Hong Kong',NULL,'vtc','DemoB_student_card_test1.jpeg','DemoB'),(10,'fungchan01250@yahoo.com.hk','JCGSS','2B Oxford Rd Kowloon Tsai',NULL,'https://www.jcgss.edu.hk/','studentA_student_card_IMG_0014.JPG','studentA'),(39,'samlam020613@gmail.com','vtc','136 Nathan Road Tsim Sha Tsui Kowloon',NULL,'http://127.0.0.1:5000/auth/student','studentz_student_card_360_F_328101522_ezzWWm1FylxgfdUj6tnVskLgszJBUWsz.jpg','studentz'),(40,'m8521@yahoo.com','vtc','27 Wood Road Wan Chai Hong Kong',NULL,'vtc','DemoA_student_card_test1.jpeg','DemoD'),(41,'m8521@yahoo.com','vtc','27 Wood Road Wan Chai Hong Kong',NULL,'vtc.edu.hk','TestDemoA_student_card_2021_03_02_14_09_34test1.jpeg','TestDemoA'),(42,'samlam020613@gmail.com','VTC','27 Wood Road Wan Chai Hong Kong',NULL,'vtc.edu.hk','TestDemoB_student_card_2021_03_02_14_51_02test1.jpeg','TestDemoB');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher`
--

DROP TABLE IF EXISTS `teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teacher` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `school_name` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL,
  `school_address` varchar(240) COLLATE utf8_unicode_ci DEFAULT NULL,
  `school_website` varchar(240) COLLATE utf8_unicode_ci DEFAULT NULL,
  `office_phone_number` int(11) DEFAULT NULL,
  `user_id` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL,
  `teacher_cofirm` tinyint(1) DEFAULT NULL,
  `staff_card_photo` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_teacher_office_phone_number` (`office_phone_number`),
  KEY `user_id` (`user_id`),
  KEY `ix_teacher_school_address` (`school_address`),
  KEY `ix_teacher_school_name` (`school_name`),
  KEY `ix_teacher_school_website` (`school_website`),
  CONSTRAINT `teacher_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher`
--

LOCK TABLES `teacher` WRITE;
/*!40000 ALTER TABLE `teacher` DISABLE KEYS */;
INSERT INTO `teacher` VALUES (1,'vtc','2 King Ling Road Tseung Kwan O New Territories','XD',12345678,'teacher',NULL,NULL),(4,'vtc hk','136 Nathan Road Tsim Sha Tsui Kowloon','http://127.0.0.1:5000/auth',12354545,'TeacherB',NULL,NULL),(5,'vtc','27 Wood Road Wan Chai Hong Kong','vtc.com',23456789,'TeacherdemoA',NULL,NULL);
/*!40000 ALTER TABLE `teacher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher_apply`
--

DROP TABLE IF EXISTS `teacher_apply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teacher_apply` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status_id` int(11) DEFAULT NULL,
  `teacher_id` int(11) DEFAULT NULL,
  `apply_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `apply_id` (`apply_id`),
  KEY `status_id` (`status_id`),
  KEY `teacher_id` (`teacher_id`),
  CONSTRAINT `teacher_apply_ibfk_1` FOREIGN KEY (`apply_id`) REFERENCES `application` (`id`),
  CONSTRAINT `teacher_apply_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`),
  CONSTRAINT `teacher_apply_ibfk_3` FOREIGN KEY (`teacher_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher_apply`
--

LOCK TABLES `teacher_apply` WRITE;
/*!40000 ALTER TABLE `teacher_apply` DISABLE KEYS */;
/*!40000 ALTER TABLE `teacher_apply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher_permission`
--

DROP TABLE IF EXISTS `teacher_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teacher_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL,
  `username` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `email` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL,
  `phone_number` int(11) DEFAULT NULL,
  `school_name` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL,
  `school_address` varchar(240) COLLATE utf8_unicode_ci DEFAULT NULL,
  `school_URL` varchar(240) COLLATE utf8_unicode_ci DEFAULT NULL,
  `idtime` varchar(60) COLLATE utf8_unicode_ci DEFAULT NULL,
  `permission_status` tinyint(1) DEFAULT NULL,
  `permission_teacher_id` int(11) DEFAULT NULL,
  `apply_status_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_teacher_permission_email` (`email`),
  UNIQUE KEY `ix_teacher_permission_school_URL` (`school_URL`),
  UNIQUE KEY `ix_teacher_permission_username` (`username`),
  KEY `apply_status_id` (`apply_status_id`),
  KEY `permission_teacher_id` (`permission_teacher_id`),
  KEY `ix_teacher_permission_full_name` (`full_name`),
  KEY `ix_teacher_permission_phone_number` (`phone_number`),
  KEY `ix_teacher_permission_school_address` (`school_address`),
  KEY `ix_teacher_permission_school_name` (`school_name`),
  CONSTRAINT `teacher_permission_ibfk_1` FOREIGN KEY (`apply_status_id`) REFERENCES `apply_status` (`id`),
  CONSTRAINT `teacher_permission_ibfk_2` FOREIGN KEY (`permission_teacher_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher_permission`
--

LOCK TABLES `teacher_permission` WRITE;
/*!40000 ALTER TABLE `teacher_permission` DISABLE KEYS */;
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    /*!40000 ALTER TABLE `thanks_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL,
  `username` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `email` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL,
  `phone_number` int(11) DEFAULT NULL,
  `role` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `region_id` int(11) DEFAULT NULL,
  `password_hash` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `about_me` varchar(140) COLLATE utf8_unicode_ci DEFAULT NULL,
  `last_seen` datetime DEFAULT NULL,
  `confirm` tinyint(1) DEFAULT NULL,
  `user_photo` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `admin_confirm` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_user_email` (`email`),
  UNIQUE KEY `ix_user_username` (`username`),
  KEY `region_id` (`region_id`),
  KEY `ix_user_full_name` (`full_name`),
  KEY `ix_user_phone_number` (`phone_number`),
  KEY `ix_user_role` (`role`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`region_id`) REFERENCES `region` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'database','database',NULL,NULL,'default',NULL,NULL,NULL,'2020-12-31 00:21:03',0,NULL,NULL),(2,'donate','donate','likw00@gmail.com',12345678,'donate',1,'pbkdf2:sha256:150000$8bbWOA2n$c64fc9d731f31cf4f840041d346bdbbb39c8f85c7941ae675ce42800d2fbd8aa',NULL,'2021-03-09 11:29:40',1,NULL,NULL),(3,'student','student','pcdonationdemo@gmail.com',12345678,'student',1,'pbkdf2:sha256:150000$xFqJJiaC$875adb40397ccc25561776049c1a5829ff7ee6a736cadab7720f8604d6d580f8',NULL,'2021-03-02 10:37:10',1,NULL,1),(4,'teacher','teacher','190034746@stu.vtc.edu.hk',12345678,'teacher',1,'pbkdf2:sha256:150000$ayaXKorA$90fa65de2c4cd6ef42410ffe6b93705a70cba9a5086a9819e711c2558eff912c',NULL,'2021-03-01 14:33:11',1,'teacher_teacher_photo_donate_13_11_13item_photodonate_03_05_08IMG_0008.JPG',1),(5,'volunteer','volunteer','190110723@stu.vtc.edu.hk',12345678,'volunteer',1,'pbkdf2:sha256:150000$OwHcuyYW$8fc7eb034d0c2e38135bb64baa962a4bfba994a1fa5f7cfd681c51c874f60e6f',NULL,'2021-02-17 07:43:23',1,'volunteer_volunteer_photo_student_student_card_download.jpg',NULL),(6,'volunteer X','volunteerx','makfung818@gmail.com',56191164,'volunteer',14,'pbkdf2:sha256:150000$OrIOj85q$14a802d85a098e7adcf905ad80d4d92bb4ab10176070242bc011b8bf18c28a56',NULL,'2021-03-01 14:34:57',1,'volunteerx_volunteer_photo_test1.jpeg',NULL),(8,'StudentDemoA','StudentDemoA','makfung919@gmail.com',56191162,'student',1,'pbkdf2:sha256:150000$mmwAMb4M$4138279b037fdafa589ae05d05dacdcc61b37221c22cbd4518c92ebc9ff63e55',NULL,'2021-01-14 07:39:21',1,NULL,NULL),(9,'StudentDemoB','StudentDemoB','samlam0206jd@yahoo.com',12354568,'student',6,'pbkdf2:sha256:150000$7UNb44yP$bda46544981481e5cbd74be2c7823e0a7ee2ab51ad243e91f38896ac9658a8ae',NULL,'2021-01-17 13:57:36',1,NULL,NULL),(10,'StudentDemoC','StudentDemoC','samlam0206jd@gmail.com',12354567,'donate',12,'pbkdf2:sha256:150000$ZTgMnu9G$105786c691e23c9d9fa58ed50aa60acc0241476e535a2393a854a0c26cc28262',NULL,'2021-01-13 17:35:08',1,NULL,NULL),(11,'StudentDemoD','StudentDemoD','samlam02061jd@gmail.com',12354569,'student',13,'pbkdf2:sha256:150000$evCsa5Mu$a2b6c3cabcccb7cd4de3421fe2d8db754b0a031ce7e8c840469bda262f30f454',NULL,'2021-01-13 17:38:46',1,NULL,NULL),(14,'TeacherB','TeacherB','190337252@stu.vtc.edu.hk',12354542,'teacher',11,'pbkdf2:sha256:150000$yXpw9tDF$20514a517a84c036e6d575adcca1a83adabfdf2480579a2fe8bcd5980ca06958',NULL,'2021-01-13 19:19:22',1,'TeacherB_teacher_photo_CV_photo.jpg',NULL),(15,'volunteer B','volunteerB','samlam020614@gmail.com',97989953,'volunteer',12,'pbkdf2:sha256:150000$x3Tdr8Er$4e4563bbbc7a456cb21767794d01a46abad5918b0e4c4b2bbc38d883ceb256f5',NULL,'2021-01-13 18:53:33',1,'volunteerB_volunteer_photo_download.jpg',NULL),(16,'StudentDemoF','StudentDemoF','190337258@stu.vtc.edu.hk',12354542,'student',14,'pbkdf2:sha256:150000$hl9PIV1M$45149c3d2f58d68b323a58d1b4f74ea3317249b2a312be19bfba833907326cca',NULL,'2021-01-13 18:59:40',1,NULL,NULL),(17,'StudentDemoY','StudentDemoY','samlam0206jf@yahoo.com',12354564,'student',13,'pbkdf2:sha256:150000$hl9PIV1M$45149c3d2f58d68b323a58d1b4f74ea3317249b2a312be19bfba833907326cca',NULL,'2021-01-13 19:05:58',1,NULL,NULL),(20,'TeacherdemoA','TeacherdemoA','m8521@yahoo.com',56191111,'teacher',1,'pbkdf2:sha256:150000$hl9PIV1M$45149c3d2f58d68b323a58d1b4f74ea3317249b2a312be19bfba833907326cca',NULL,'2021-03-02 06:27:00',1,'TeacherdemoA_teacher_photo_png.png',1),(21,'DemoA','DemoA','m85222@yahoo.com',56191121,'student',1,'pbkdf2:sha256:150000$BZKtckIt$4b2f90acc1f21963a97bc069f27369f77fbbc76d175c156d2176fe5c52d0fbd2',NULL,'2021-03-01 14:03:30',1,'DemoA_student_card_test1.jpeg',1),(22,'DonateDemoA','DonateDemoA','ma8523@yahoo.com',56191211,'donate',1,'pbkdf2:sha256:150000$CrK1ovzZ$ea2383c45161123f94590c8fc250b7fb1fdb63be0cec6697c64f1dd16566c98e',NULL,'2021-01-31 18:35:00',1,NULL,1),(23,'DemoB','DemoB','ma85244@yahoo.com',56191122,'student',1,'pbkdf2:sha256:150000$lb4fV5el$fae03cae2367ae03155c73898363cd8f1269b86d060f0fd24c8237f63cf57fce',NULL,'2021-03-08 13:38:47',1,NULL,1),(24,'studentA','studentA','fungchan01250@yahoo.com.hk',23456789,'student',1,'pbkdf2:sha256:150000$4ySDBq1r$c84ef6c61eedff876ec9fb444801b8a60e1717005a29b8bf16ddeca4bcb5dc05',NULL,'2021-01-26 17:26:44',1,'DemoD_student_card_2021_02_04_21_37_49test1',1),(30,'DemoD','DemoD','garymak0075@gmail.com',88662345,'student',1,'pbkdf2:sha256:150000$CrnTCZai$8c478d0bd8a5044c7daa8ff39bacf0197919f265987bc9c3ce54a75e761cea3e',NULL,'2021-03-02 06:08:04',1,'DemoD_student_card_2021_02_04_21_37_49test1.jpeg',1),(31,'fungchan','fungchan','fungchan01240@yahoo.com.hk',98765432,'donate',1,'pbkdf2:sha256:150000$n1FRtb97$fe7e579ae0483d57723f784f10c4ae2eac614dbfcf41f910e32b5f953f1e752f',NULL,'2021-02-04 15:05:10',1,'DemoA_donate_photo_IMG_0014.JPG',1),(32,'donateA','donateA','donateA@gmail.com',98765431,'donate',1,'pbkdf2:sha256:150000$9ybuV8ls$009102b1e943906b3106e8d19086d3d7ea537fd853b6a2ebd26873e63950dfa3',NULL,'2021-02-04 16:01:21',1,'fungchan_donate_photo_IMG_0014.JPG',NULL),(34,'admin','admin','190337259@stu.vtc.edu.hk',97959954,'admin',2,'pbkdf2:sha256:150000$OrIOj85q$14a802d85a098e7adcf905ad80d4d92bb4ab10176070242bc011b8bf18c28a56',NULL,'2021-03-09 14:35:12',1,'TeacherB_teacher_photo_CV_photo.jpg',NULL),(81,'studentz','studentz','samlam020611@yahoo.com.hk',12354564,'student',1,'pbkdf2:sha256:150000$yGTHORPe$df72bbf238fa1800af292009c09d406967ec6e00c8fa6db0bd351c6703719cc0',NULL,'2021-03-01 12:34:53',1,NULL,1),(83,'TestDemoA','TestDemoA','makfung717@gmail.com',8866234,'student',1,'pbkdf2:sha256:150000$OHXIOUjR$8f599c02cd459b082bc273cfbbf72a428a4e1fb5d42e8be71780419bb2ffa4d5',NULL,'2021-03-02 06:09:39',1,'TestDemoA_student_card_2021_03_02_14_09_34test1.jpeg',1),(86,'TestDemoB','TestDemoB','samlam0206jp@gmail.com',86746234,'student',1,'pbkdf2:sha256:150000$np02tFWf$8729906e736df764c11ff89e322f856742d79a2262204b29ac467c7c10838153',NULL,'2021-03-02 10:38:27',1,'TestDemoB_student_card_2021_03_02_14_51_02test1.jpeg',1),(88,'DonateDemoB','DonateDemoB','190320056@stu.vtc.edu.hk',56191164,'donate',1,'pbkdf2:sha256:150000$xSak2UFf$7f62974f86d2aa13ab018ee4b9d7f3560f75241531111f85e77e71de9df5b59f',NULL,'2021-03-09 04:17:35',1,'DonateDemoB_donor_photo_Bill_Gates.jpg',0);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `volunteer`
--

DROP TABLE IF EXISTS `volunteer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `volunteer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL,
  `phone_number` int(11) DEFAULT NULL,
  `address` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_id` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_volunteer_email` (`email`),
  UNIQUE KEY `ix_volunteer_phone_number` (`phone_number`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `volunteer_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `volunteer`
--

LOCK TABLES `volunteer` WRITE;
/*!40000 ALTER TABLE `volunteer` DISABLE KEYS */;
INSERT INTO `volunteer` VALUES (1,'190110723@stu.vtc.edu.hk',12345678,'Mira Place Tower A 132 Nathan Road Tsim Sha Tsui Kowloon','volunteer'),(2,'makfung818@gmail.com',56191163,'4 Wong Chuk Hang Road Hong Kong','volunteerx'),(3,'190337259@stu.vtc.edu.hk',12354546,'138 Nathan Road Tsim Sha Tsui Kowloon','volunteerB');
/*!40000 ALTER TABLE `volunteer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `volunteer_repair`
--

DROP TABLE IF EXISTS `volunteer_repair`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `volunteer_repair` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `repair_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `repair_id` (`repair_id`),
  KEY `status_id` (`status_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `volunteer_repair_ibfk_1` FOREIGN KEY (`repair_id`) REFERENCES `apply_repair` (`id`),
  CONSTRAINT `volunteer_repair_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`),
  CONSTRAINT `volunteer_repair_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `volunteer_repair`
--

LOCK TABLES `volunteer_repair` WRITE;
/*!40000 ALTER TABLE `volunteer_repair` DISABLE KEYS */;
/*!40000 ALTER TABLE `volunteer_repair` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-09 15:43:29
