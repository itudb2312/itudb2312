from flask import Flask, render_template, request,jsonify
import mysql.connector as mysql

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

        # Check if the selected year is not empty or "All Years"
        if selected_year and selected_year != "All Years":
            # If a specific year is selected, filter by that year
            select_query = f"SELECT * FROM races WHERE year = {selected_year}"
            cursor.execute(select_query)
            result = cursor.fetchall()
            return render_template('races.html', races=result, selected_year=selected_year)
        else:
            # If no specific year is selected or "All Years," retrieve all races
            select_query = "SELECT * FROM races"
            cursor.execute(select_query)
            result = cursor.fetchall()
            return render_template('races.html', races=result, selected_year="All Years")
    else:
        # Retrieve all races when no specific year is selected
        select_query = "SELECT * FROM races"
        cursor.execute(select_query)
        result = cursor.fetchall()
        return render_template('races.html', races=result)

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
        selected_nationality = request.form.get('selected_nationality')
        if selected_nationality and selected_nationality != 'all':
            select_query = f"SELECT * FROM drivers WHERE nationality = '{selected_nationality}'"
        else:
            select_query = "SELECT * FROM drivers"
    else:
        select_query = "SELECT * FROM drivers"

    cursor.execute(select_query)
    result = cursor.fetchall()

    # Retrieve distinct nationalities for the dropdown menu
    cursor.execute("SELECT DISTINCT nationality FROM drivers")
    nationalities = cursor.fetchall()

    return render_template('drivers.html', drivers=result, nationalities=nationalities)

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

