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

    mock_players = ["Lebron", "Luka", "Anthony Edwards"]
    return mock_players


# Function to fetch player stats
def get_player_stats(player_name, season_year):
    myConnection = get_connection()

    cursor = myConnection.cursor()
    
    # Get Player_ID
    # cursor.execute("SELECT Player_ID FROM Players WHERE Player_Name = %s", (player_name,))
    # player_id = cursor.fetchone()[0]

    # Get Season_ID
    # cursor.execute("SELECT Season_ID FROM Season WHERE YEAR(Season_Start) = %s", (season_year,))
    # season_id = cursor.fetchone()[0]
    
    # Get Player Stats
    # cursor.execute("""
    #     SELECT Games_Played, Field_Goals_2PT, Field_Goals_3PT, Free_Throws, Rebounds, Assists
    #     FROM PlayerSeasonStats
    #     WHERE Player_ID = %s AND Season_ID = %s
    # """, (player_id, season_id))
    # stats = cursor.fetchone()
    
    myConnection.close()

    mock_stats = [5, 10, 10, 10, 10, 10]
    return mock_stats