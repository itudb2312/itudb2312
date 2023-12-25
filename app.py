
from flask import Flask, render_template, redirect, url_for, request, jsonify
import mysql.connector as mysql
import datetime

app = Flask(__name__ )

# Your database configuration
# Create a MySQL connection
db = mysql.connect(
    user='user', 
    password='password', 
    database='mysql',
    host='127.0.0.1', 
    port=3306
)

cursor = db.cursor()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/tables')
def tables():
    
    select_query = """SELECT table_name FROM information_schema.tables
    WHERE table_schema = 'mysql';"""
    cursor.execute(select_query)
    result = cursor.fetchall()
    return result

@app.route('/races', methods=['GET', 'POST'])
def races():
    if request.method == 'POST':
        selected_year = request.form.get('selected_year')
        search_query = request.form.get('search_query')

        # Check if the search query is provided
        if search_query:
            # If search query is provided, filter the races based on the query
            search_query = f"%{search_query}%"  # Use "%" for wildcard matching
            select_query = f"SELECT * FROM races WHERE name LIKE %s OR year LIKE %s"
            cursor.execute(select_query, (search_query,search_query))
            result = cursor.fetchall()
            return render_template('races.html', races=result, selected_year="All Years", search_query=search_query)
        elif selected_year and selected_year != "All Years":
            # If a specific year is selected, filter by that year
            select_query = f"SELECT * FROM races WHERE year = {selected_year}"
            cursor.execute(select_query)
            result = cursor.fetchall()
            return render_template('races.html', races=result, selected_year=selected_year, search_query="")
        else:
            # If no specific year or search query is provided, retrieve all races
            select_query = "SELECT * FROM races"
            cursor.execute(select_query)
            result = cursor.fetchall()
            return render_template('races.html', races=result, selected_year="All Years", search_query="")
    else:
        # Retrieve all races when no specific year or search query is provided
        select_query = "SELECT * FROM races"
        cursor.execute(select_query)
        result = cursor.fetchall()
        return render_template('races.html', races=result, search_query="")

    
