CREATE DATABASE Basketball;
USE Basketball;

CREATE TABLE Players (
    Player_ID INT PRIMARY KEY,
    Player_Name VARCHAR(100) NOT NULL,
    Birthdate DATE NOT NULL,
    School VARCHAR(100) NOT NULL,
    Country VARCHAR(100) NOT NULL,
    Draft_Year INT,
    Draft_Round INT 
);

CREATE TABLE Team (
    Team_ID INT PRIMARY KEY,
    Team_Name VARCHAR(100) NOT NULL,
    Abbreviation VARCHAR(5) NOT NULL,
    City VARCHAR(100) NOT NULL,
    Year_Founded INT NOT NULL
);

CREATE TABLE Season (
	Season_ID INT PRIMARY KEY
); 

CREATE TABLE PlayedSeasonWith (
    Player_ID INT,
    Season_ID INT NOT NULL,
    Team_ID INT,
    Age INT NOT NULL,
    Games_Played INT, -- GP
    Points INT NOT NULL, 
    Rebounds INT NOT NULL, -- REB
    Assists INT NOT NULL, -- AST
    Steals INT NOT NULL,
    Blocks INT NOT NULL,
    PRIMARY KEY (Player_ID, Season_ID, Team_ID),
    FOREIGN KEY (Player_ID) REFERENCES Players(Player_ID),
    FOREIGN KEY (Season_ID) REFERENCES Season(Season_ID),
    FOREIGN KEY (Team_ID) REFERENCES Team(Team_ID)
);

CREATE TABLE Coaches (
    Coach_ID INT PRIMARY KEY,
    Coach_Name VARCHAR(100) NOT NULL
);

CREATE TABLE Arenas (
	Arena_ID INT PRIMARY KEY,
    Arena_Name VARCHAR(100),
    Capacity INT NOT NULL
);

CREATE TABLE Games (
    Game_ID INT PRIMARY KEY,
    Season_ID INT,
    Game_Date DATE NOT NULL,
    Season_Type VARCHAR(100) NOT NULL,
    Home_Points INT NOT NULL,
    Away_Points INT NOT NULL,
    Home_Team_ID INT,
    Away_Team_ID INT,
    Home_Win BOOLEAN NOT NULL,
    FOREIGN KEY (Season_ID) REFERENCES Season(Season_ID),
    FOREIGN KEY (Home_Team_ID) REFERENCES Team(Team_ID),
    FOREIGN KEY (Away_Team_ID) REFERENCES Team(Team_ID)
);

CREATE TABLE Referees (
    Official_ID INT PRIMARY KEY,
    Referee_Name VARCHAR(100) NOT NULL
);

CREATE TABLE CoachesTeam (
    Coach_ID INT,
    Team_ID INT,
    Start_Date DATE NOT NULL,
    End_Date DATE NOT NULL,
    PRIMARY KEY (Coach_ID, Team_ID, Start_Date),
    FOREIGN KEY (Coach_ID) REFERENCES Coaches(Coach_ID),
    FOREIGN KEY (Team_ID) REFERENCES Team(Team_ID)
);

CREATE TABLE CoachedIn ( -- DONT KNOW IF WE HAVE THIS DATA
    Coach_ID INT,
    Game_ID INT,
    PRIMARY KEY (Coach_ID, Game_ID),
    FOREIGN KEY (Coach_ID) REFERENCES Coaches(Coach_ID),
    FOREIGN KEY (Game_ID) REFERENCES Games(Game_ID)
);

CREATE TABLE HomeVenue (
    Team_ID INT,
    Arena_ID INT,
    PRIMARY KEY (Team_ID, Arena_ID),
    FOREIGN KEY (Team_ID) REFERENCES Team(Team_ID),
    FOREIGN KEY (Arena_ID) REFERENCES Arenas(Arena_ID)
);

CREATE TABLE Officiates (
    Official_ID INT,
    Game_ID INT,
    Jersey_Number INT,
    PRIMARY KEY (Official_ID, Game_ID),
    FOREIGN KEY (Official_ID) REFERENCES Referees(Official_ID),
    FOREIGN KEY (Game_ID) REFERENCES Games(Game_ID)
);
