CREATE DATABASE  IF NOT EXISTS `pokedex` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `pokedex`;
-- MySQL dump 10.13  Distrib 5.7.12, for osx10.9 (x86_64)
--
-- Host: 127.0.0.1    Database: pokedex
-- ------------------------------------------------------
-- Server version	5.5.5-10.1.13-MariaDB

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
-- Table structure for table `player_pokemon`
--

DROP TABLE IF EXISTS `player_pokemon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `player_pokemon` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `player_login` varchar(20) NOT NULL,
  `pokemon_name` varchar(20) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_login_name` (`player_login`,`name`),
  KEY `fk_player_pokemon_1_idx` (`player_login`),
  KEY `fk_player_pokemon_2_idx` (`pokemon_name`),
  CONSTRAINT `fk_player_pokemon_1` FOREIGN KEY (`player_login`) REFERENCES `players` (`login`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_player_pokemon_2` FOREIGN KEY (`pokemon_name`) REFERENCES `pokemons` (`name`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `player_pokemon`
--

LOCK TABLES `player_pokemon` WRITE;
/*!40000 ALTER TABLE `player_pokemon` DISABLE KEYS */;
/*!40000 ALTER TABLE `player_pokemon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `players`
--

DROP TABLE IF EXISTS `players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `players` (
  `login` varchar(20) NOT NULL,
  `password` char(128) NOT NULL,
  `token` char(64) NOT NULL,
  `pokebolls` smallint(6) NOT NULL DEFAULT '100',
  `experience` smallint(6) NOT NULL DEFAULT '0',
  `level` tinyint(4) NOT NULL DEFAULT '1',
  PRIMARY KEY (`login`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `players`
--

LOCK TABLES `players` WRITE;
/*!40000 ALTER TABLE `players` DISABLE KEYS */;
/*!40000 ALTER TABLE `players` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pokemon_type`
--

DROP TABLE IF EXISTS `pokemon_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pokemon_type` (
  `pokemon_name` varchar(20) NOT NULL,
  `type_name` varchar(20) NOT NULL,
  PRIMARY KEY (`pokemon_name`,`type_name`),
  KEY `fk_pokemon_type_2_idx` (`type_name`),
  CONSTRAINT `fk_pokemon_type_1` FOREIGN KEY (`pokemon_name`) REFERENCES `pokemons` (`name`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_pokemon_type_2` FOREIGN KEY (`type_name`) REFERENCES `types` (`name`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pokemon_type`
--

LOCK TABLES `pokemon_type` WRITE;
/*!40000 ALTER TABLE `pokemon_type` DISABLE KEYS */;
INSERT INTO `pokemon_type` VALUES ('Bulbasaur','Grass'),('Bulbasaur','Poison'),('Butterfree','Flying'),('Caterpie','Bug'),('Charizard','Flying'),('Charmander','Fire'),('Ekans','Poison'),('Nidoran','Poison'),('Pidgey','Flying'),('Pidgey','Normal'),('Pikachu','Electric'),('Rattata','Normal'),('Sandshrew','Ground'),('Spearow','Flying'),('Spearow','Normal'),('Squirtle','Water'),('Vulpix','Fire'),('Weedle','Bug'),('Weedle','Poison'),('Zubat','Flying'),('Zubat','Poison');
/*!40000 ALTER TABLE `pokemon_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pokemons`
--

DROP TABLE IF EXISTS `pokemons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pokemons` (
  `name` varchar(20) NOT NULL,
  `category` varchar(20) NOT NULL,
  `rarity` enum('very common','common','uncommon','rare','very rare','special','epic','legendary') NOT NULL,
  `ability` varchar(20) NOT NULL,
  `evolves_from` varchar(20) DEFAULT NULL,
  `hp` tinyint(4) NOT NULL,
  `attack` tinyint(4) NOT NULL,
  `defense` tinyint(4) NOT NULL,
  `special_attack` tinyint(4) NOT NULL,
  `special_defense` tinyint(4) NOT NULL,
  `speed` tinyint(4) NOT NULL,
  PRIMARY KEY (`name`),
  KEY `fk_pokemons_1_idx` (`evolves_from`),
  CONSTRAINT `fk_pokemons_1` FOREIGN KEY (`evolves_from`) REFERENCES `pokemons` (`name`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pokemons`
--

LOCK TABLES `pokemons` WRITE;
/*!40000 ALTER TABLE `pokemons` DISABLE KEYS */;
INSERT INTO `pokemons` VALUES ('Arbok','Cobra','common','Shed Skin','Ekans',3,4,3,3,3,4),('Beedrill','Poison Bee','rare','Swarm','Kakuna',3,5,2,2,3,4),('Blastoise','Shellfish','epic','Torrent','Wartortle',3,4,4,4,4,4),('Bulbasaur','Seed','common','Overgrow','Egg',2,3,2,3,3,3),('Butterfree','Butterfly','uncommon','Compound Eyes','Metapod',3,2,2,4,3,4),('Caterpie','Worm','very common','Shield Dust','Egg',2,2,2,1,1,3),('Charizard','Flame','epic','Blaze','Charmeleon',3,4,3,5,4,5),('Charmander','Lizard','common','Blaze','Egg',2,3,2,3,2,3),('Charmeleon','Flame','special','Blaze','Charmander',3,3,3,4,3,4),('Egg','None','','None',NULL,0,0,0,0,0,0),('Ekans','Snake','very common','Shed Skin','Egg',2,3,2,2,2,3),('Fearow','Beak','uncommon','Keen Eye','Spearow',3,5,3,3,3,5),('Golbat','Bat','common','Inner Focus','Zubat',3,4,3,3,3,5),('Ivysaur','Seed','special','Overgrow','Bulbasaur',3,3,3,4,3,3),('Kakuna','Cocoon','common','Shed Skin','Weedle',2,1,2,1,1,2),('Metapod','Cocoon','common','Shed Skin','Caterpie',2,1,3,1,1,2),('Nidoran','Poison Pin','very common','Poison Pin','Egg',2,3,2,2,2,2),('Nidorina','Poison Pin','uncommon','Poison Point','Nidoran',3,3,3,3,2,3),('Ninetales','Fox','uncommon','Flash Fire','Vulpix',3,4,3,4,4,5),('Pidgeot','Bird','rare','Keen Eye','Pidgeotto',3,4,3,3,3,5),('Pidgeotto','Bird','common','Keen Eye','Pidgey',3,3,3,2,2,4),('Pidgey','Tiny Bird','very common','Keen Eye','Egg',2,2,2,2,2,3),('Pikachu','Mouse','common','Static','Egg',2,3,2,2,2,5),('Raichu','Mouse','very rare','Static','Pikachu',3,5,3,4,3,5),('Raticate','Mouse','common','Run Away','Rattata',2,4,3,2,3,5),('Rattata','Mouse','very common','Run Away','Egg',2,3,2,1,2,3),('Sandshrew','Mouse','very common','Sand Veil','Egg',2,4,4,1,1,2),('Sandslash','Mouse','common','Sand Veil','Sandshrew',3,5,5,2,2,4),('Spearow','Tiny Bird','common','Keen Eye','Egg',2,3,2,2,1,4),('Squirtle','Tiny Turtle','common','Torrent','Egg',2,3,3,2,3,2),('Venusaur','Seed','epic','Overgrow','Ivysaur',3,4,4,5,4,4),('Vulpix','Fox','common','Flash Fire','Egg',2,2,2,2,3,4),('Wartortle','Turtle','special','Torrent','Squirtle',3,3,4,3,3,3),('Weedle','Hairy Bug','very common','Shield Dust','Egg',2,2,2,1,1,3),('Zubat','Bat','very common','Inner Focus','Egg',2,2,2,1,2,3);
/*!40000 ALTER TABLE `pokemons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `settings`
--

DROP TABLE IF EXISTS `settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `settings` (
  `name` varchar(20) NOT NULL,
  `value` varchar(20) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `settings`
--

LOCK TABLES `settings` WRITE;
/*!40000 ALTER TABLE `settings` DISABLE KEYS */;
/*!40000 ALTER TABLE `settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `type_damage`
--

DROP TABLE IF EXISTS `type_damage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `type_damage` (
  `attacking_type` varchar(20) NOT NULL,
  `defending_type` varchar(20) NOT NULL,
  `damage_multiplier` float(2,1) NOT NULL,
  PRIMARY KEY (`attacking_type`,`defending_type`),
  KEY `fk_type_weakness_2_idx` (`defending_type`),
  CONSTRAINT `fk_type_weakness_1` FOREIGN KEY (`attacking_type`) REFERENCES `types` (`name`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_type_weakness_2` FOREIGN KEY (`defending_type`) REFERENCES `types` (`name`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `type_damage`
--

LOCK TABLES `type_damage` WRITE;
/*!40000 ALTER TABLE `type_damage` DISABLE KEYS */;
INSERT INTO `type_damage` VALUES ('Bug','Dark',2.0),('Bug','Fairy',0.5),('Bug','Fire',0.5),('Bug','Flying',0.5),('Bug','Ghost',0.5),('Bug','Grass',2.0),('Bug','Poison',0.5),('Bug','Psychic',2.0),('Bug','Steel',0.5),('Electric','Dragon',0.5),('Electric','Electric',0.5),('Electric','Flying',2.0),('Electric','Grass',0.5),('Electric','Ground',0.0),('Electric','Water',2.0),('Fire','Bug',2.0),('Fire','Dragon',0.5),('Fire','Fire',0.5),('Fire','Grass',2.0),('Fire','Ice',2.0),('Fire','Rock',0.5),('Fire','Steel',2.0),('Fire','Water',0.5),('Flying','Bug',2.0),('Flying','Electric',0.5),('Flying','Fighting',2.0),('Flying','Grass',2.0),('Flying','Rock',0.5),('Flying','Steel',0.5),('Grass','Bug',0.5),('Grass','Dragon',0.5),('Grass','Fire',0.5),('Grass','Flying',0.5),('Grass','Grass',0.5),('Grass','Ground',2.0),('Grass','Poison',0.5),('Grass','Rock',2.0),('Grass','Steel',0.5),('Grass','Water',2.0),('Ground','Bug',0.5),('Ground','Electric',2.0),('Ground','Fire',2.0),('Ground','Flying',0.0),('Ground','Grass',0.5),('Ground','Poison',2.0),('Ground','Rock',2.0),('Ground','Steel',2.0),('Normal','Ghost',0.0),('Normal','Rock',0.5),('Normal','Steel',0.5),('Poison','Fairy',2.0),('Poison','Ghost',0.5),('Poison','Grass',2.0),('Poison','Ground',0.5),('Poison','Poison',0.5),('Poison','Rock',0.5),('Poison','Steel',0.0),('Water','Dragon',0.5),('Water','Fire',2.0),('Water','Grass',0.5),('Water','Ground',2.0),('Water','Rock',2.0),('Water','Water',0.5);
/*!40000 ALTER TABLE `type_damage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `types`
--

DROP TABLE IF EXISTS `types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `types` (
  `name` varchar(20) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `types`
--

LOCK TABLES `types` WRITE;
/*!40000 ALTER TABLE `types` DISABLE KEYS */;
INSERT INTO `types` VALUES ('Bug'),('Dark'),('Dragon'),('Electric'),('Fairy'),('Fighting'),('Fire'),('Flying'),('Ghost'),('Grass'),('Ground'),('Ice'),('Normal'),('Poison'),('Psychic'),('Rock'),('Steel'),('Water');
/*!40000 ALTER TABLE `types` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-09 23:45:32
