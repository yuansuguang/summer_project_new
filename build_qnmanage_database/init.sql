-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: qnmanage_database
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `survey_question`
--

DROP TABLE IF EXISTS `survey_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `survey_question` (
  `question_id` int NOT NULL AUTO_INCREMENT,
  `question_title` varchar(100) NOT NULL,
  `question_description` varchar(250) DEFAULT NULL,
  `is_necessary` tinyint(1) NOT NULL,
  `sequence_id` int NOT NULL,
  `is_hidden` tinyint(1) NOT NULL,
  `question_type` varchar(30) NOT NULL,
  `option_num` int NOT NULL,
  `max_option_num` int NOT NULL,
  `score` int NOT NULL,
  `correct_answer` varchar(250) NOT NULL,
  `survey_id_id` int NOT NULL,
  `max_point` int NOT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`question_id`),
  KEY `survey_question_survey_id_id_922ec8a1_fk_survey_survey_survey_id` (`survey_id_id`),
  CONSTRAINT `survey_question_survey_id_id_922ec8a1_fk_survey_survey_survey_id` FOREIGN KEY (`survey_id_id`) REFERENCES `survey_survey` (`survey_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `survey_question`
--

LOCK TABLES `survey_question` WRITE;
/*!40000 ALTER TABLE `survey_question` DISABLE KEYS */;
INSERT INTO `survey_question` VALUES (2,'11111111111','11111111111',1,1,0,'radio',0,99999,0,'',14,0,''),(3,'您常玩的游戏类型是？','',1,2,0,'checkbox',0,99999,0,'',14,0,''),(4,'您玩游戏的月均消费为？','单位为人民币',1,3,0,'radio',0,99999,0,'',14,0,''),(5,'您玩游戏多长时间了？','',1,4,0,'radio',0,99999,0,'',14,0,''),(6,'您对本游戏的评价如何？','',0,5,0,'text',0,99999,0,'',14,0,''),(7,'给本游戏打个分吧~','',1,6,0,'mark',0,99999,0,'',14,10,'');
/*!40000 ALTER TABLE `survey_question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `survey_option`
--

DROP TABLE IF EXISTS `survey_option`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `survey_option` (
  `option_id` int NOT NULL AUTO_INCREMENT,
  `option_description` varchar(250) DEFAULT NULL,
  `sequence_id` int NOT NULL,
  `question_id_id` int NOT NULL,
  PRIMARY KEY (`option_id`),
  KEY `survey_option_question_id_id_d17fe2ff_fk_survey_qu` (`question_id_id`),
  CONSTRAINT `survey_option_question_id_id_d17fe2ff_fk_survey_qu` FOREIGN KEY (`question_id_id`) REFERENCES `survey_question` (`question_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `survey_option`
--

LOCK TABLES `survey_option` WRITE;
/*!40000 ALTER TABLE `survey_option` DISABLE KEYS */;
INSERT INTO `survey_option` VALUES (2,'11111111111',1,2),(3,'RPG',1,3),(4,'动作',2,3),(5,'卡牌',3,3),(6,'Rougelike',4,3),(7,'解密',5,3),(8,'塔防',6,3),(9,'类银河恶魔城',7,3),(10,'0 ~ 100',1,4),(11,'100 ~ 1000',2,4),(12,'1000 ~ 2000',3,4),(13,'2000以上',4,4),(14,'0 ~ 1 年',1,5),(15,'1 ~ 5 年',2,5),(16,'5 ~ 10 年',3,5),(17,'10年以上',4,5),(18,'',0,6),(19,'',0,7);
/*!40000 ALTER TABLE `survey_option` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `survey_survey`
--

DROP TABLE IF EXISTS `survey_survey`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `survey_survey` (
  `survey_id` int NOT NULL AUTO_INCREMENT,
  `survey_title` varchar(100) NOT NULL,
  `survey_description` varchar(250) DEFAULT NULL,
  `username` varchar(30) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `last_modified_time` datetime(6) NOT NULL,
  `deadline` datetime(6) DEFAULT NULL,
  `duration` int DEFAULT NULL,
  `submission_num` int NOT NULL,
  `max_submission` int NOT NULL,
  `is_available` tinyint(1) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `is_collected` tinyint(1) NOT NULL,
  `question_num` int NOT NULL,
  `max_question_num` int NOT NULL,
  `survey_type` varchar(30) NOT NULL,
  `is_random` tinyint(1) NOT NULL,
  `share_code` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`survey_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `survey_survey`
--

LOCK TABLES `survey_survey` WRITE;
/*!40000 ALTER TABLE `survey_survey` DISABLE KEYS */;
INSERT INTO `survey_survey` VALUES (14,'11111','1111111','Starduster','2024-08-29 07:41:57.517212','2024-08-29 15:48:40.538923',NULL,NULL,0,10000,1,0,0,6,99999,'1',0,'31be73061f9de6113779bb13f7be55f5d094b4dc82060cab6d90e19d32552632');
/*!40000 ALTER TABLE `survey_survey` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-29 16:28:47
