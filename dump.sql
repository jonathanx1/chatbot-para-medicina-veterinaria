-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: chatbot_veterinario
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `consultas`
--

DROP TABLE IF EXISTS `consultas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `consultas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) NOT NULL,
  `consulta` text NOT NULL,
  `respuesta` text NOT NULL,
  `fecha` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `consultas_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=239 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consultas`
--

LOCK TABLES `consultas` WRITE;
/*!40000 ALTER TABLE `consultas` DISABLE KEYS */;
INSERT INTO `consultas` VALUES (1,1,'mi perro tiene tos','Traqueobronquitis','2025-04-10 18:25:06'),(2,2,'mi gato tiene diarrea','Parvovirus','2025-04-11 10:26:02'),(4,2,'mi perro tiene fiebre y tos seca','Moquillo','2025-04-11 10:39:00'),(5,2,'mi perro tiene fiebre leve y tos seca','Moquillo','2025-04-11 10:39:25'),(6,2,'mi perro tiene tos y fiebre','Moquillo','2025-04-11 10:39:49'),(7,2,'mi perro tiene fiebre leve y tos seca','Moquillo','2025-04-11 10:46:48'),(8,1,'mi gato tiene fiebre leve y tos seca','Moquillo','2025-04-11 10:48:34'),(9,1,'mi perro tiene fiebre leve y tos seca','Desconocido','2025-04-11 11:06:00'),(11,1,'mi perro tiene fiebre leve  tos seca','Desconocido','2025-04-11 11:15:11'),(12,1,'mi perro tiene fiebre','Desconocido','2025-04-11 11:21:06'),(13,1,'mi perro tiene fiebre leve y tos seca','Desconocido','2025-04-11 11:26:53'),(14,1,'mi perro tiene fiebre leve y tos seca','Desconocido','2025-04-11 11:37:51'),(15,1,'mi perro tiene fiebre levey tos seca','Desconocido','2025-04-11 11:45:35'),(16,1,'mi perro tiene tos seca y fiebre leve','Desconocido','2025-04-11 11:50:59'),(17,1,'mi perro tiene tos ','Desconocido','2025-04-11 11:51:18'),(18,1,'mi perro tiene fiebre ','Desconocido','2025-04-11 12:01:05'),(23,1,'mi perro tiene diarrea','Parvovirus','2025-04-11 17:58:41'),(24,1,'mi perro tiene fiebre','Moquillo','2025-04-11 18:57:18'),(27,2,'mi gato tiene diarrea','Parvovirus','2025-04-11 22:34:23'),(28,2,'mi gato tiene diarrea','Parvovirus','2025-04-11 22:34:23'),(29,5,'mi perro tiene tos','Traqueobronquitis','2025-04-11 22:35:15'),(30,5,'mi perro tiene fiebre','Moquillo','2025-04-11 22:41:08'),(31,5,'mi perro tiene dolor de cabeza','Sin coincidencias','2025-04-11 22:41:54'),(32,1,'mi perro tiene dolor de cabeza','Parvovirus','2025-04-11 22:50:06'),(33,1,'mi perro tiene dolor de cabeza','Parvovirus','2025-04-13 20:24:30'),(34,5,'mi gato tiene dolor de cabeza','Parvovirus','2025-04-13 20:35:47'),(35,5,'mi perro tiene dolor de cabeza','Parvovirus','2025-04-13 21:06:43'),(36,5,'mi perro tiene dolor de cabeza\r\n','Parvovirus','2025-04-13 21:09:22'),(37,5,'mi perro tiene dolor de cabeza','Parvovirus','2025-04-13 21:14:02'),(38,5,'mi perro tiene dolor de cabza','Sin coincidencias','2025-04-13 22:45:10'),(39,5,'mi perro tiene dolor de cabeza\r\n\r\n','Parvovirus','2025-04-13 22:45:23'),(40,5,'mi perro tiene dolor de cabeza','Traqueobronquitis','2025-04-13 22:46:53'),(41,5,'mi perro tiene dolor de cabeza','Traqueobronquitis','2025-04-13 22:48:15'),(42,5,'mi perro tiene dolor de cabeza\r\n','Traqueobronquitis','2025-04-13 22:48:51'),(43,1,'mi perro tiene dolor de cabeza','Traqueobronquitis','2025-04-13 23:09:07'),(44,1,'mi perro tiene dolor de cabeza','Traqueobronquitis','2025-04-13 23:41:21'),(45,1,'mi perro tiene dolor de cabeza\r\n\r\n','Traqueobronquitis','2025-04-14 00:01:40'),(46,1,'mi perro tiene fiebre','Traqueobronquitis','2025-04-14 00:03:37'),(47,1,'mi perro tiene dolor de cabeza','Traqueobronquitis','2025-04-14 00:04:09'),(48,5,'mi perro tiene dolor de cabeza','Traqueobronquitis','2025-04-14 01:24:14'),(49,1,'mi perro tiene dolor de cabeza','Traqueobronquitis','2025-04-27 22:32:53'),(50,1,'mi perro tiene dolor de cabeza','migra√±a','2025-04-27 22:56:06'),(51,1,'mi perro tiene tos y fiebre','Parvovirus','2025-04-27 22:57:16'),(52,2,'mi perro tiene dolor de cabeza','migra√±a','2025-04-27 22:59:07'),(53,5,'mi perro tiene tos y secrecion nasal','Parvovirus','2025-04-27 23:16:38'),(54,5,'mi perro tiene tos y secrecion nasal','Parvovirus','2025-04-27 23:18:03'),(55,5,'mi perro tiene dolor de cabeza','migra√±a','2025-04-27 23:18:47'),(56,1,'mi perro tiene tos pero no fiebre','Parvovirus','2025-04-28 00:49:40'),(57,1,'mi perro no tiene fiebre pero si tos seca','Parvovirus','2025-04-28 00:54:55'),(58,1,'mi perro no tiene fiebre pero si tos seca','Parvovirus','2025-04-28 01:54:14'),(59,1,'mi perro no tiene fiebre pero si tos seca','Parvovirus','2025-04-28 02:11:12'),(60,1,'mi perro no tiene fiebre pero s√≠ tos seca','Parvovirus','2025-04-28 02:17:39'),(61,1,'mi perro no tiene fiebre pero s√≠ tos seca\r\n','Parvovirus','2025-04-28 02:27:29'),(62,1,'mi perro no tiene fiebre pero s√≠ tos seca\r\n','Parvovirus','2025-04-28 02:30:57'),(63,1,'mi perro no tiene fiebre pero s√≠ tos seca\r\n','Parvovirus','2025-04-28 02:31:46'),(64,1,'mi perro tiene fiebre','Parvovirus','2025-05-04 00:26:32'),(65,1,'mi perro tiene dolor de cabeza','migra√±a','2025-05-04 01:25:54'),(66,5,'mi gato tiene mareos','Sin coincidencias','2025-05-04 01:40:39'),(67,5,'mi gato tiene mareos','viruela','2025-05-04 01:49:38'),(68,5,'mi gato tiene mareos','viruela fwef','2025-05-04 01:56:45'),(69,5,'mi perro tiene mareos','viruela fwef','2025-05-04 01:56:56'),(70,5,'mi perro tiene tos','Moquillo','2025-05-04 01:57:56'),(71,5,'mi perro tiene tos y estornudos','Moquillo','2025-05-04 01:58:10'),(72,5,'mi perro tiene tos y estornudos','Moquillo','2025-05-04 01:59:07'),(73,5,'mi perro tiene tos y estornudos','gripa','2025-05-04 02:03:07'),(74,5,'mi perro tiene tos pero no fiebre','Parvovirus','2025-05-04 02:03:27'),(75,5,'mi perro tiene tos pero no fiebre','Sin coincidencias','2025-05-04 02:07:47'),(76,5,'mi perro tiene tos pero no fiebre','Moquillo','2025-05-04 02:13:20'),(77,5,'mi perro tiene tos pero no fiebre','gripa','2025-05-04 02:25:34'),(78,5,'mi perro tiene fiebre pero no tos','Parvovirus','2025-05-04 02:26:10'),(79,5,'mi perro presenta tos pero no presenta fiebre','Parvovirus','2025-05-04 02:29:41'),(80,5,'mi perro presenta tos sin embargo carece de fiebre','Parvovirus','2025-05-04 02:36:05'),(81,5,'mi perro presenta tos sin embargo no presenta fiebre\r\n\r\n','Sin coincidencias','2025-05-04 02:36:30'),(82,5,'mi perro presenta tos ','Moquillo','2025-05-04 02:48:40'),(83,5,'mi perro tiene tos pero no fiebre','Parvovirus','2025-05-04 03:23:17'),(84,5,'mi perro tiene tos pero no fiebre','Parvovirus','2025-05-04 03:24:12'),(85,5,'mi perro tiene tos pero no fiebre','Parvovirus','2025-05-04 03:25:31'),(86,5,'mi perro tiene tos pero no fiebre','Parvovirus','2025-05-04 03:28:10'),(87,5,'mi perro tiene tos pero no fiebre','Parvovirus','2025-05-04 03:29:40'),(88,5,'mi perro tiene tos pero no fiebre','gripa','2025-05-04 03:30:55'),(89,5,'mi perro tiene fiebre pero no tos','Parvovirus','2025-05-04 03:31:11'),(90,1,'mi perro tiene tos y fiebre','Parvovirus','2025-05-04 23:26:24'),(91,1,'mi perro tiene mareos','viruela fwef','2025-05-04 23:27:12'),(92,1,'mi perro presenta tos y fiebre','Parvovirus','2025-05-04 23:38:10'),(93,1,'Mi perro no tiene fiebre pero s√≠ tos seca\r\n\r\n','Moquillo','2025-05-05 00:00:09'),(94,1,'Mi perro no tiene fiebre pero s√≠ tos seca','gripa','2025-05-05 00:04:42'),(95,1,'Mi perro no tiene fiebre pero s√≠ tos seca','gripa','2025-05-05 00:08:17'),(96,1,'mi perro tiene fiebre y tos seca','Parvovirus','2025-05-05 23:35:32'),(97,1,'mi perro tiene fiebre y tos seca\r\n\r\n','Parvovirus','2025-05-05 23:37:33'),(98,1,'mi perro tiene tos y fiebre','Parvovirus','2025-05-05 23:37:54'),(99,1,'mi perro esta enfermo tiene tos y fiebre, me puedes ayudar','Parvovirus','2025-05-05 23:38:26'),(100,1,'ayudame mi perro tiene vomito, diarrea y fiebre','Parvovirus','2025-05-06 00:13:31'),(101,1,'hola','Sin coincidencias','2025-05-06 00:18:53'),(102,1,'mi gato tiene tos y fiebre','Modelo no disponible','2025-05-07 05:54:58'),(103,1,'mi gato tiene tos y fiebre','Modelo no disponible','2025-05-07 06:08:57'),(104,1,'mi gato tiene tos y fiebre','Modelo no disponible','2025-05-07 20:31:50'),(105,1,'mi perro tiene tos y fiebre','Parvovirus','2025-05-07 20:32:36'),(106,1,'mi gato tiene tos y fiebre','Parvovirus','2025-05-07 20:37:04'),(107,1,'mi gato tiene tos y fiebre','Moquillo','2025-05-07 20:37:26'),(108,1,'mi perro tiene tos y fiebre','Moquillo','2025-05-07 21:03:13'),(109,1,'mi gato tiene tos y fiebre','Moquillo','2025-05-07 21:03:38'),(110,1,'mi gato tiene tos y fiebre','‚ö†Ô∏è Lo siento, no puedo procesar esta consulta para la especie indicada.','2025-05-08 04:17:24'),(111,1,'mi perro tiene fiebre y diarrea','Parvovirus','2025-05-08 04:23:35'),(112,1,'mi perro tiene tos seca y fiebre','Parvovirus','2025-05-08 04:24:03'),(113,1,'mi perro tiene tos srca y fiebre','Moquillo','2025-05-08 04:35:05'),(114,1,'mi perro tiene tos seca y fiebre\r\n\r\n','Parvovirus','2025-05-08 04:35:26'),(115,1,'mi perro tiene fiebre leve y tos seca','Traqueobronquitis','2025-05-08 04:44:13'),(116,1,'mi perro tiene fiebre y tos seca\r\n\r\n','Parvovirus','2025-05-08 04:44:42'),(117,1,'mi perro tiene diarrea y vomito','Parvovirus','2025-05-08 04:45:28'),(118,1,'mi perro tiene diarrea y vomito','Parvovirus','2025-05-08 05:01:00'),(119,1,'mi perro tiene tos sgcr y fiebre','Moquillo','2025-05-08 05:01:30'),(120,1,'mi perro tiene tos, fiebre y secrecion nasal','Moquillo','2025-05-08 05:02:55'),(121,1,'mi perro tiene tos sgcr y fiebre\r\n\r\n','migra√±a','2025-05-08 06:06:31'),(122,1,'mi perro tiene tos sgcr y fiebre','migra√±a','2025-05-08 06:14:29'),(123,1,'mi perro tiene tos sgcr y fiebre\r\n\r\n','migra√±a','2025-05-12 00:30:41'),(124,1,'mi perro tiene fiebre y tos','migra√±a','2025-05-12 00:31:23'),(125,1,'mi perro tiene fiebre y tos\r\n\r\n','migra√±a','2025-05-12 00:40:31'),(126,1,'mi perro tiene fiebre y tos\r\n\r\n','Moquillo','2025-05-12 00:41:42'),(127,1,'mi perro tiene fiebre pero no tos\r\n\r\n','Moquillo','2025-05-12 00:42:02'),(128,1,'mi perro tiene fiebre pero no tos\r\n\r\n','Moquillo','2025-05-12 00:43:04'),(129,1,'mi perro tiene tos, fiebre y secrecion nasal\r\n\r\n','Moquillo','2025-05-12 00:48:29'),(130,1,'mi perro tiene tos pero no fiebre\r\n\r\n','Parvovirus','2025-05-12 00:48:49'),(131,1,'mi perro tiene tos pero no fiebre\r\n\r\n','Parvovirus','2025-05-12 00:49:41'),(132,1,'mi perro tiene tos pero no fiebre\r\n\r\n','Parvovirus','2025-05-12 00:50:11'),(133,1,'mi perro tiene tos pero no fiebre\r\n\r\n','Parvovirus','2025-05-12 00:50:38'),(134,1,'mi perro tiene tos pero no fiebre\r\n\r\n','Parvovirus','2025-05-12 00:52:14'),(135,1,'mi perro tiene tos pero no fiebre\r\n\r\n','Parvovirus','2025-05-12 00:53:16'),(136,1,'mi perro tiene tos pero no fiebre\r\n\r\n','Parvovirus','2025-05-12 01:08:33'),(137,1,'mi perro tiene tos pero no fiebre\r\n\r\n','Parvovirus','2025-05-12 01:18:46'),(138,1,'mi perro tiene vomito','Parvovirus','2025-05-12 01:19:30'),(139,1,'mi perro tiene secrecion nasal','migra√±a','2025-05-12 01:19:53'),(140,1,'mi perro tiene tos pero no fiebre\r\n\r\n','Parvovirus','2025-05-12 01:50:40'),(141,1,'mi perro tiene tos pero no fiebre\r\n\r\n','Moquillo','2025-05-12 01:51:47'),(142,1,'mi perro tiene vomito','migra√±a','2025-05-12 01:52:00'),(143,1,'mi perro tiene vomito','migra√±a','2025-05-12 01:57:20'),(144,1,'mi perro tiene vomito\r\n\r\n','Parvovirus','2025-05-12 01:57:56'),(145,1,'mi perro tiene tos pero no fiebre','Parvovirus','2025-05-12 01:58:18'),(146,1,'mi perro tiene vomito','migra√±a','2025-05-12 02:08:44'),(147,1,'mi perro tiene vomito','Parvovirus','2025-05-12 02:12:22'),(148,1,'mi perro tiene tos pero no fiebre','Moquillo','2025-05-12 02:12:38'),(149,1,'mi perro tiene tos pero no fiebre\r\n\r\n','Moquillo','2025-05-12 02:14:05'),(150,1,'mi perro no tiene tos pero si fiebre','migra√±a','2025-05-12 02:14:38'),(151,1,'mi perro tiene tos pero no fiebre','Parvovirus','2025-05-12 02:16:56'),(152,1,'mi perro tiene tos pero no fiebre','Parvovirus','2025-05-12 02:17:27'),(153,1,'mi perro tiene tos pero no fiebre\r\n\r\n','Parvovirus','2025-05-12 02:21:00'),(154,1,'mi perro tiene vomito pero no tos','Parvovirus','2025-05-12 02:21:17'),(155,1,'mi perro tiene fiebre pero no tos','Moquillo','2025-05-12 02:21:40'),(156,1,'mi perro tiene tos pero no fiebre','migra√±a','2025-05-12 02:23:27'),(157,1,'mi perro tiene tos pero no fiebre\r\n','Parvovirus','2025-05-12 05:55:30'),(158,1,'mi perro tiene vomito','Parvovirus','2025-05-12 05:55:44'),(159,1,'mi perro tiene tos pero no fiebre\r\n\r\n','migra√±a','2025-05-12 21:35:27'),(160,1,'mi perro tiene tos pero no fiebre','migra√±a','2025-05-12 21:45:34'),(161,1,'mi perro tiene tos pero no fiebre','migra√±a','2025-05-12 21:49:22'),(162,1,'mi perro tiene tos pero no fiebre\r\n\r\n','Parvovirus','2025-05-12 21:55:09'),(163,1,'mi perro tiene tos pero no fiebre\r\n\r\n','migra√±a','2025-05-12 22:04:32'),(164,1,'mi perro tiene tos pero no fiebre\r\n\r\n','migra√±a','2025-05-12 22:05:12'),(165,1,'mi perro tiene tos pero no fiebre\r\n','gripa','2025-05-12 22:06:29'),(166,1,'mi perro tiene tos pero no fiebre\r\n','gripa','2025-05-12 22:08:08'),(167,1,'mi perro no tiene tos pero si fiebre','Parvovirus','2025-05-12 22:08:28'),(168,1,'mi perro tiene vomito','Parvovirus','2025-05-12 22:08:40'),(169,1,'mi perro tiene secrecion nasal','migra√±a','2025-05-12 22:08:59'),(170,1,'mi perro tiene tos y fiebre','Moquillo','2025-05-12 22:09:47'),(171,1,'mi perro tiene tos, fiebre y secrecion nasal','Moquillo','2025-05-12 22:10:37'),(172,1,'mi perro tiene estornudos','gripa','2025-05-12 22:11:43'),(173,1,'mi perro tiene tos, fiebre y secrecion nasal\r\n\r\n','Moquillo','2025-05-12 22:13:09'),(174,1,'mi perro tiene secrecion nasal\r\n','migra√±a','2025-05-12 22:17:05'),(175,1,'mi perro tiene secrecion nasal\r\n\r\n','migra√±a','2025-05-12 22:21:49'),(176,1,'mi perro tiene secrecion nasal\r\n\r\n','migra√±a','2025-05-12 22:22:15'),(177,1,'mi perro tiene secrecion nasal\r\n\r\n','migra√±a','2025-05-12 22:26:34'),(178,1,'mi perro tiene secrecion nasal\r\n\r\n','migra√±a','2025-05-12 22:28:51'),(179,1,'mi perro tiene secrecion nasal\r\n\r\n','Moquillo','2025-05-12 22:32:59'),(180,1,'mi perro tiene fiebre, tos y secrecion nasal','Moquillo','2025-05-12 22:37:26'),(181,1,'mi perro tiene vomito','Parvovirus','2025-05-12 22:37:44'),(182,1,'mi perro tiene fiebre leve','Parvovirus','2025-05-12 22:39:46'),(183,1,'mi perro tiene fiebre leve\r\n\r\n','Parvovirus','2025-05-12 22:52:52'),(184,1,'mi perro tiene fiebre leve\r\n\r\n','Traqueobronquitis','2025-05-12 23:15:28'),(185,1,'mi perro tiene fiebre','Parvovirus','2025-05-12 23:15:50'),(186,1,'mi perro tiene tos seca y fiebre leve','Traqueobronquitis','2025-05-12 23:16:07'),(187,1,'mi perro tiene fiebre alta\r\n\r\n','Parvovirus','2025-05-12 23:28:48'),(188,1,'mi perro tiene tos y fiebre','Moquillo','2025-05-13 22:28:05'),(189,1,'mi perro tiene tos','Moquillo','2025-05-14 06:02:06'),(190,1,'mi perro tiene tos','Moquillo','2025-05-14 06:08:09'),(191,1,'mi perro tienes tos y fiebre','Moquillo','2025-05-14 06:14:03'),(192,1,'mi perro tienes vomito','Parvovirus','2025-05-14 06:14:26'),(194,1,'mi perro tiene tos y fiebre','Moquillo','2025-05-15 22:59:24'),(195,1,'mi perro tiene fiebre tos','Parvovirus','2025-05-15 23:14:24'),(196,1,'mi perro tiene fiebre y tos','Parvovirus','2025-05-15 23:15:31'),(197,1,'mi perro tiene fiebre y no tos ninguno mas','migra√±a','2025-05-15 23:17:26'),(198,1,'mi perro tiene tos y fiebre ninguno mas','migra√±a','2025-05-15 23:17:57'),(199,1,'mi perro tiene tos y fiebre ninguno mas','migra√±a','2025-05-15 23:21:57'),(200,1,'mi perro tiene tos','migra√±a','2025-05-15 23:23:34'),(201,1,'mi perro tiene tos y fiebre','migra√±a','2025-05-15 23:24:01'),(202,1,'mi perro tiene tos y fiebre','Parvovirus','2025-05-15 23:26:25'),(203,1,'mi perro tiene tos','Parvovirus','2025-05-15 23:26:40'),(204,1,'mi perro tiene tos y fiebre','Parvovirus','2025-05-15 23:28:26'),(205,1,'mi perro tiene tos y fiebre','Moquillo','2025-05-15 23:30:30'),(206,1,'mi perro tiene fiebre','Moquillo','2025-05-15 23:30:49'),(207,1,'mi perro tiene vomito','Parvovirus','2025-05-15 23:31:12'),(208,1,'mi perro tiene fiebre pero no tos','Moquillo','2025-05-15 23:31:30'),(209,1,'mi perro tiene fiebre pero no tos','Parvovirus','2025-05-15 23:34:05'),(210,1,'mi perro no tiene fiebre pero si tos','Moquillo','2025-05-15 23:34:31'),(211,1,'mi perro tiene fiebre leve y tos seca','Moquillo','2025-05-15 23:34:49'),(212,1,'mi perro tiene tos seca y fiebre leve','Traqueobronquitis','2025-05-15 23:37:03'),(213,1,'mi perro tiene fiebre alta','Parvovirus','2025-05-15 23:37:24'),(214,1,'mi perro tiene estornudos','Parvovirus','2025-05-15 23:46:12'),(215,1,'mi perro tiene fiebre alta','Parvovirus','2025-05-15 23:46:47'),(216,1,'mi perro tiene estornudos','Parvovirus','2025-05-15 23:49:50'),(217,1,'mi perro tiene estornudos','Parvovirus','2025-05-15 23:52:44'),(218,1,'mi perro tiene estornudos','Parvovirus','2025-05-15 23:58:27'),(219,1,'mi perro tiene estornudos','Parvovirus','2025-05-16 00:04:27'),(221,1,'mi perro tiene estornudos','Parvovirus','2025-05-16 00:06:13'),(225,1,'mi perro tiene fiebre y tos','Moquillo','2025-05-17 05:42:30'),(226,1,'mi perro tiene tos','Moquillo','2025-05-17 05:42:40'),(227,1,'mi perro tiene tos','Moquillo','2025-05-17 05:48:40'),(228,1,'mi perro tiene fiebre pero no tos','Parvovirus','2025-05-17 05:48:55'),(229,1,'mi perro tiene vomito','Parvovirus','2025-05-17 05:49:08'),(230,1,'mi perro no tiene tos pero si fiebre','Parvovirus','2025-05-17 05:57:46'),(231,1,'mi perro tiene tos','Moquillo','2025-05-17 05:58:01'),(232,5,'mi perro tiene tos','Moquillo','2025-05-17 06:01:32'),(233,1,'mi gato tiene tos','Moquillo','2025-05-17 06:23:30'),(234,1,'mi gato tiene tos','Moquillo','2025-05-17 06:48:00'),(235,1,'mi gato tiene tos','Moquillo','2025-05-17 06:52:10'),(236,1,'mi gato tiene tos','Moquillo','2025-05-17 06:53:18'),(237,1,'mi gato tiene tos','Moquillo','2025-05-17 07:22:58'),(238,1,'mi gato tiene tos','Moquillo','2025-05-17 07:27:16');
/*!40000 ALTER TABLE `consultas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enfermedades`
--

DROP TABLE IF EXISTS `enfermedades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `enfermedades` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `sintomas` text NOT NULL,
  `tratamiento` text NOT NULL,
  `prevencion` text NOT NULL,
  `especie_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `especie_id` (`especie_id`),
  CONSTRAINT `enfermedades_ibfk_1` FOREIGN KEY (`especie_id`) REFERENCES `especies` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enfermedades`
--

LOCK TABLES `enfermedades` WRITE;
/*!40000 ALTER TABLE `enfermedades` DISABLE KEYS */;
INSERT INTO `enfermedades` VALUES (1,'Parvovirus','V√≥mito, diarrea, fiebre','Hidrataci√≥n, antivirales','Vacunaci√≥n',1),(2,'Moquillo','Fiebre, tos, secreci√≥n nasal','Suero, antibi√≥ticos','Vacunaci√≥n',1),(3,'Traqueobronquitis','Tos seca, fiebre leve','Antibi√≥ticos, antiinflamatorios','Evitar contacto con perros enfermos',1),(5,'migra√±a','dolor de cabeza','pastillas','evitar el frio',1);
/*!40000 ALTER TABLE `enfermedades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `especies`
--

DROP TABLE IF EXISTS `especies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `especies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `descripcion` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `especies`
--

LOCK TABLES `especies` WRITE;
/*!40000 ALTER TABLE `especies` DISABLE KEYS */;
INSERT INTO `especies` VALUES (1,'Canino','Perros dom√©sticos de diversas razas, caracterizados por su lealtad, sociabilidad y necesidad de ejercicio regular. Incluye razas desde peque√±os chihuahuas hasta grandes labradores.'),(2,'Felino','Gatos dom√©sticos conocidos por su independencia, agilidad y adaptabilidad. Comprende razas variadas, desde siameses hasta persas, y son excelentes compa√±eros en el hogar.');
/*!40000 ALTER TABLE `especies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feedback` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) NOT NULL,
  `comentario` text DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
INSERT INTO `feedback` VALUES (1,1,'buena aplicacion',5,'2025-04-11 15:06:34'),(2,1,'necesita mejorar',3,'2025-05-13 05:58:05'),(3,1,'esta bien',4,'2025-05-14 11:17:07');
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varbinary(255) NOT NULL,
  `email` varbinary(255) NOT NULL,
  `rol` varbinary(50) NOT NULL,
  `password` varbinary(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Ó€ﬁ√$/‚ﬁ™Ä™Kãw','_ã¬¢œìS˘Z\"ÇZ@Q˝≠@Íˇ96ËîYÁöL\'®Z','Óó+d\"Ä¨ oc@í8Q','ÏótØ•v—Hzûm]≈úZ'),(2,'[3ekí$˛Ÿ¿Û ’Z¿8ê','$àìôIÚöPx[;˘êä•üÕ≥=5M§ﬂ”G‰ï  ','ΩøQK⁄”aÚBŒ@—≤i','a	∂ò(B0˛˚P&»\0Ô'),(5,'.hÂ¯|å:–]‚a3¶Ü','[◊ íµ8B3ëuÌ—+˝≠@Íˇ96ËîYÁöL\'®Z','z·J`S Çàm5„ìúA','\rè˝Ì¥tßYïöZ≠	™M');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `set_default_rol` BEFORE INSERT ON `usuarios` FOR EACH ROW BEGIN
    IF NEW.rol IS NULL OR NEW.rol = '' THEN
        SET NEW.rol = AES_ENCRYPT('estudiante', 'mi_clave_secreta');
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-23 22:07:41
