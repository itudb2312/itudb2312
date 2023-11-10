USE mysql;

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

-- Create the table if it doesn't exist
CREATE TABLE IF NOT EXISTS sprint_results (
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
    fastestLapTime VARCHAR(10),
    statusId INT
);

-- Load data from CSV file into the table
LOAD DATA LOCAL INFILE '/data/sprint_results.csv'
INTO TABLE sprint_results
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


-- Create the table if it doesn't exist
CREATE TABLE IF NOT EXISTS driver_standings (
    driverStandingsId INT,
    raceId INT,
    driverId INT,
    points INT,
    position INT,
    positionText VARCHAR(10),
    wins INT
);

-- Load data from CSV file into the table
LOAD DATA LOCAL INFILE '/data/driver_standings.csv'
INTO TABLE driver_standings
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;