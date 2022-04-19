CREATE TABLE `music` (
  `musicID` INT NOT NULL AUTO_INCREMENT,
  `catalogueNo` VARCHAR(45) NOT NULL,
  `categoryID` INT NOT NULL ,
  `title` VARCHAR(255) NOT NULL,
  `composer` VARCHAR(255) NULL,
  `arranger` VARCHAR(255) NULL,
  `publisher` VARCHAR(255) NULL,
  `featuredInstrument` VARCHAR(255) NULL,
  `ensembleID` INT NULL,
  `parts` VARCHAR(255) NULL,
  `remarks` VARCHAR(255) NULL,
  PRIMARY KEY (`musicID`),
  UNIQUE INDEX `catalogueNo_UNIQUE` (`catalogueNo` ASC));


CREATE TABLE `category` (
  `categoryID` INT NOT NULL,
  `category` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`categoryID`),
  UNIQUE INDEX `categoryID_UNIQUE` (`categoryID` ASC),
  UNIQUE INDEX `category_UNIQUE` (`category` ASC));



CREATE TABLE `ensemble` (
  `ensembleID` INT NOT NULL,
  `ensemble` VARCHAR(15) NOT NULL,
  PRIMARY KEY (`ensembleID`),
  UNIQUE INDEX `ensembleID_UNIQUE` (`ensembleID` ASC));


/* foreign keys init */
ALTER TABLE `music` ALTER INDEX `ensembleID_idx` VISIBLE;
ALTER TABLE `music` 
ADD CONSTRAINT `ensembleID`
  FOREIGN KEY (`ensembleID`)
  REFERENCES `ensemble` (`ensembleID`)
  ON DELETE RESTRICT
  ON UPDATE CASCADE;

ALTER TABLE `music` 
ADD INDEX `categoryID_idx` (`categoryID` ASC) VISIBLE;
;
ALTER TABLE `music` 
ADD CONSTRAINT `categoryID`
  FOREIGN KEY (`categoryID`)
  REFERENCES `category` (`categoryID`)
  ON DELETE RESTRICT
  ON UPDATE CASCADE;



/* Data init */
INSERT INTO `ensemble` (`ensembleID`, `ensemble`) VALUES ('1', 'Concert Band');
INSERT INTO `ensemble` (`ensembleID`, `ensemble`) VALUES ('2', 'Marching Band');
INSERT INTO `ensemble` (`ensembleID`, `ensemble`) VALUES ('3', 'Solo');
INSERT INTO `ensemble` (`ensembleID`, `ensemble`) VALUES ('4', 'Ensemble');
INSERT INTO `ensemble` (`ensembleID`, `ensemble`) VALUES ('5', 'Big Band');
INSERT INTO `ensemble` (`ensembleID`, `ensemble`) VALUES ('6', 'Study');
INSERT INTO `ensemble` (`ensembleID`, `ensemble`) VALUES ('7', 'Reference');
INSERT INTO `ensemble` (`ensembleID`, `ensemble`) VALUES ('8', 'Others');


INSERT INTO `category` (`categoryID`, `category`) VALUES ('00', 'NON-PUBLISHED');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('10', 'WIND BAND');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('11', 'WIND BAND (A5)');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('12', 'CEREMONIAL MUSIC');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('13', 'FOREIGN ANTHEM');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('14', 'WIND BAND TRAINING');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('20', 'FLUTE');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('21', 'OBOE');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('22', 'COR ANGLAIS');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('23', 'BASSOON');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('24', 'CLARINET');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('25', 'SAXOPHONE');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('30', 'HORN');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('31', 'TRUMPET');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('32', 'TROMBONE');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('33', 'EUPHONIUM');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('34', 'TUBA');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('40', 'STRINGS');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('41', 'PIANO');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('42', 'HARP/GUITAR');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('50', 'PERCUSSION');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('60', 'RECORDER');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('61', 'VOCAL');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('70', 'WOODWIND ENSEMBLE');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('71', 'BRASS ENSEMBLE');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('72', 'MIXED ENSEMBLE');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('73', 'FLEXIBLE ENSEMBLE');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('74', 'BIG BAND');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('80', 'REFERENCE');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('81', 'THEORY PAPERS G5');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('82', 'THEORY PAPERS G6');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('83', 'THEORY PAPERS G7');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('84', 'THEORY PAPERS G8');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('85', 'THEORY MATERIAL');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('86', 'AURAL MATERIAL');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('90', 'WIND BAND/ORCH DISC');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('91', 'INSTRUMENT/CHAMBER DISC');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('92', 'MISCELLANEOUS/ARCHIVE DISC');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('93', 'WIND BAND TRAINING DISC');
INSERT INTO `category` (`categoryID`, `category`) VALUES ('94', 'MARCHING BAND DISC');


INSERT INTO `music` (`musicID`, `catalogueNo`, 'categoryID', `title`, `composer`, `publisher`, `ensembleID`) VALUES ('1', '10-0032-01', '10', 'Hymn of the Highlands', 'Philip Sparke', 'Anglo Music Press', '1');

