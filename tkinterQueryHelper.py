import mysql.connector

def get_connection():
    myConnection = mysql.connector.connect(
        user='root',
        password="",
        host='localhost',
        database='Basketball'
    )
    return myConnection

# Function to fetch players from the database
def get_players():
    myConnection = get_connection()
    cursor = myConnection.cursor()
                        
    cursor.execute("SELECT Player_Name FROM Players")
    players = [row[0] for row in cursor.fetchall()]
    myConnection.close()
    
    return players

# Function to fetch top scorers by points per game
def get_top_scorers(number_players, season_year):
    myConnection = get_connection()
    cursor = myConnection.cursor()

    # Get Season_ID
    cursor.execute("SELECT Season_ID FROM Season WHERE Season_ID = %s", (season_year,))
    season_id = cursor.fetchone()[0]

    # Get top scorers from PlayedSeasonWith table by Points Per Game
    cursor.execute("""
        SELECT p.Player_Name, ROUND(psw.Points / psw.Games_Played, 2) AS Points_Per_Game
        FROM PlayedSeasonWith psw
        JOIN Players p ON psw.Player_ID = p.Player_ID
        WHERE psw.Season_ID = %s
        ORDER BY Points_Per_Game DESC
        LIMIT %s
    """, (season_id, number_players))
    
    top_scorers = cursor.fetchall()
    
    myConnection.close()

    return top_scorers

# Function to fetch player stats
def get_player_stats(player_name, season_year):
    myConnection = get_connection()
    cursor = myConnection.cursor()
    
    # Get Player_ID
    cursor.execute("SELECT Player_ID FROM Players WHERE Player_Name = %s", (player_name,))
    player_id = cursor.fetchone()[0]
    
    # Assuming the Season table has a column to identify the start year of the season
    cursor.execute("SELECT Season_ID FROM Season WHERE Season_ID = %s", (season_year,))
    season_id = cursor.fetchone()[0]
    
    # Get Player Stats from PlayedSeasonWith table
    cursor.execute("""
        SELECT Games_Played, Points, Rebounds, Assists, Steals, Blocks
        FROM PlayedSeasonWith
        WHERE Player_ID = %s AND Season_ID = %s
    """, (player_id, season_id))
    stats = cursor.fetchone()
    
    myConnection.close()

    return stats

# Function to fetch teams from the database
def get_teams():
    myConnection = get_connection()
    cursor = myConnection.cursor()

    cursor.execute("SELECT Team_Name FROM Team") 
    teams = [row[0] for row in cursor.fetchall()]
    myConnection.close()

    return teams

# Function to fetch team stats
def get_team_stats(team_name, season_year):
    myConnection = get_connection()
    cursor = myConnection.cursor()

    # Get Team_ID
    cursor.execute("SELECT Team_ID FROM Team WHERE Team_Name = %s", (team_name,))
    team_id = cursor.fetchone()[0]

    # Get Season_ID
    cursor.execute("SELECT Season_ID FROM Season WHERE Season_ID = %s", (season_year,))
    season_id = cursor.fetchone()[0]

    # Get Team Stats from Games table
    cursor.execute("""
        SELECT 
            COUNT(g.Game_ID) AS Games_Played,
            SUM(CASE 
                WHEN g.Home_Team_ID = %s THEN g.Home_Points
                ELSE g.Away_Points
            END) AS Total_Points,
            ROUND(
            AVG(CASE 
                WHEN g.Home_Team_ID = %s THEN g.Home_Points
                ELSE g.Away_Points
            END), 2) AS Points_Per_Game, 
            ROUND(
            AVG(CASE 
                WHEN g.Home_Team_ID = %s THEN g.Away_Points
                ELSE g.Home_Points
            END), 2) AS Points_Allowed_Per_Game,
            SUM(CASE 
                WHEN (g.Home_Team_ID = %s AND g.Home_Win = TRUE) OR (g.Away_Team_ID = %s AND g.Home_Win = FALSE) THEN 1
                ELSE 0
            END) AS Wins,
            SUM(CASE 
                WHEN (g.Home_Team_ID = %s AND g.Home_Win = FALSE) OR (g.Away_Team_ID = %s AND g.Home_Win = TRUE) THEN 1
                ELSE 0
            END) AS Losses
        FROM 
            Games g
        WHERE 
            (g.Home_Team_ID = %s OR g.Away_Team_ID = %s)
            AND g.Season_ID = %s
    """, (team_id, team_id, team_id, team_id, team_id, team_id, team_id, team_id, team_id, season_id))
    
    stats = cursor.fetchone()
    
    myConnection.close()

    return stats

