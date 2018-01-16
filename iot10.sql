-- MySQL dump 10.13  Distrib 5.7.20, for Linux (x86_64)
--
-- Host: localhost    Database: iot10
-- ------------------------------------------------------
-- Server version	5.7.20-0ubuntu0.16.04.1

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permission_group_id_689710a9a73b7457_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `auth__content_type_id_508cf46651277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(22,'Can add user',8,'add_user'),(23,'Can change user',8,'change_user'),(24,'Can delete user',8,'delete_user'),(25,'Can add role',9,'add_role'),(26,'Can change role',9,'change_role'),(27,'Can delete role',9,'delete_role'),(28,'Can add permissions',10,'add_permissions'),(29,'Can change permissions',10,'change_permissions'),(30,'Can delete permissions',10,'delete_permissions'),(31,'Can add permissions group',11,'add_permissionsgroup'),(32,'Can change permissions group',11,'change_permissionsgroup'),(33,'Can delete permissions group',11,'delete_permissionsgroup'),(34,'Can add iot medicine',12,'add_iotmedicine'),(35,'Can change iot medicine',12,'change_iotmedicine'),(36,'Can delete iot medicine',12,'delete_iotmedicine'),(37,'Can add message',13,'add_message'),(38,'Can change message',13,'change_message'),(39,'Can delete message',13,'delete_message'),(40,'Can add iot device',14,'add_iotdevice'),(41,'Can change iot device',14,'change_iotdevice'),(42,'Can delete iot device',14,'delete_iotdevice'),(46,'Can add company profile',16,'add_companyprofile'),(47,'Can change company profile',16,'change_companyprofile'),(48,'Can delete company profile',16,'delete_companyprofile'),(49,'Can add device profile',17,'add_deviceprofile'),(50,'Can change device profile',17,'change_deviceprofile'),(51,'Can delete device profile',17,'delete_deviceprofile'),(52,'Can add device',18,'add_device'),(53,'Can change device',18,'change_device'),(54,'Can delete device',18,'delete_device'),(55,'Can add custom fields',19,'add_customfields'),(56,'Can change custom fields',19,'change_customfields'),(57,'Can delete custom fields',19,'delete_customfields');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$20000$H15BwVvog3Qf$7k3tjHZ+g+94AWSb34fHkBJOrBP+Ksb/mSQoK09NQ48=','2018-01-06 01:36:50.466484',1,'admin','','','969766927@qq.com',1,1,'2018-01-06 01:36:34.851065');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissi_user_id_7f0938558328534a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_customfields`
--

DROP TABLE IF EXISTS `device_customfields`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device_customfields` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` varchar(521) NOT NULL,
  `type` int(11) NOT NULL,
  `device_id` int(11),
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_customfields`
--

LOCK TABLES `device_customfields` WRITE;
/*!40000 ALTER TABLE `device_customfields` DISABLE KEYS */;
/*!40000 ALTER TABLE `device_customfields` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_iotdevice`
--

