-- BEGIN
--     FOR c IN (SELECT table_name FROM user_tables) LOOP
--         EXECUTE IMMEDIATE 'DROP TABLE "' || c.table_name || '" CASCADE CONSTRAINTS';
--     END LOOP;
-- END;

-- PURGE RECYCLEBIN;

CREATE SEQUENCE id_seq1;
CREATE TABLE Smart_Home (
    HomeID           VARCHAR2(100) PRIMARY KEY,
    OwnerEmail       VARCHAR2(100) NOT NULL,
    SquareFootage    NUMBER NOT NULL,
    SecondaryContact VARCHAR2(100)
);

CREATE SEQUENCE id_seq2;
CREATE TABLE Sensor (
    LocalDeviceID    VARCHAR2(100) PRIMARY KEY,
    SensorType       VARCHAR2(100) NOT NULL,
    InstallationDate DATE NOT NULL
);

CREATE SEQUENCE id_seq3;
CREATE TABLE System_Health_Profile (
    ProfileID        VARCHAR2(100) PRIMARY KEY,
    UptimePercentage NUMBER NOT NULL,
    PartitionKey     VARCHAR2(100) NOT NULL,
    HomeID           VARCHAR2(100) NOT NULL -- Added here so the table starts with it
);

CREATE SEQUENCE id_seq4;
CREATE TABLE Weather_Condition (
    ConditionType    VARCHAR2(100) PRIMARY KEY,
    SeverityLevel    NUMBER NOT NULL
);

CREATE SEQUENCE id_seq5;
CREATE TABLE Sensor_Reading (
    ReadingID        VARCHAR2(100) PRIMARY KEY,
    HomeID           VARCHAR2(100) NOT NULL,
    LocalDeviceID    VARCHAR2(100) NOT NULL,
    ConditionType    VARCHAR2(100) NOT NULL,
    Value            NUMBER NOT NULL,
    Timestamp        DATE NOT NULL
);

/* --- ADD ALL CONSTRAINTS AT THE END --- */

-- Connect Health Profile to Smart Home
ALTER TABLE System_Health_Profile 
    ADD CONSTRAINT FK_Health_HomeID 
    FOREIGN KEY (HomeID) 
    REFERENCES Smart_Home (HomeID);

-- Connect Readings to Smart Home
ALTER TABLE Sensor_Reading 
    ADD CONSTRAINT FK_HomeID 
    FOREIGN KEY (HomeID) 
    REFERENCES Smart_Home (HomeID); 

-- Connect Readings to Sensor
ALTER TABLE Sensor_Reading 
    ADD CONSTRAINT FK_LocalDeviceID 
    FOREIGN KEY (LocalDeviceID) 
    REFERENCES Sensor (LocalDeviceID); 

-- Connect Readings to Weather
ALTER TABLE Sensor_Reading 
    ADD CONSTRAINT FK_ConditionType
    FOREIGN KEY (ConditionType) 
    REFERENCES Weather_Condition (ConditionType);

TRUNCATE TABLE Sensor_Reading;