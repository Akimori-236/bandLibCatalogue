CREATE TABLE `music` (
  `musicID` INT NOT NULL,
  `catalogueNo` VARCHAR(45) NOT NULL,
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


-- CREATE TABLE `publisher` (
--   `publisherID` INT NOT NULL,
--   `publisher` VARCHAR(255) NOT NULL,
--   PRIMARY KEY (`publisherID`),
--   UNIQUE INDEX `publisherID_UNIQUE` (`publisherID` ASC));


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


/* Data init */
INSERT INTO `ensemble` (`ensembleID`, `ensemble`) VALUES ('1', 'Concert Band');
INSERT INTO `ensemble` (`ensembleID`, `ensemble`) VALUES ('2', 'Marching Band');
INSERT INTO `ensemble` (`ensembleID`, `ensemble`) VALUES ('3', 'Solo');
INSERT INTO `ensemble` (`ensembleID`, `ensemble`) VALUES ('4', 'Ensemble');
INSERT INTO `ensemble` (`ensembleID`, `ensemble`) VALUES ('5', 'Big Band');
INSERT INTO `ensemble` (`ensembleID`, `ensemble`) VALUES ('6', 'Study');
INSERT INTO `ensemble` (`ensembleID`, `ensemble`) VALUES ('7', 'Reference');
INSERT INTO `ensemble` (`ensembleID`, `ensemble`) VALUES ('8', 'Others');

INSERT INTO `music` (`musicID`, `catalogueNo`, `title`, `composer`, `publisher`, `ensembleID`) VALUES ('1', '10-0032-01', 'Hymn of the Highlands', 'Philip Sparke', 'Anglo Music Press', '1');
