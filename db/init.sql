CREATE TABLE `ItemsProcesados` (
  `id` int NOT NULL AUTO_INCREMENT,
  `site` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `siteID` int NOT NULL,
  `price` double DEFAULT NULL,
  `start_time` varchar(30) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `description` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `nickname` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `ItemsRechazados` (
  `id` int NOT NULL AUTO_INCREMENT,
  `siteID` varchar(30) DEFAULT NULL,
  `comentario` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `fecha_proceso` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;



