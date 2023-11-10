USE mysql;

CREATE TABLE IF NOT EXISTS races (
    raceId INT,
    year INT,
    round INT,
    circuitId INT,
    name VARCHAR(50),
    date DATE,
    time TIME,
    url VARCHAR(100),
    fp1_date DATE,
    fp1_time TIME,
    fp2_date DATE,
    fp2_time TIME,
    fp3_date DATE,
    fp3_time TIME,
    quali_date DATE,
    quali_time TIME,   
    sprint_date DATE,
    sprint_time TIME
);

-- Load data from CSV file into the table
LOAD DATA LOCAL INFILE '/data/races.csv'
INTO TABLE races
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

CREATE TABLE IF NOT EXISTS drivers (
    driverId INT,
    drivrRef VARCHAR(20),
    number INT,
    code CHAR(3),
    forename VARCHAR(50),
    surname VARCHAR(50),
    dob DATE,
    nationality VARCHAR(20),
    url VARCHAR(100)
);

-- Load data from CSV file into the table
LOAD DATA LOCAL INFILE '/data/drivers.csv'
INTO TABLE drivers
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

CREATE TABLE IF NOT EXISTS pit_stops (
    raceId INT,
    driverId INT,
    stop INT,
    lap INT,
    time TIME,
    duration VARCHAR(10),
    milliseconds INT
);

-- Load data from CSV file into the table
LOAD DATA LOCAL INFILE '/data/pit_stops.csv'
INTO TABLE pit_stops
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


-- Create the table if it doesn't exist
CREATE TABLE IF NOT EXISTS results (
    resultId INT,
    raceId INT,
    driverId INT,
    constructorId INT,
    number INT,
    grid INT,
    position INT,
    positionText VARCHAR(10),
    positionOrder INT,
    points INT,
    laps INT,
    time TIME,
    milliseconds INT,
    fastestLap INT,
    rank INT,
    fastestLapTime VARCHAR(10),
    fastestLapSpeed VARCHAR(10),
    statusId INT
);

-- Load data from CSV file into the table
LOAD DATA LOCAL INFILE '/data/results.csv'
INTO TABLE results
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;