@app.route('/add_race', methods=['POST'])
def add_race():
    if request.method == 'POST':
        # Get form data
        year = request.form['year']
        round = request.form['round']
        circuitId = request.form['circuitId']
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        url = request.form['url']
        fp1_date = request.form['fp1_date']
        fp1_time = request.form['fp1_time']
        fp2_date = request.form['fp2_date']
        fp2_time = request.form['fp2_time']
        fp3_date = request.form['fp3_date']
        fp3_time = request.form['fp3_time']
        quali_date = request.form['quali_date']
        quali_time = request.form['quali_time']
        sprint_date = request.form['sprint_date']
        sprint_time = request.form['sprint_time']

        # Insert new race into the database
        insert_query = """
            INSERT INTO races (year, round, circuitId, name, date, time, url,
                                           fp1_date, fp1_time, fp2_date, fp2_time, fp3_date, fp3_time,
                                           quali_date, quali_time, sprint_date, sprint_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (year, round, circuitId, name, date, time, url,
                                      fp1_date, fp1_time, fp2_date, fp2_time, fp3_date, fp3_time,
                                      quali_date, quali_time, sprint_date, sprint_time))
        # Commit the changes to the database
        db.commit()

        return redirect(url_for('races'))


# Similarly, you can implement edit and delete routes
@app.route('/edit_race', methods=['POST'])
def edit_race():
    if request.method == 'POST':
        race_id = request.form.get('raceId')
        year = request.form.get('year')
        round = request.form.get('round')
        circuitId = request.form.get('circuitId')
        name = request.form.get('name')
        date = request.form.get('date')
        time = request.form.get('time')
        url = request.form.get('url')
        fp1_date = request.form.get('fp1_date')
        fp1_time = request.form.get('fp1_time')
        fp2_date = request.form.get('fp2_date')
        fp2_time = request.form.get('fp2_time')
        fp3_date = request.form.get('fp3_date')
        fp3_time = request.form.get('fp3_time')
        quali_date = request.form.get('quali_date')
        quali_time = request.form.get('quali_time')
        sprint_date = request.form.get('sprint_date')
        sprint_time = request.form.get('sprint_time')

        update_query = """
            UPDATE races
            SET year = %s, round = %s, circuitId = %s, name = %s, date = %s, time = %s,
                url = %s, fp1_date = %s, fp1_time = %s, fp2_date = %s, fp2_time = %s, fp3_date = %s, fp3_time = %s,
                quali_date = %s, quali_time = %s, sprint_date = %s, sprint_time = %s
            WHERE raceId = %s
        """
        cursor.execute(update_query, (year, round, circuitId, name, date, time, url,
                                      fp1_date, fp1_time, fp2_date, fp2_time, fp3_date, fp3_time,
                                      quali_date, quali_time, sprint_date, sprint_time, race_id))
        # Commit the changes to the database
        db.commit()

        return redirect(url_for('races'))


@app.route('/delete_race/<int:race_id>', methods=['POST'])
def delete_race(race_id):
    if request.method == 'POST':
        # Delete race from the database based on the race_id
        delete_query = "DELETE FROM races WHERE raceId = %s"
        cursor.execute(delete_query, (race_id,))
        # Commit the changes to the database
        db.commit()

    return redirect(url_for('races'))

@app.route('/race/<int:race_id>/', methods=['GET', 'POST'])
def race(race_id):
    select_query = f"""
    SELECT races.*, circuits.name AS circuitName
    FROM races
    JOIN circuits ON races.circuitId = circuits.circuitId
    WHERE races.raceId = {race_id}
    LIMIT 1
    """
    cursor.execute(select_query)
    result = cursor.fetchall()

    return render_template('race_by_id.html', result=result[0])

@app.route('/get_races', methods=['POST'])
def get_races():
    selected_year = request.form['year']

    select_query = f"""SELECT name
        FROM races
        WHERE year = {selected_year}
        """
    
    cursor.execute(select_query)
    result = cursor.fetchall()
    return jsonify({'races': result})

@app.route('/who_won', methods=['GET'])
def who_won():
    query = "SELECT * FROM races"
    cursor.execute(query)
    races = cursor.fetchall()

    race_data = []
    for race in races:
        winner_name = get_winner(race[0])
        race_data.append({"race_name": race[4], "winner": winner_name})
    return render_template('who_won.html', races=race_data)

def get_winner(race_id):
    query = f'''
        SELECT drivers.forename, drivers.surname
        FROM results
        JOIN drivers ON results.driverId = drivers.driverId
        WHERE results.raceId = {race_id}
        ORDER BY results.points DESC
        LIMIT 1
    '''
    cursor.execute(query)
    winner = cursor.fetchone()

    return f"{winner[0]} {winner[1]}" if winner else "No Winner"
    
@app.route('/drivers', methods=['GET', 'POST'])
def drivers():
    if request.method == 'POST':
        # Check if a search query is present
        search_query = request.form.get('search_query', None)
        
        # Check if a nationality filter is present
        selected_nationality = request.form.get('selected_nationality', 'all')

        if search_query:
            # If a search query is present, filter the drivers based on it
            search_query = f"%{search_query}%"
            select_query = """
                SELECT * FROM drivers
                WHERE driverRef LIKE %s
                    OR number LIKE %s
                    OR code LIKE %s
                    OR forename LIKE %s
                    OR surname LIKE %s
                    OR dob LIKE %s
                    OR nationality LIKE %s
                    OR url LIKE %s
            """
            cursor.execute(select_query, (search_query, search_query, search_query, search_query, search_query, search_query, search_query, search_query))
        elif selected_nationality and selected_nationality != 'all':
            # If a nationality filter is present, filter the drivers based on it
            select_query = f"SELECT * FROM drivers WHERE nationality = '{selected_nationality}'"
            cursor.execute(select_query)
        else:
            # If no search query and no nationality filter, retrieve all drivers
            select_query = "SELECT * FROM drivers"
            cursor.execute(select_query)
    else:
        # Retrieve all drivers when no form is submitted
        select_query = "SELECT * FROM drivers"
        cursor.execute(select_query)

    result = cursor.fetchall()

    # Retrieve distinct nationalities for the dropdown menu
    cursor.execute("SELECT DISTINCT nationality FROM drivers")
    nationalities = cursor.fetchall()

    return render_template('drivers.html', drivers=result, nationalities=nationalities)


@app.route('/about_driver/<int:driver_id>')
def about_driver(driver_id):
    # Query to get driver information, total points, races won, and race names
    query = '''
        SELECT
            drivers.forename,
            drivers.surname,
            drivers.dob,
            SUM(results.points) AS total_points,
            COUNT(CASE WHEN results.positionOrder = 1 THEN 1 END) AS racewins,
            AVG(results.points) AS avg_points,
            GROUP_CONCAT(CASE WHEN results.positionOrder = 1 THEN races.name END) AS racewon
        FROM
            drivers
        JOIN
            results ON drivers.driverId = results.driverId
        JOIN
            races ON results.raceId = races.raceId
        WHERE
            drivers.driverId = %s
        GROUP BY
            drivers.forename,
            drivers.surname,
            drivers.dob;    
    '''
    cursor.execute(query, (driver_id,))
    driver_info = cursor.fetchone()

    if driver_info is not None:
        dob = driver_info[2]
        today = datetime.date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    else: age = 0
    return render_template('about_driver.html', driver_info=driver_info, age=age)


@app.route('/driver_stats')
def driver_stats():
    # Query to get distinct drivers, their winning count, and total points
    query = '''
        SELECT drivers.forename, drivers.surname, SUM(results.points) AS total_points
        FROM drivers
        JOIN results ON drivers.driverId = results.driverId
        GROUP BY drivers.forename, drivers.surname
        ORDER BY total_points DESC;
    '''

    cursor.execute(query)
    driver_stats = cursor.fetchall()

    return render_template('driver_stats.html', driver_stats=driver_stats)

@app.route('/results/', methods=['GET', 'POST'])
@app.route('/race/<int:race_id>/results/', methods=['GET', 'POST'])
def get_results(race_id=None):
    if request.method == 'POST':
        year = request.form['year']
        race_name = request.form['race']

        select_query = f"""
        SELECT 
            res.positionOrder,
            drv.number,
            CONCAT(drv.forename, ' ', drv.surname) AS driver,
            con.name AS constructor,
            res.points,
            drv.driverId,
            res.resultId
        FROM 
            results res
        JOIN (SELECT raceId FROM races WHERE year = {year} AND name = "{race_name}") AS r ON res.raceId = r.raceId
        JOIN drivers drv ON res.driverId = drv.driverId
        JOIN constructors con ON res.constructorId = con.constructorId
        ORDER BY res.positionOrder ASC"""
        
        cursor.execute(select_query)
        result = cursor.fetchall()
        race_info = [year,race_name]
        
        return render_template('results.html', results=result,race_info=race_info)

    if race_id is not None:
        select_query = f""" SELECT 
            res.positionOrder,
            drv.number,
            CONCAT(drv.forename, ' ', drv.surname) AS driver,
            con.name AS constructor,
            res.points,
            drv.driverId,
            res.resultId,
            r.year,
            r.name
        FROM 
            results res
        JOIN races r ON res.raceId = r.raceId
        JOIN drivers drv ON res.driverId = drv.driverId
        JOIN constructors con ON res.constructorId = con.constructorId
        WHERE r.raceId = {race_id} 
        ORDER BY res.positionOrder ASC
        """
        
        cursor.execute(select_query)
        result = cursor.fetchall()
        race_info = [result[0][7],result[0][8]]
        return render_template('results.html', results=result ,race_info=race_info)

    result = []
    return render_template('results.html',results=result)

@app.route('/create_result', methods=['GET', 'POST'])
def create_result():
    if request.method == 'POST':
        race_year = request.form['race_year']
        race_name = request.form['race_name']
        driver_id = request.form['driver_id']
        constructor_id = request.form['constructor_id']
        number = request.form['number']
        grid = request.form['grid']
        position = request.form['position']
        position_text = request.form['position_text']
        position_order = request.form['position_order']
        points = request.form['points']
        laps = request.form['laps']
        time = request.form['time']
        milliseconds = request.form['milliseconds']
        fastest_lap = request.form['fastest_lap']
        rank = request.form['rank']
        fastest_lap_time = request.form['fastest_lap_time']
        fastest_lap_speed = request.form['fastest_lap_speed']
        status_id = request.form['status_id']
        
        # Get race ID from year and name
        race_query = f"""SELECT raceId FROM races WHERE name = "{race_name}" AND year = {race_year} """
        cursor.execute(race_query)
        race_result = cursor.fetchall()
        race_id = race_result[0][0] if race_result else None

        # Insert the result into the database
        insert_query = """
            INSERT INTO results (raceId, driverId, constructorId, number, grid, position, positionText, positionOrder, points, laps, time, milliseconds, fastestLap, rank, fastestLapTime, fastestLapSpeed, statusId)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (race_id, driver_id, constructor_id, number, grid, position, position_text, position_order, points, laps, time, milliseconds, fastest_lap, rank, fastest_lap_time, fastest_lap_speed, status_id))
        db.commit()

        # Return to race/race_id/results page
        return redirect(url_for('get_results', race_id=race_id))    

    driver_query = f"""SELECT
    driverId,
    CONCAT(forename, ' ', surname) AS driver
    FROM drivers
    """
    cursor.execute(driver_query)
    driver_result = cursor.fetchall()

    constructor_query = f"""SELECT
    constructorId,
    name
    FROM constructors
    """
    cursor.execute(constructor_query)
    constructor_result = cursor.fetchall()


    return render_template('create_result.html', drivers=driver_result, constructors=constructor_result)
    
