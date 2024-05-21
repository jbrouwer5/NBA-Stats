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

# Function to fetch the teams a player has played for along with the years
def get_player_teams(player_name):
    myConnection = get_connection()
    cursor = myConnection.cursor()

    # Get Player_ID
    cursor.execute("SELECT Player_ID FROM Players WHERE Player_Name = %s", (player_name,))
    player_id = cursor.fetchone()[0]
    
    # Fetch teams and seasons
    cursor.execute("""
        SELECT t.Team_Name, s.Season_ID
        FROM PlayedSeasonWith psw
        JOIN Team t ON psw.Team_ID = t.Team_ID
        JOIN Season s ON psw.Season_ID = s.Season_ID
        WHERE psw.Player_ID = %s
        ORDER BY s.Season_ID
    """, (player_id,))
    
    player_teams = cursor.fetchall()
    
    myConnection.close()

    return player_teams

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
    
    if stats is None: 
        return stats 
    
    # Calculate per-game statistics
    games_played = stats[0]
    ppg = round(stats[1] / games_played, 1) if games_played else 0
    rpg = round(stats[2] / games_played, 1) if games_played else 0
    apg = round(stats[3] / games_played, 1) if games_played else 0
    spg = round(stats[4] / games_played, 1) if games_played else 0
    bpg = round(stats[5] / games_played, 1) if games_played else 0
    
    return (games_played, ppg, rpg, apg, spg, bpg)
    


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
            END), 1) AS Points_Per_Game, 
            ROUND(
            AVG(CASE 
                WHEN g.Home_Team_ID = %s THEN g.Away_Points
                ELSE g.Home_Points
            END), 1) AS Points_Allowed_Per_Game,
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

# Function to fetch a player's career stats
def get_player_career_stats(player_name):
    myConnection = get_connection()
    cursor = myConnection.cursor()
    
    # Get Player_ID
    cursor.execute("SELECT Player_ID FROM Players WHERE Player_Name = %s", (player_name,))
    player_id = cursor.fetchone()[0]
    
    # Get Player Career Stats from PlayedSeasonWith table
    cursor.execute("""
        SELECT 
            SUM(Games_Played) AS Total_Games_Played,
            SUM(Points) AS Total_Points,
            SUM(Rebounds) AS Total_Rebounds,
            SUM(Assists) AS Total_Assists,
            SUM(Steals) AS Total_Steals,
            SUM(Blocks) AS Total_Blocks
        FROM PlayedSeasonWith
        WHERE Player_ID = %s
    """, (player_id,))
    
    career_stats = cursor.fetchone()

    career_stats = (career_stats[0], career_stats[1], career_stats[2], career_stats[3], career_stats[4], career_stats[5], 
                    round(career_stats[1] / career_stats[0], 1), round(career_stats[2] / career_stats[0], 1), 
                    round(career_stats[3] / career_stats[0], 1), round(career_stats[4] / career_stats[0], 1), 
                    round(career_stats[5] / career_stats[0], 1))
    
    myConnection.close()
    
    return career_stats

def get_champion_data():

    myConnection = get_connection()
    cursor = myConnection.cursor()

    # Get Player_ID
    cursor.execute("""SELECT 
                    t.Team_Name,
                    s.Season_ID,
                    COUNT(g.Game_ID) AS Games_Played,
                    SUM(CASE WHEN g.Home_Team_ID = s.Winner_ID THEN g.Home_Points ELSE g.Away_Points END) AS Points_Scored,
                    SUM(CASE WHEN g.Home_Team_ID = s.Winner_ID THEN g.Away_Points ELSE g.Home_Points END) AS Points_Allowed,
                    SUM(CASE WHEN g.Home_Team_ID = s.Winner_ID AND g.Home_Win = 1 THEN 1
                            WHEN g.Away_Team_ID = s.Winner_ID AND g.Home_Win = 0 THEN 1 ELSE 0 END) AS Wins,
                    SUM(CASE WHEN g.Home_Team_ID = s.Winner_ID AND g.Home_Win = 0 THEN 1
                            WHEN g.Away_Team_ID = s.Winner_ID AND g.Home_Win = 1 THEN 1 ELSE 0 END) AS Losses
                FROM 
                    Season s
                JOIN 
                    Team t ON s.Winner_ID = t.Team_ID
                JOIN 
                    Games g ON (g.Home_Team_ID = s.Winner_ID OR g.Away_Team_ID = s.Winner_ID) AND YEAR(g.Game_Date) = s.Season_ID
                WHERE 
                    s.Season_ID BETWEEN 1946 AND 2023
                GROUP BY 
                    t.Team_Name, s.Season_ID
                ORDER BY
                    s.Season_ID DESC;
    """)
    stats = cursor.fetchall()
    myConnection.close()

    return stats
    
