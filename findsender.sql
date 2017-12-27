SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `c`
-- ----------------------------
DROP TABLE IF EXISTS `c`;
CREATE TABLE `c` (
  `c` char(255) NOT NULL DEFAULT '',
  `times` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`c`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of c
-- ----------------------------

-- ----------------------------
-- Table structure for `cf`
-- ----------------------------
DROP TABLE IF EXISTS `cf`;
CREATE TABLE `cf` (
  `c` char(255) NOT NULL DEFAULT '',
  `f` char(255) NOT NULL DEFAULT '',
  `times` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`c`,`f`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of cf
-- ----------------------------

-- ----------------------------
-- Table structure for `fc`
-- ----------------------------
DROP TABLE IF EXISTS `fc`;
CREATE TABLE `fc` (
  `c` char(255) NOT NULL DEFAULT '',
  `times` int(32) NOT NULL DEFAULT '0',
  PRIMARY KEY (`c`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of fc
-- ----------------------------