@app.route('/update_result/<int:result_id>', methods=['GET', 'POST'])    
def update_result(result_id):
    if request.method == 'POST':
        race_year = request.form['race_year']
        race_name = request.form['race_name']
        driver_id = request.form['driver_id']
        constructor_id = request.form['constructor_id']
        number = request.form['number']
        grid = request.form['grid']
        position = request.form['position']
        position_text = request.form['position_text']
        position_order = request.form['position_order']
        points = request.form['points']
        laps = request.form['laps']
        time = request.form['time']
        milliseconds = request.form['milliseconds']
        fastest_lap = request.form['fastest_lap']
        rank = request.form['rank']
        fastest_lap_time = request.form['fastest_lap_time']
        fastest_lap_speed = request.form['fastest_lap_speed']
        status_id = request.form['status_id']
        
        # Get race ID from year and name
        race_query = f"""SELECT raceId FROM races WHERE name = "{race_name}" AND year = {race_year} """
        cursor.execute(race_query)
        race_result = cursor.fetchall()
        race_id = race_result[0][0] if race_result else None

        
        # Convert values to integers if they are not None
        fastest_lap = int(fastest_lap) if fastest_lap is not None and fastest_lap != 'None' else 0
        rank = int(rank) if rank is not None and rank != 'None' else 0
        milliseconds = int(milliseconds) if milliseconds is not None and milliseconds != 'None' else 0
        position = int(position) if position is not None and position != 'None' else 0
        position_order = int(position_order) if position_order is not None and position_order != 'None' else 0
        points = int(points) if points is not None and points != 'None' else 0
        laps = int(laps) if laps is not None and laps != 'None' else 0
        grid = int(grid) if grid is not None and grid != 'None' else 0
        number = int(number) if number is not None and number != 'None' else 0

        update_query = """
            UPDATE results
            SET raceId = %s, driverId = %s, constructorId = %s, number = %s, grid = %s, position = %s, positionText = %s, positionOrder = %s, points = %s, laps = %s, time = %s, milliseconds = %s, fastestLap = %s, rank = %s, fastestLapTime = %s, fastestLapSpeed = %s, statusId = %s
            WHERE resultId = %s
            """

        cursor.execute(update_query, (race_id, driver_id, constructor_id, number, grid, position, position_text, position_order, points, laps, time, milliseconds, fastest_lap, rank, fastest_lap_time, fastest_lap_speed, status_id, result_id))
        db.commit()

        # Return to race/race_id/results page
        return redirect(url_for('get_results', race_id=race_id))   
 
    select_query = f"""SELECT * FROM results WHERE resultId = {result_id} LIMIT 1"""
 
    cursor.execute(select_query)
    result = cursor.fetchall()

    race_query = f"""SELECT year,name FROM races where raceId = {result[0][1]}"""
    cursor.execute(race_query)
    race = cursor.fetchall()

    driver_query = f"""SELECT
    driverId,
    CONCAT(forename, ' ', surname) AS driver
    FROM drivers WHERE driverId = {result[0][2]}
    """
    cursor.execute(driver_query)
    driver_result = cursor.fetchall()

    constructor_query = f"""SELECT
    constructorId,
    name
    FROM constructors  WHERE constructorId = {result[0][3]}
    """
    cursor.execute(constructor_query)
    constructor_result = cursor.fetchall()
    
    return render_template('update_result.html',result=result[0],race=race[0],drivers=driver_result, constructors=constructor_result)

