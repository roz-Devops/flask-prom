CREATE TABLE IF NOT EXISTS `colors` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `color` varchar(30) NOT NULL DEFAULT '',
  `color_type` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
);

INSERT INTO colors ( `id`, `color` , `color_type` )
VALUES (1,'red','primary'),
       (2,'black','basic'),
       (3,'blue','primary'),
       (4,'purple','basic'),
       (5,'yellow','primary');
