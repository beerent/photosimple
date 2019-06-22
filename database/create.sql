CREATE TABLE `directories` (
	  `id` int(11) NOT NULL AUTO_INCREMENT,
	  `directory_name` varchar(200) NOT NULL,
	  `directory_path` varchar(200) NOT NULL,
	  `directory_type` varchar(11) NOT NULL,
	  `active` varchar(1) NOT NULL DEFAULT '1',
	  `root` varchar(1) NOT NULL DEFAULT '0',
	  PRIMARY KEY (`id`),
	  UNIQUE KEY `directory_path_UNIQUE` (`directory_path`,`directory_type`)
) ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE `photos` (
	  `id` int(11) NOT NULL AUTO_INCREMENT,
	  `file_name` varchar(100) NOT NULL,
	  `sub_directory` varchar(12) NOT NULL,
	  `hash` varchar(40) DEFAULT NULL,
	  `source` int(11) NOT NULL,
	  `added` datetime NOT NULL,
	  `modified` datetime NOT NULL,
	  PRIMARY KEY (`id`),
	  UNIQUE KEY `hash_UNIQUE` (`hash`),
	  KEY `source_fk_idx` (`source`),
	  CONSTRAINT `source_fk` FOREIGN KEY (`source`) REFERENCES `directories` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB CHARSET=utf8;