@app.route('/delete_result/<int:result_id>', methods=['POST'])
def delete_result(result_id):
    if request.method == 'POST':
        # Delete result from the database based on the result_id
        delete_query = "DELETE FROM results WHERE resultId = %s"
        cursor.execute(delete_query, (result_id,))
        # Commit the changes to the database
        db.commit()

    return redirect(url_for('get_results'))

@app.route('/delete_driver/<int:driver_id>', methods=['POST'])
def delete_driver(driver_id):
    if request.method == 'POST':
        # Perform deletion from the database
        delete_query = "DELETE FROM drivers WHERE driverId = %s"
        cursor.execute(delete_query, (driver_id,))
        db.commit()

        # Redirect to the drivers page or any other page as needed
        return redirect(url_for('drivers'))

@app.route('/add_driver', methods=['POST'])
def add_driver():
    if request.method == 'POST':
        # Retrieve form data
        driverRef = request.form.get('driverRef')
        number = request.form.get('number')
        code = request.form.get('code')
        forename = request.form.get('forename')
        surname = request.form.get('surname')
        dob = request.form.get('dob')
        nationality = request.form.get('nationality')
        url = request.form.get('url')

        # Insert the new driver into the database
        insert_query = """
            INSERT INTO drivers (driverRef, number, code, forename, surname, dob, nationality, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (driverRef, number, code, forename, surname, dob, nationality, url))
        db.commit()

        # Redirect to the drivers page or any other page as needed
        return redirect(url_for('drivers'))

@app.route('/edit_driver', methods=['POST'])
def edit_driver():
    if request.method == 'POST':
        # Retrieve form data
        driverId = request.form.get('driverId')
        driverRef = request.form.get('driverRef')
        number = request.form.get('number')
        code = request.form.get('code')
        forename = request.form.get('forename')
        surname = request.form.get('surname')
        dob = request.form.get('dob')
        nationality = request.form.get('nationality')
        url = request.form.get('url')

        # Update the driver's information in the database
        update_query = """
            UPDATE drivers
            SET driverRef = %s, number = %s, code = %s, forename = %s, surname = %s, dob = %s, nationality = %s, url = %s
            WHERE driverId = %s
        """
        cursor.execute(update_query, (driverRef, number, code, forename, surname, dob, nationality, url, driverId))
        db.commit()

        # Redirect to the drivers page or any other page as needed
        return redirect(url_for('drivers'))
    

@app.route('/pit_stops/',methods=['GET','POST'])
@app.route('/race/<int:race_id>/pit_stops/', methods=['GET', 'POST'])
def pit_stops(race_id=None):
    if request.method == 'POST':
        year = request.form['year']
        race_name = request.form['race']

        select_query = f"""SELECT
        CONCAT(d.forename, ' ', d.surname) AS driver,
        p.stop,
        p.lap,
        p.time,
        p.duration,
        p.milliseconds,
        r.raceId,
        d.driverId
        FROM pit_stops p
        JOIN drivers d ON p.driverId = d.driverId
        JOIN races r ON p.raceId = r.raceId
        WHERE  (r.name = "{race_name}" AND r.year = {year})
        ORDER BY p.milliseconds ASC
        """
        cursor.execute(select_query)
        result = cursor.fetchall()
        race_info = [year,race_name]
        
        return render_template('pit_stops.html', pit_stops=result,race_info=race_info)


    if race_id is not None:
        select_query = f"""SELECT
        CONCAT(d.forename, ' ', d.surname) AS driver,
        p.stop,
        p.lap,
        p.time,
        p.duration,
        p.milliseconds,
        r.raceId,
        d.driverId, 
        r.year,
        r.name
        FROM pit_stops p
        JOIN drivers d ON p.driverId = d.driverId
        JOIN races r ON p.raceId = r.raceId
        WHERE p.raceId = {race_id}
        ORDER BY p.duration ASC
        """
        
        cursor.execute(select_query)
        result = cursor.fetchall()
        
        if result != []:
            race_info = [result[0][8],result[0][9]]
        else:  
            race_query = f"""SELECT year,name FROM races where raceId = {race_id}"""
            cursor.execute(race_query)
            race = cursor.fetchall()
            race_info = [race[0][0],race[0][1]]
        return render_template('pit_stops.html', pit_stops=result ,race_info=race_info)

    select_query = """SELECT
    CONCAT(d.forename, ' ', d.surname) AS driver,
    p.stop,
    p.lap,
    p.time,
    p.duration,
    p.milliseconds
    FROM pit_stops p
    JOIN drivers d ON p.driverId = d.driverId LIMIT 0
    """
    cursor.execute(select_query)
    result = cursor.fetchall()
    race_info = []

    return render_template('pit_stops.html',pit_stops=result,race_info=race_info)

@app.route('/create_pit_stop/', methods=['GET', 'POST'])
def create_pit_stop():
    if request.method == 'POST':
        race_year = request.form['race_year']
        race_name = request.form['race_name']
        driver_id = request.form['driver_id']
        stop = request.form['stop']
        lap = request.form['lap']
        time = request.form['time']
        duration = request.form['duration']
        milliseconds = request.form['milliseconds']
        
        
        # Get race ID from year and name
        race_query = f"""SELECT raceId FROM races WHERE name = "{race_name}" AND year = {race_year} """
        cursor.execute(race_query)
        race_result = cursor.fetchall()
        race_id = race_result[0][0] if race_result else None

        insert_query = """
            INSERT INTO pit_stops (raceId, driverId, stop, lap, time, duration, milliseconds)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query,(race_id,driver_id,stop,lap,time,duration,milliseconds))
        db.commit()

        # Return to race/race_id/results page
        return redirect(url_for('pit_stops', race_id=race_id))    

    driver_query = f"""SELECT
    driverId,
    CONCAT(forename, ' ', surname) AS driver
    FROM drivers
    """
    cursor.execute(driver_query)
    driver_result = cursor.fetchall()

    constructor_query = f"""SELECT
    constructorId,
    name
    FROM constructors
    """
    cursor.execute(constructor_query)
    constructor_result = cursor.fetchall()


    return render_template('create_pitstop.html', drivers=driver_result, constructors=constructor_result)