DROP TABLE IF EXISTS `device_iotdevice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device_iotdevice` (
  `device_id` int(11) NOT NULL AUTO_INCREMENT,
  `SN` varchar(32) DEFAULT NULL,
  `mac_addr` varchar(32) NOT NULL,
  `serial_num` varchar(32) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `activation` smallint(6) NOT NULL,
  `state` smallint(6) NOT NULL,
  `time_registered` datetime(6),
  PRIMARY KEY (`device_id`),
  UNIQUE KEY `mac_addr` (`mac_addr`),
  UNIQUE KEY `SN` (`SN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_iotdevice`
--

LOCK TABLES `device_iotdevice` WRITE;
/*!40000 ALTER TABLE `device_iotdevice` DISABLE KEYS */;
/*!40000 ALTER TABLE `device_iotdevice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_iotdevice_user_has`
--

DROP TABLE IF EXISTS `device_iotdevice_user_has`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device_iotdevice_user_has` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `iotdevice_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `iotdevice_id` (`iotdevice_id`,`user_id`),
  KEY `device_iotdevice_user__user_id_5a3d3494edb204fa_fk_users_user_id` (`user_id`),
  CONSTRAINT `devi_iotdevice_id_26fd56b95e3eafe4_fk_device_iotdevice_device_id` FOREIGN KEY (`iotdevice_id`) REFERENCES `device_iotdevice` (`device_id`),
  CONSTRAINT `device_iotdevice_user__user_id_5a3d3494edb204fa_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_iotdevice_user_has`
--

LOCK TABLES `device_iotdevice_user_has` WRITE;
/*!40000 ALTER TABLE `device_iotdevice_user_has` DISABLE KEYS */;
/*!40000 ALTER TABLE `device_iotdevice_user_has` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_profiles`
--

DROP TABLE IF EXISTS `device_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device_profiles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `device_field` varchar(32) NOT NULL,
  `description` varchar(521) NOT NULL,
  `high_temperature` varchar(32) NOT NULL,
  `low_temperature` varchar(32) NOT NULL,
  `delayed` int(11) DEFAULT NULL,
  `record_interval` int(11) DEFAULT NULL,
  `create_time` datetime(6) NOT NULL,
  `profiles_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `profiles_id` (`profiles_id`),
  CONSTRAINT `devic_profiles_id_36c79e6201913d20_fk_device_iotdevice_device_id` FOREIGN KEY (`profiles_id`) REFERENCES `device_iotdevice` (`device_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_profiles`
--

LOCK TABLES `device_profiles` WRITE;
/*!40000 ALTER TABLE `device_profiles` DISABLE KEYS */;
/*!40000 ALTER TABLE `device_profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `djang_content_type_id_697914295151027a_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` (`user_id`),
  CONSTRAINT `djang_content_type_id_697914295151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2018-01-06 05:55:41.957622','2','iot',1,'',16,1),(2,'2018-01-06 06:04:18.658867','1','admin',1,'',8,1),(3,'2018-01-06 06:07:03.614819','3','发货',1,'',9,1),(4,'2018-01-06 06:08:40.453553','4','收货',1,'',9,1),(5,'2018-01-06 06:10:58.972232','5','发货和收货',1,'',9,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_45f3b1d93ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(19,'device','customfields'),(18,'device','device'),(17,'device','deviceprofile'),(14,'device','iotdevice'),(6,'sessions','session'),(16,'users','companyprofile'),(12,'users','iotmedicine'),(13,'users','message'),(10,'users','permissions'),(11,'users','permissionsgroup'),(9,'users','role'),(8,'users','user');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2017-12-29 08:38:04.623450'),(2,'auth','0001_initial','2017-12-29 08:38:13.113235'),(3,'admin','0001_initial','2017-12-29 08:38:13.845509'),(4,'contenttypes','0002_remove_content_type_name','2017-12-29 08:38:14.514496'),(5,'auth','0002_alter_permission_name_max_length','2017-12-29 08:38:15.359953'),(6,'auth','0003_alter_user_email_max_length','2017-12-29 08:38:15.683203'),(7,'auth','0004_alter_user_username_opts','2017-12-29 08:38:15.726783'),(8,'auth','0005_alter_user_last_login_null','2017-12-29 08:38:16.018649'),(9,'auth','0006_require_contenttypes_0002','2017-12-29 08:38:16.075477'),(10,'users','0001_initial','2017-12-29 08:38:20.806577'),(11,'device','0001_initial','2017-12-29 08:38:21.584852'),(12,'sessions','0001_initial','2017-12-29 08:38:21.977536'),(13,'device','0002_auto_20180106_0205','2018-01-06 02:05:38.636356'),(14,'users','0002_auto_20180106_0558','2018-01-06 05:58:19.046428'),(15,'users','0003_auto_20180106_0600','2018-01-06 06:00:33.473236'),(16,'device','0002_auto_20180106_0631','2018-01-06 06:31:55.529176'),(17,'admin','0002_logentry_remove_auto_add','2018-01-08 07:25:55.461469'),(18,'auth','0007_alter_validators_add_error_messages','2018-01-08 07:25:55.654169');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('vwvrn5n85qvznibygmwb3iixz1oa1aly','MGE5OTQ5ZjY3YWVlMzYyZDk3Y2I2ODJkZDM0ODRiZDRkNDdmOGY3ODp7Il9hdXRoX3VzZXJfaGFzaCI6IjI4ZGFhOTcyMTIzMWI2MWFkMDFjZGZmMzE3NzY0YzQxOGEzNmZmNGYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2018-01-20 01:36:51.039293');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_companyprofile`
--

DROP TABLE IF EXISTS `users_companyprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_companyprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `company` varchar(64) NOT NULL,
  `street` varchar(64) NOT NULL,
  `postal_code` varchar(64) NOT NULL,
  `city` varchar(512) NOT NULL,
  `Image` varchar(100) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_companyprofile`
--

LOCK TABLES `users_companyprofile` WRITE;
/*!40000 ALTER TABLE `users_companyprofile` DISABLE KEYS */;
INSERT INTO `users_companyprofile` VALUES (2,'iot','','','','','2018-01-06 05:55:41.851784');
/*!40000 ALTER TABLE `users_companyprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_iotmedicine`
--

DROP TABLE IF EXISTS `users_iotmedicine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_iotmedicine` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `company` varchar(64) NOT NULL,
  `secret_key` varchar(64) NOT NULL,
  `time` datetime(6) NOT NULL,
  `bundle_id` varchar(64) NOT NULL,
  `package_name` varchar(64) NOT NULL,
  `type` int(11) NOT NULL,
  `app_id` varchar(64) NOT NULL,
  `token` varchar(64) NOT NULL,
  `description` varchar(512) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_iotmedicine`
--

LOCK TABLES `users_iotmedicine` WRITE;
/*!40000 ALTER TABLE `users_iotmedicine` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_iotmedicine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_message`
--

DROP TABLE IF EXISTS `users_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login_time` datetime(6) NOT NULL,
  `username` varchar(32) DEFAULT NULL,
  `message` varchar(64) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `users_message_e8701ad4` (`user_id`),
  CONSTRAINT `users_message_user_id_12509171c667ea96_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_message`
--

LOCK TABLES `users_message` WRITE;
/*!40000 ALTER TABLE `users_message` DISABLE KEYS */;
INSERT INTO `users_message` VALUES (1,'2017-12-27 02:56:02.196362','admin','admin has login in',NULL),(2,'2017-12-27 02:59:05.448587','admin','admin has login in',NULL),(3,'2017-12-27 08:23:13.251539','admin','admin has login in',NULL),(4,'2017-12-27 08:36:58.283435','admin','admin has login in',NULL),(5,'2017-12-27 08:38:58.290585','admin','admin has login in',NULL),(6,'2017-12-27 08:59:33.385268','admin','admin has login in',NULL),(7,'2017-12-27 09:02:27.654580','admin','admin has login in',NULL),(8,'2017-12-27 09:37:01.701104','admin','admin has login in',NULL),(9,'2017-12-27 10:26:17.567174','admin','admin has login in',NULL),(10,'2017-12-27 11:00:24.172549','admin','admin has login in',NULL),(11,'2017-12-27 11:02:37.024030','admin','admin has login in',NULL),(12,'2017-12-28 02:15:10.463511','admin','admin has login in',NULL),(13,'2017-12-28 03:04:47.223091','admin','admin has login in',NULL);
/*!40000 ALTER TABLE `users_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_permissions`
--

DROP TABLE IF EXISTS `users_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(128) NOT NULL,
  `code` varchar(16) NOT NULL,
  `name` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_permissions`
--

LOCK TABLES `users_permissions` WRITE;
/*!40000 ALTER TABLE `users_permissions` DISABLE KEYS */;
INSERT INTO `users_permissions` VALUES (2,'/users/add/','add','增加用户'),(3,'/users/delete/','delete','删除用户'),(4,'/users/update/','update','修改用户'),(5,'/users/get/','get','查看用户'),(6,'/event/post/','/event/post/','event'),(7,'/express/get_count_bymonth/','month','month'),(8,'/express/get_latest/','latest','latest'),(9,'/express/register/','register','register'),(10,'/order/register/','register','新建订单'),(11,'/order/update/','update','修改订单'),(12,'/order/get/','get','获取订单'),(13,'/order/time/','time','获取订单时间'),(14,'/order/in_delivery/','send','已发货订单'),(15,'/order/created_today','created_today','created_today'),(16,'/order/delivered_today','delivered_today','今日已发货'),(17,'/temperature/post/','post','post'),(18,'/temperature/delete/','delete','delete'),(19,'/temperature/get/','get','get'),(20,'/temperature/get_compressed/','get_compressed','get_compressed'),(21,'/temperature/get_seq/','get_seq','get_seq'),(22,'/device/register/','register','新建设备'),(23,'/device/get/','get','获取设备列表'),(24,'/device/update/','update','修改设备'),(25,'/users/get_groups/','get_groups','权限组列表'),(26,'users/get_roles/','get_roles','get_roles'),(27,'users/add_roles/','add_roles','add_roles'),(28,'users/add_roles/','add_roles','add_roles'),(29,'users/profile','profile','profile'),(30,'users/edit_profile/','edit_profile','edit_profile');
/*!40000 ALTER TABLE `users_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_permissionsgroup`
--

DROP TABLE IF EXISTS `users_permissionsgroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_permissionsgroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL,
  `is_show` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_permissionsgroup`
--

LOCK TABLES `users_permissionsgroup` WRITE;
/*!40000 ALTER TABLE `users_permissionsgroup` DISABLE KEYS */;
INSERT INTO `users_permissionsgroup` VALUES (1,'manager user',1),(2,'event',1),(3,'manager device',1),(4,'order ',1),(5,' get device',1),(6,'权限组列表',1),(7,'get_groups',1),(8,'profile',1);
/*!40000 ALTER TABLE `users_permissionsgroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_permissionsgroup_permissions`
--

DROP TABLE IF EXISTS `users_permissionsgroup_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_permissionsgroup_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `permissionsgroup_id` int(11) NOT NULL,
  `permissions_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `permissionsgroup_id` (`permissionsgroup_id`,`permissions_id`),
  KEY `users_pe_permissions_id_69dc0198696fee70_fk_users_permissions_id` (`permissions_id`),
  CONSTRAINT `D1f9afd08afae19f055a7a9cbfc5b0bd` FOREIGN KEY (`permissionsgroup_id`) REFERENCES `users_permissionsgroup` (`id`),
  CONSTRAINT `users_pe_permissions_id_69dc0198696fee70_fk_users_permissions_id` FOREIGN KEY (`permissions_id`) REFERENCES `users_permissions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_permissionsgroup_permissions`
--

LOCK TABLES `users_permissionsgroup_permissions` WRITE;
/*!40000 ALTER TABLE `users_permissionsgroup_permissions` DISABLE KEYS */;
INSERT INTO `users_permissionsgroup_permissions` VALUES (2,1,2),(3,1,3),(4,1,4),(5,2,5),(6,3,21),(7,3,22),(8,3,23),(9,4,9),(10,4,10),(11,4,11),(12,4,12),(13,4,13),(14,4,14),(15,4,15),(16,5,22),(17,5,23),(19,7,25),(20,8,29),(21,8,30);
/*!40000 ALTER TABLE `users_permissionsgroup_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_role`
--

DROP TABLE IF EXISTS `users_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role` varchar(32) NOT NULL,
  `is_show` tinyint(1) NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_role`
--

LOCK TABLES `users_role` WRITE;
/*!40000 ALTER TABLE `users_role` DISABLE KEYS */;
INSERT INTO `users_role` VALUES (1,'administrator',1,NULL),(2,'manager',1,NULL),(3,'发货',1,'2018-01-06 06:07:03.375562'),(4,'收货',1,'2018-01-06 06:08:40.146322'),(5,'发货和收货',1,'2018-01-06 06:10:58.948512');
/*!40000 ALTER TABLE `users_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_role_groups`
--

DROP TABLE IF EXISTS `users_role_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_role_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) NOT NULL,
  `permissionsgroup_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `role_id` (`role_id`,`permissionsgroup_id`),
  KEY `D56f5a9c81f8e3c4cbd5e64dca40e9de` (`permissionsgroup_id`),
  CONSTRAINT `D56f5a9c81f8e3c4cbd5e64dca40e9de` FOREIGN KEY (`permissionsgroup_id`) REFERENCES `users_permissionsgroup` (`id`),
  CONSTRAINT `users_role_groups_role_id_373d3b5b455b6473_fk_users_role_id` FOREIGN KEY (`role_id`) REFERENCES `users_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_role_groups`
--

LOCK TABLES `users_role_groups` WRITE;
/*!40000 ALTER TABLE `users_role_groups` DISABLE KEYS */;
INSERT INTO `users_role_groups` VALUES (16,1,1),(17,1,2),(18,1,3),(19,1,4),(20,1,5),(21,1,6),(22,1,7),(23,1,8),(7,2,2),(8,2,4),(9,2,5),(24,3,2),(25,3,3),(26,3,4),(27,3,5),(28,3,7),(29,3,8),(30,4,5),(31,5,2),(32,5,3),(33,5,4),(34,5,5),(35,5,6),(36,5,7),(37,5,8);
/*!40000 ALTER TABLE `users_role_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user`
--

DROP TABLE IF EXISTS `users_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(32) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL,
  `email` varchar(32) DEFAULT NULL,
  `is_lock` tinyint(1) NOT NULL,
  `temperature_unit` smallint(6) DEFAULT NULL,
  `note` varchar(512) DEFAULT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `iotprofile_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user`
--

LOCK TABLES `users_user` WRITE;
/*!40000 ALTER TABLE `users_user` DISABLE KEYS */;
INSERT INTO `users_user` VALUES (1,'admin','1234','123@qq.com',0,NULL,'18510234326','2018-01-06 06:04:18.341575',2);
/*!40000 ALTER TABLE `users_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user_role`
--

DROP TABLE IF EXISTS `users_user_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_user_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`role_id`),
  KEY `users_user_role_role_id_66d018d0baed46bc_fk_users_role_id` (`role_id`),
  CONSTRAINT `users_user_role_role_id_66d018d0baed46bc_fk_users_role_id` FOREIGN KEY (`role_id`) REFERENCES `users_role` (`id`),
  CONSTRAINT `users_user_role_user_id_32b944f8c0a3dabf_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_role`
--

LOCK TABLES `users_user_role` WRITE;
/*!40000 ALTER TABLE `users_user_role` DISABLE KEYS */;
INSERT INTO `users_user_role` VALUES (8,1,1),(7,2,2),(5,3,2);
/*!40000 ALTER TABLE `users_user_role` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-01-08 17:49:48
