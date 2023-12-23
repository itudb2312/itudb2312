from flask import Flask, render_template, redirect, url_for, request
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

    # Calculate age based on date of birth
    dob = driver_info[2]
    today = datetime.date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

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
    
            
@app.route('/results')
def results():
    
    select_query = "SELECT * FROM results WHERE resultId < 100"
    cursor.execute(select_query)
    result = cursor.fetchall()

    return render_template('results.html',results=result)

@app.route('/pit_stops')
def pit_stops():
    select_query = "SELECT * FROM pit_stops"
    cursor.execute(select_query)
    result = cursor.fetchall()

    return render_template('pit_stops.html',pit_stops=result)

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

        driverId_query = f"SELECT driverId from drivers WHERE surname='{driver}'"
        cursor.execute(driverId_query)
        driverId = cursor.fetchone()
        driverId = driverId[0]
        cursor.fetchall()

        raceId_query = f"SELECT raceId from races WHERE name='{race}'"
        cursor.execute(raceId_query)
        raceId = cursor.fetchone()
        raceId = raceId[0]
        cursor.fetchall()

        insert_query = """
            INSERT INTO driver_standings (raceId, driverId, points, position, positionText, wins)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query,(raceId , driverId, point, position, position, wins))
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

        driverId_query = f"SELECT driverId from drivers WHERE surname='{driver}'"
        cursor.execute(driverId_query)
        driverId = cursor.fetchone()
        driverId = driverId[0]
        cursor.fetchall()

        raceId_query = f"SELECT raceId from races WHERE name='{race}'"
        cursor.execute(raceId_query)
        raceId = cursor.fetchone()
        raceId = raceId[0]
        cursor.fetchall()

        update_query = """
            UPDATE driver_standings
            SET raceId = %s, driverId = %s, points = %s, position = %s, positionText = %s, wins = %s
            WHERE driverStandingsId = %s
        """
        cursor.execute(update_query, (raceId, driverId, point, position, position, wins, driverStandingId))
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

        driverId_query = f"SELECT driverId from drivers WHERE surname='{driver}'"
        cursor.execute(driverId_query)
        driverId = cursor.fetchone()
        driverId = driverId[0]
        cursor.fetchall()

        raceId_query = f"SELECT raceId from races WHERE name='{race}'"
        cursor.execute(raceId_query)
        raceId = cursor.fetchone()
        raceId = raceId[0]
        cursor.fetchall()

        constructorId_query = f"SELECT constructorId from constructors WHERE name='{constructor}'"
        cursor.execute(constructorId_query)
        constructorId = cursor.fetchone()
        constructorId = constructorId[0]
        cursor.fetchall()

        insert_query = """
            INSERT INTO sprint_results (raceId, driverId, constructorId, number, position, 
            positionText, points, laps, time, fastestLap, fastestLapTime)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (raceId, driverId, constructorId, number, position, position, points, laps, time, fastest_lap, fastest_lap_time))
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

        driverId_query = f"SELECT driverId from drivers WHERE surname='{driver}'"
        cursor.execute(driverId_query)
        driverId = cursor.fetchone()
        driverId = driverId[0]
        cursor.fetchall()

        raceId_query = f"SELECT raceId from races WHERE name='{race}'"
        cursor.execute(raceId_query)
        raceId = cursor.fetchone()
        raceId = raceId[0]
        cursor.fetchall()

        constructorId_query = f"SELECT constructorId from constructors WHERE name='{constructor}'"
        cursor.execute(constructorId_query)
        constructorId = cursor.fetchone()
        constructorId = constructorId[0]
        cursor.fetchall()

        update_query = """
            UPDATE sprint_results
            SET driverId = %s, raceId = %s, constructorId = %s, number = %s, position = %s, positionText = %s, 
            points = %s, laps = %s, time = %s, fastestLap=%s, fastestLapTime=%s 
            WHERE resultId = %s
        """
        cursor.execute(update_query, (driverId, raceId, constructorId, number, position, position, points, laps, time, fastest_lap, fastest_lap_time, resultId))
        db.commit()

        return redirect(url_for('sprint_results'))



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