@app.route('/update_pit_stop/<int:race_id>/<int:driver_id>/<int:stop>/', methods=['GET', 'POST'])
def update_pit_stop(race_id,driver_id,stop):
    if request.method == 'POST':
        race_year = request.form['race_year']
        race_name = request.form['race_name']
        driver_id = request.form['driver_id']
        stop = request.form['stop']
        lap = request.form['lap']
        time = request.form['time']
        duration = request.form['duration']
        milliseconds = request.form['milliseconds']
            # Get race ID from year and name
        race_query = f"""SELECT raceId FROM races WHERE name = "{race_name}" AND year = {race_year} """
        cursor.execute(race_query)
        race_result = cursor.fetchall()
        race_id = race_result[0][0] if race_result else None
        
        # Convert values to integers if they are not None
        stop = int(stop) if stop is not None and stop != 'None' else 0
        lap = int(lap) if lap is not None and lap != 'None' else 0
        milliseconds = int(milliseconds) if milliseconds is not None and milliseconds != 'None' else 0
        


        update_query = """
            UPDATE pit_stops
            SET raceId = %s, driverId = %s, stop = %s, lap = %s, time = %s, duration = %s, milliseconds = %s
            WHERE raceId = %s AND driverId = %s AND stop = %s
        """
        
        cursor.execute(update_query, (race_id, driver_id, stop, lap, time, duration, milliseconds,race_id, driver_id, stop))
        db.commit()
        
        # Return to pit_stops page
        return redirect(url_for('pit_stops',race_id=race_id))

    select_query = f"""SELECT
    CONCAT(d.forename, ' ', d.surname) AS driver,
    p.stop,
    p.lap,
    p.time,
    p.duration,
    p.milliseconds,
    r.raceId,
    d.driverId
    FROM pit_stops p
    JOIN drivers d ON p.driverId = d.driverId
    JOIN races r ON p.raceId = r.raceId
    WHERE  r.raceId = {race_id} and d.driverId = {driver_id} and p.stop = {stop}
    ORDER BY p.milliseconds ASC
    """
    cursor.execute(select_query)
    pit_stop = cursor.fetchall()

    driver_query = f"""SELECT
    driverId,
    CONCAT(forename, ' ', surname) AS driver
    FROM drivers
    """
    cursor.execute(driver_query)
    driver_result = cursor.fetchall()

    print(pit_stop[0][7],pit_stop[0][0])
    print(driver_result[0][0],driver_result[0][1])

    race_query = f"""SELECT year,name FROM races where raceId = {race_id}"""
    cursor.execute(race_query)
    race = cursor.fetchall()
    
    return render_template('update_pitstop.html', pit_stop=pit_stop[0], race=race[0], drivers=driver_result)

