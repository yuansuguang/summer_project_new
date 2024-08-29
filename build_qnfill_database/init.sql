-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: qnfill_database
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
-- Table structure for table `survey_question_submit`
--

DROP TABLE IF EXISTS `survey_question_submit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `survey_question_submit` (
  `question_submit_id` int NOT NULL AUTO_INCREMENT,
  `answer` varchar(250) NOT NULL,
  `username` varchar(30) NOT NULL,
  `question_id_id` int NOT NULL,
  `survey_submit_id_id` int NOT NULL,
  `question_type` varchar(20) NOT NULL,
  `score` int DEFAULT NULL,
  PRIMARY KEY (`question_submit_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `survey_question_submit`
--

LOCK TABLES `survey_question_submit` WRITE;
/*!40000 ALTER TABLE `survey_question_submit` DISABLE KEYS */;
/*!40000 ALTER TABLE `survey_question_submit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `survey_survey_submit`
--

DROP TABLE IF EXISTS `survey_survey_submit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `survey_survey_submit` (
  `survey_submit_id` int NOT NULL AUTO_INCREMENT,
  `survey_submit_time` datetime(6) NOT NULL,
  `is_submitted` tinyint(1) NOT NULL,
  `survey_score` int NOT NULL,
  `username` varchar(30) NOT NULL,
  `survey_id_id` int NOT NULL,
  PRIMARY KEY (`survey_submit_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `survey_survey_submit`
--

LOCK TABLES `survey_survey_submit` WRITE;
/*!40000 ALTER TABLE `survey_survey_submit` DISABLE KEYS */;
/*!40000 ALTER TABLE `survey_survey_submit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'qnfill_database'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-29 16:34:09