@app.route('/results', methods=['GET', 'POST'])
@app.route('/results/<int:race_id>', methods=['GET', 'POST'])
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
            res.points
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
        print("BURDAA RACE ID VAR",race_id)
        select_query = f""" SELECT 
            res.positionOrder,
            drv.number,
            CONCAT(drv.forename, ' ', drv.surname) AS driver,
            con.name AS constructor,
            res.points,
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
        race_info = [result[0][5],result[0][6]]
        return render_template('results.html', results=result ,race_info=race_info)
    
    # GET isteği geldiğinde çalışacak olan kodlar
    select_query = "SELECT * FROM results WHERE resultId < 100 LIMIT 0"
    cursor.execute(select_query)
    result = cursor.fetchall()

    return render_template('results.html', results=result)

@app.route('/create_result', methods=['GET', 'POST'])
def create_result():
    if request.method == 'POST':
        result_id = request.form['result_id']
        race_id = request.form['race_id']
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
        
        
        # Insert the result into the database
        insert_query = f"INSERT INTO results (raceId, driverId, position, points) VALUES ({race_id}, {driver_id}, {position}, {points})"
        cursor.execute(insert_query)
        db.commit()
        
        return "Result created successfully"
    
    return render_template('create_result.html')
    

@app.route('/race/<int:race_id>', methods=['GET','POST'])
def race(race_id):
    select_query = f"""SELECT * FROM races WHERE raceId = {race_id} LIMIT 1"""
    cursor.execute(select_query)
    result = cursor.fetchall()

    return render_template('race_by_id.html',result=result[0])


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

@app.route('/pit_stops')
def pit_stops():
    select_query = "SELECT * FROM pit_stops"
    cursor.execute(select_query)
    result = cursor.fetchall()

    return render_template('pit_stops.html',pit_stops=result)

@app.route('/driver_standings')
def driver_standings():
    select_query = """SELECT driver_standings.driverStandingsId, races.name, drivers.surname, 
        driver_standings.points, driver_standings.position, driver_standings.wins
    FROM driver_standings 
    JOIN drivers ON driver_standings.driverId = drivers.driverId
    JOIN races ON driver_standings.raceId = races.raceId
    WHERE drivers.surname = "Hamilton"
    ORDER BY driver_standings.driverStandingsId ASC;
    """
    cursor.execute(select_query)
    result = cursor.fetchall()

    return render_template('driver_standings.html',driver_standings=result)

@app.route('/sprint_results')
def sprint_results():
    select_query = """SELECT sprint_results.resultId, races.name, drivers.surname,
    constructors.name, sprint_results.number, sprint_results.grid, sprint_results.position, sprint_results.points,
    sprint_results.laps, sprint_results.time, sprint_results.milliseconds, sprint_results.fastestLap, sprint_results.fastestLapTime
    FROM sprint_results
    JOIN drivers ON sprint_results.driverId = drivers.driverId
    JOIN races ON sprint_results.raceId = races.raceId
    JOIN constructors ON constructors.constructorId = sprint_results.constructorId
    WHERE drivers.surname = "Hamilton"
    ORDER BY sprint_results.resultId ASC; """

    cursor.execute(select_query)
    result = cursor.fetchall()

    return render_template('sprint_results.html',sprint_results=result)

@app.route('/circuits', methods=['GET', 'POST'])
def circuits():
    if request.method == 'POST':
        selected_hemisphere = request.form.get('selected_hemisphere')

        # Check if the selected hemisphere is not empty or "All Hemispheres"
        if selected_hemisphere and selected_hemisphere != "All Hemispheres":
            # If a specific hemisphere is selected, filter by that hemisphere
            if selected_hemisphere == "Northern Hemisphere":
                select_query = "SELECT * FROM circuits WHERE lat > 0"
            else:
                select_query = "SELECT * FROM circuits WHERE lat < 0"
            cursor.execute(select_query)
            result = cursor.fetchall()
            return render_template('circuits.html', circuits=result, selected_hemisphere=selected_hemisphere)
        else:
            # If no specific hemisphere is selected or "All Hemispheres," retrieve all circuits
            select_query = "SELECT * FROM circuits"
            cursor.execute(select_query)
            result = cursor.fetchall()
            return render_template('circuits.html', circuits=result, selected_hemisphere="All Hemispheres")
    else:
        # Retrieve all circuit information, group them by countries, and order them by altitudes
        select_query = """SELECT circuits.name, circuits.location, circuits.country, MAX(circuits.alt) as altitude, circuits.url
                        FROM circuits
                        GROUP BY circuits.name, circuits.location, circuits.country, circuits.url
                        ORDER BY altitude DESC;"""
        cursor.execute(select_query)

        result = cursor.fetchall()
        return render_template('circuits.html', circuits=result)


@app.route('/qualifying', methods=['GET', 'POST'])
def qualifying():
    # Fetch the list of driver surnames for the dropdown
    cursor.execute("SELECT DISTINCT drivers.surname FROM qualifying JOIN drivers ON qualifying.driverId = drivers.driverId")
    driver_surnames = [driver[0] for driver in cursor.fetchall()]

    # Fetch the list of drivers for the dropdown
    cursor.execute("SELECT DISTINCT driverId FROM qualifying")
    drivers = [str(driver[0]) for driver in cursor.fetchall()]

    if request.method == 'POST':
        selected_surname = request.form.get('selected_surname')

        # Check if the selected surname is not empty or "All Drivers"
        if selected_surname and selected_surname != "All Drivers":
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
                WHERE
                    drivers.surname = %s
                ORDER BY
                    races.date DESC
            """
            cursor.execute(select_query, (selected_surname,))
            result = cursor.fetchall()
            return render_template('qualifying.html', qualifying=result, selected_surname=selected_surname, driver_surnames=driver_surnames, drivers=drivers)
        
        else:
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
                GROUP BY
                    drivers.surname
            """
            cursor.execute(select_query)
            result = cursor.fetchall()
            return render_template('qualifying.html', qualifying=result, selected_surname="All Surnames", driver_surnames=driver_surnames, drivers=drivers)
    else:
        # Initialize selected_surname and selected_driver to empty strings or default values
        selected_surname = ""

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
            ORDER BY
                races.date DESC
        """
        cursor.execute(select_query)
        result = cursor.fetchall()
        return render_template('qualifying.html', qualifying=result, selected_surname=selected_surname, driver_surnames=driver_surnames, drivers=drivers)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