@app.route('/delete_pit_stop/<int:race_id>/<int:driver_id>/<int:stop>/', methods=['POST'])
def delete_pit_stop(race_id,driver_id,stop):
    if request.method == 'POST':
        # Delete result from the database based on the result_id
        delete_query = "DELETE FROM pit_stops WHERE raceId = %s AND driverId = %s AND stop = %s"
        cursor.execute(delete_query, (race_id,driver_id,stop))
        db.commit()

    return redirect(url_for('pit_stops'))

@app.route('/driver_standings', methods=['GET', 'POST'])
def driver_standings():
    if request.method == 'POST':
        selected_driver = request.form.get('selected_driver')
    else:
        selected_driver = 'Hamilton'

    select_query = f"""SELECT driver_standings.driverStandingsId, races.name, drivers.surname, 
        driver_standings.points, driver_standings.position, driver_standings.wins
    FROM driver_standings 
    JOIN drivers ON driver_standings.driverId = drivers.driverId
    JOIN races ON driver_standings.raceId = races.raceId
    WHERE drivers.surname = '{selected_driver}'
    ORDER BY driver_standings.driverStandingsId ASC;
    """

    cursor.execute(select_query)
    result = cursor.fetchall()

    cursor.execute("SELECT DISTINCT surname FROM drivers")
    drivers = cursor.fetchall()

    return render_template('driver_standings.html',driver_standings=result, drivers=drivers)