def get_all_time_scorers():

    myConnection = get_connection()
    cursor = myConnection.cursor()

    # Get Player_ID
    cursor.execute("""
                    SELECT p.Player_Name, SUM(psw.Points) AS Total_Points
                    FROM PlayedSeasonWith psw
                    JOIN Players p ON psw.Player_ID = p.Player_ID
                    GROUP BY p.Player_Name
                    ORDER BY Total_Points DESC
                    LIMIT 10
                """)
    stats = cursor.fetchall()
    myConnection.close()

    return stats

def get_biased_refs():

    myConnection = get_connection()
    cursor = myConnection.cursor()

    # Get Player_ID
    cursor.execute("""
                    SELECT 
                r.Referee_Name,
                COUNT(CASE WHEN g.Home_Win = 1 THEN 1 END) AS Home_Wins_Officiated,
                COUNT(*) AS Total_Games_Officiated,
                (COUNT(CASE WHEN g.Home_Win = 1 THEN 1 END) * 100.0 / COUNT(*)) AS Home_Win_Percentage
            FROM 
                Officiates o
            JOIN 
                Games g ON o.Game_ID = g.Game_ID
            JOIN 
                Referees r ON o.Official_ID = r.Official_ID
            GROUP BY 
                r.Referee_Name
            HAVING
                COUNT(*) > 100
            ORDER BY 
                Home_Win_Percentage DESC
            LIMIT 10;
                """)
    stats = cursor.fetchall()
    myConnection.close()

    return stats


def get_top_champions():

    myConnection = get_connection()
    cursor = myConnection.cursor()

    cursor.execute("""
                    SELECT 
                    s.Season_ID,
                    t.Team_Name as Champion,
                    p.Player_Name as HighestScoringPlayer,
                    psw.Points as HighestScoringPlayerPoints
                FROM Season s
                JOIN Team t ON s.Winner_ID = t.Team_ID
                JOIN PlayedSeasonWith psw ON s.Season_ID = psw.Season_ID AND s.Winner_ID = psw.Team_ID
                JOIN  Players p ON psw.Player_ID = p.Player_ID
                WHERE 
                    (psw.Season_ID, psw.Team_ID, psw.Points) IN (
                        SELECT 
                            psw.Season_ID,
                            psw.Team_ID,
                            MAX(psw.Points)
                        FROM 
                            PlayedSeasonWith psw
                        JOIN Season s ON psw.Season_ID = s.Season_ID
                        GROUP BY 
                            psw.Season_ID, psw.Team_ID
                    )
                ORDER BY 
                    s.Season_ID DESC;
                   """)
    
    stats = cursor.fetchall()
    myConnection.close()

    return stats

def get_winningest_arenas():
    myConnection = get_connection()
    cursor = myConnection.cursor()

    cursor.execute("""
            SELECT 
            a.Arena_Name,
            a.Capacity,
            COUNT(CASE WHEN g.Home_Win = 1 THEN 1 END) AS Home_Wins,
            COUNT(*) AS Total_Games_Hosted,
            (COUNT(CASE WHEN g.Home_Win = 1 THEN 1 END) * 100.0 / COUNT(*)) AS Home_Win_Percentage
        FROM 
            Games g
        JOIN 
            Arenas a ON g.Arena_ID = a.Arena_ID
        GROUP BY 
            a.Arena_Name, a.Capacity
        ORDER BY 
            Home_Win_Percentage DESC;""")
    
    stats = cursor.fetchall()
    myConnection.close()

    return stats

