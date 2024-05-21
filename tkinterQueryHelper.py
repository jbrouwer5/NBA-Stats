import mysql.connector

def get_connection():
    
    myConnection = mysql.connector.connect( user = 'root',
    password = "",
    host = 'localhost',
    database = 'Basketball')

    return myConnection

# Function to fetch players from the database
def get_players():
    myConnection = get_connection()

    cursor = myConnection.cursor()
                        
    cursor.execute("SELECT Player_Name FROM Players")
    players = [row[0] for row in cursor.fetchall()]
    myConnection.close()
    
    return players


# Function to fetch player stats
def get_player_stats(player_name, season_year):
    myConnection = get_connection()

    cursor = myConnection.cursor()
    
    # Get Player_ID
    cursor.execute("SELECT Player_ID FROM Players WHERE Player_Name = %s", (player_name,))
    player_id = cursor.fetchone()[0]
    print(player_id)
    # Assuming the Season table has a column to identify the start year of the season
    cursor.execute("SELECT Season_ID FROM Season WHERE Season_ID = %s", (season_year,))
    season_id = cursor.fetchone()[0]
    print(season_id)
    # Get Player Stats from PlayedSeasonWith table
    cursor.execute("""
        SELECT Games_Played, Points, Rebounds, Assists, Steals, Blocks
        FROM PlayedSeasonWith
        WHERE Player_ID = %s AND Season_ID = %s
    """, (player_id, season_id))
    stats = cursor.fetchone()
    
    myConnection.close()

    return stats