@app.route('/add_driver_standing', methods=['POST'])
def add_driver_standing():
    if request.method == 'POST':
        race = request.form.get('race')
        driver = request.form.get('driver')
        point = request.form.get('point')
        position = request.form.get('position')
        wins = request.form.get('wins')

        insert_query = """
            INSERT INTO driver_standings (raceId, driverId, points, position, positionText, wins)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query,(race , driver, point, position, position, wins))
        db.commit()

        return redirect(url_for('driver_standings'))

@app.route('/delete_driver_standing/<int:driver_standing_id>', methods=['POST'])
def delete_driver_standing(driver_standing_id):
    if request.method == 'POST':
        delete_query = "DELETE FROM driver_standings WHERE driverStandingsId = %s"
        cursor.execute(delete_query, (driver_standing_id,))
        db.commit()

        return redirect(url_for('driver_standings'))
    
@app.route('/edit_driver_standing', methods=['POST'])
def edit_driver_standing():
    if request.method == 'POST':
        driverStandingId = request.form.get('driverStandingId')
        race = request.form.get('race')
        driver = request.form.get('driver')
        point = request.form.get('point')
        position = request.form.get('position')
        wins = request.form.get('wins')

        update_query = """
            UPDATE driver_standings
            SET raceId = %s, driverId = %s, points = %s, position = %s, positionText = %s, wins = %s
            WHERE driverStandingsId = %s
        """
        cursor.execute(update_query, (race, driver, point, position, position, wins, driverStandingId))
        db.commit()

        return redirect(url_for('driver_standings'))


@app.route('/sprint_results', methods=['GET', 'POST'])
def sprint_results():
    select_query = """
    SELECT sprint_results.resultId, races.name, drivers.surname,
    constructors.name, sprint_results.number, sprint_results.position, sprint_results.points,
    sprint_results.laps, sprint_results.time, sprint_results.fastestLap, sprint_results.fastestLapTime
    FROM sprint_results
    JOIN drivers ON sprint_results.driverId = drivers.driverId
    JOIN races ON sprint_results.raceId = races.raceId
    JOIN constructors ON constructors.constructorId = sprint_results.constructorId
    ORDER BY sprint_results.resultId ASC; """

    if request.method == 'POST':
        selected_constructor = request.form.get('select_constructor')
        if selected_constructor and selected_constructor != 'all':
            select_query = f"""SELECT sprint_results.resultId, races.name, drivers.surname,
                constructors.name, sprint_results.number, sprint_results.position, sprint_results.points,
                sprint_results.laps, sprint_results.time, sprint_results.fastestLap, sprint_results.fastestLapTime
                FROM sprint_results
                JOIN drivers ON sprint_results.driverId = drivers.driverId
                JOIN races ON sprint_results.raceId = races.raceId
                JOIN constructors ON constructors.constructorId = sprint_results.constructorId
                WHERE constructors.name = '{selected_constructor}'
                ORDER BY sprint_results.resultId ASC; """

    cursor.execute(select_query)
    result = cursor.fetchall()

    cursor.execute("SELECT DISTINCT name FROM constructors")
    constructors = cursor.fetchall()

    return render_template('sprint_results.html',sprint_results=result, constructors=constructors)

@app.route('/add_sprint_result', methods=['POST'])
def add_sprint_result():
    if request.method == 'POST':
        race = request.form.get('race')
        driver = request.form.get('driver')
        constructor = request.form.get('constructor')
        number = request.form.get('number')
        position = request.form.get('position')
        points = request.form.get('points')
        laps = request.form.get('laps')
        time = request.form.get('time')
        fastest_lap = request.form.get('fastest_lap')
        fastest_lap_time = request.form.get('fastest_lap_time')

        insert_query = """
            INSERT INTO sprint_results (raceId, driverId, constructorId, number, position, 
            positionText, points, laps, time, fastestLap, fastestLapTime)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (race, driver, constructor, number, position, position, points, laps, time, fastest_lap, fastest_lap_time))
        db.commit()

        return redirect(url_for('sprint_results'))

@app.route('/delete_sprint_result/<int:result_id>', methods=['POST'])
def delete_sprint_result(result_id):
    if request.method == 'POST':
        delete_query = "DELETE FROM sprint_results WHERE resultId = %s"
        cursor.execute(delete_query, (result_id,))
        db.commit()

        return redirect(url_for('sprint_results'))

@app.route('/edit_sprint_result', methods=['POST'])
def edit_sprint_result():
    if request.method == 'POST':
        resultId = request.form.get('sprintResultId')
        race = request.form.get('race')
        driver = request.form.get('driver')
        constructor = request.form.get('constructor')
        number = request.form.get('number')
        position = request.form.get('position')
        points = request.form.get('points')
        laps = request.form.get('laps')
        time = request.form.get('time')
        fastest_lap = request.form.get('fastest_lap')
        fastest_lap_time = request.form.get('fastest_lap_time')

        update_query = """
            UPDATE sprint_results
            SET driverId = %s, raceId = %s, constructorId = %s, number = %s, position = %s, positionText = %s, 
            points = %s, laps = %s, time = %s, fastestLap=%s, fastestLapTime=%s 
            WHERE resultId = %s
        """
        cursor.execute(update_query, (driver, race, constructor, number, position, position, points, laps, time, fastest_lap, fastest_lap_time, resultId))
        db.commit()

        return redirect(url_for('sprint_results'))

@app.route('/circuits', methods=['GET', 'POST'])
def circuits():
    selected_hemisphere = request.form.get('selected_hemisphere') if request.method == 'POST' else None
    search_query = request.form.get('search_query') if request.method == 'POST' else None

    select_query = """
        SELECT
            circuits.circuitId,
            circuits.name,
            circuits.location,
            circuits.country,
            MAX(circuits.alt) as altitude,
            circuits.url
        FROM
            circuits
    """

    params = ()

    if selected_hemisphere and selected_hemisphere != "All Hemispheres":
        select_query += " WHERE circuits.lat > 0" if selected_hemisphere == "Northern Hemisphere" else " WHERE circuits.lat < 0"

    if search_query:
        search_query = "%" + search_query + "%"
        if 'WHERE' in select_query:
            select_query += " AND (circuits.name LIKE %s OR circuits.location LIKE %s OR circuits.country LIKE %s)"
        else:
            select_query += " WHERE (circuits.name LIKE %s OR circuits.location LIKE %s OR circuits.country LIKE %s)"
        params += (search_query, search_query, search_query)

    select_query += """
        GROUP BY
            circuits.circuitId,
            circuits.name,
            circuits.location,
            circuits.country,
            circuits.url
        ORDER BY
            altitude DESC
    """

    cursor.execute(select_query, params)
    result = cursor.fetchall()

    return render_template('circuits.html', circuits=result, selected_hemisphere=selected_hemisphere if selected_hemisphere else "All Hemispheres")

@app.route('/add_circuit', methods=['POST'])
def add_circuit():
    fields = ['circuitRef', 'name', 'location', 'country', 'lat', 'lng', 'alt', 'url']

    values = [request.form.get(field) for field in fields]

    insert_query = f"""
        INSERT INTO circuits ({', '.join(fields)})
        VALUES ({', '.join(['%s'] * len(fields))})
    """

    cursor.execute(insert_query, values)
    db.commit()

    return redirect(url_for('circuits'))

@app.route('/edit_circuit', methods=['POST'])
def edit_circuit():
    fields = ['circuitId', 'circuitRef', 'name', 'location', 'country', 'lat', 'lng', 'alt', 'url']

    values = [request.form.get(field) for field in fields]

    values.append(request.form.get('circuitId'))

    update_query = f"""
        UPDATE circuits
        SET {', '.join(f'{field} = %s' for field in fields)}
        WHERE circuitId = %s
    """

    cursor.execute(update_query, values)
    db.commit()

    return redirect(url_for('circuits'))
    
@app.route('/delete_circuit/<int:circuit_id>', methods=['POST'])
def delete_circuit(circuit_id):
    delete_query = "DELETE FROM circuits WHERE circuitId = %s"
    cursor.execute(delete_query, (circuit_id,))
    db.commit()
    return redirect(url_for('circuits'))

@app.route('/qualifying', methods=['GET', 'POST'])
def qualifying():
    cursor.execute("SELECT DISTINCT drivers.surname FROM qualifying JOIN drivers ON qualifying.driverId = drivers.driverId")
    driver_surnames = [driver[0] for driver in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT driverId FROM qualifying")
    drivers = [str(driver[0]) for driver in cursor.fetchall()]

    selected_surname = request.form.get('selected_surname') if request.method == 'POST' else None
    search_query = request.form.get('search_query') if request.method == 'POST' else None

    select_query = """
        SELECT
            qualifying.qualifyId,
            races.date as raceDate,
            drivers.forename as driverName,
            drivers.surname as driverSurname,
            constructors.name as constructorName,
            qualifying.number,
            qualifying.position,
            qualifying.q1,
            qualifying.q2,
            qualifying.q3
        FROM
            qualifying
        JOIN
            races ON qualifying.raceId = races.raceId
        JOIN
            drivers ON qualifying.driverId = drivers.driverId
        JOIN
            constructors ON qualifying.constructorId = constructors.constructorId
    """

    params = ()

    if selected_surname and selected_surname != "All Drivers":
        select_query += " WHERE drivers.surname = %s"
        params += (selected_surname,)

    if search_query:
        search_query = "%" + search_query + "%"
        if params:
            select_query += " AND (drivers.forename LIKE %s OR drivers.surname LIKE %s OR constructors.name LIKE %s)"
        else:
            select_query += " WHERE (drivers.forename LIKE %s OR drivers.surname LIKE %s OR constructors.name LIKE %s)"
        params += (search_query, search_query, search_query)

    select_query += " GROUP BY qualifying.qualifyId, constructorName ORDER BY raceDate DESC, position ASC LIMIT 3500"
    cursor.execute(select_query, params)

    result = cursor.fetchall()

    return render_template('qualifying.html', qualifying=result, selected_surname=selected_surname if selected_surname else "All Surnames", driver_surnames=driver_surnames, drivers=drivers)


@app.route('/add_qualifying', methods=['POST'])
def add_qualifying():
    fields = ['raceId', 'driverId', 'constructorId', 'number', 'position', 'q1', 'q2', 'q3']

    values = [request.form.get(field) for field in fields]

    insert_query = f"""
        INSERT INTO qualifying ({', '.join(fields)})
        VALUES ({', '.join(['%s'] * len(fields))})
    """

    cursor.execute(insert_query, values)
    db.commit()

    return redirect(url_for('qualifying'))


@app.route('/edit_qualifying', methods=['POST'])
def edit_qualifying():
    fields = ['qualifyId','raceId', 'driverId', 'constructorId', 'number', 'position', 'q1', 'q2', 'q3']

    values = [request.form.get(field) for field in fields]

    values.append(request.form.get('qualifyId'))

    update_query = f"""
        UPDATE qualifying
        SET {', '.join(f'{field} = %s' for field in fields)}
        WHERE qualifyId = %s
    """

    cursor.execute(update_query, values)
    db.commit()

    return redirect(url_for('qualifying'))

@app.route('/delete_qualifying/<int:qualifyId>', methods=['POST'])
def delete_qualifying(qualifyId):
    delete_query = "DELETE FROM qualifying WHERE qualifyId = %s"
    cursor.execute(delete_query, (qualifyId,))
    db.commit()
    return redirect(url_for('qualifying'))


if __name__ == '__main__':
    app.run(port=8000, debug=True)
