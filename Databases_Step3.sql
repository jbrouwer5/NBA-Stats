CREATE DATABASE Basketball;
USE Basketball;

CREATE TABLE Players (
    Player_ID INT PRIMARY KEY,
    Player_Name VARCHAR(100) NOT NULL,
    Birthdate DATE NOT NULL,
    School VARCHAR(100) NOT NULL,
    Country VARCHAR(100) NOT NULL,
    Draft_Year INT NOT NULL,
    Draft_Round INT NOT NULL
);

CREATE TABLE Team (
    Team_ID INT PRIMARY KEY,
    Team_Name VARCHAR(100) NOT NULL,
    Abrreviation VARCHAR(5) NOT NULL,
    City VARCHAR(100) NOT NULL,
    Year_Founded INT NOT NULL,
);


CREATE TABLE Season (
	Season_ID INT PRIMARY KEY,
    Season_Start DATE,
    Season_End DATE
);

CREATE TABLE PlayerSeasonStats (
    Player_ID INT,
    Season_ID INT,
    Team_ID INT,
    Jersey_Number INT NOT NULL,
    Games_Played INT, -- GP
    Field_Goals_2PT INT NOT NULL, -- FGM
    Field_Goals_3PT INT NOT NULL, -- FG3M
    Free_Throws INT NOT NULL, -- FTM
    Rebounds INT NOT NULL, -- REB
    Assists INT NOT NULL, -- AST
    PRIMARY KEY (Player_ID, Season_ID),
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
    Capacity INT NOT NULL,
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
    Referee_Name VARCHAR(100) NOT NULL,
);


CREATE TABLE PlayedFor (
    Player_ID INT,
    Team_ID INT,
    Play_Start INT NOT NULL,
    Play_End INT,
    PRIMARY KEY (Player_ID, Team_ID, Contract_Start),
    FOREIGN KEY (Player_ID) REFERENCES Players(Player_ID),
    FOREIGN KEY (Team_ID) REFERENCES Team(Team_ID)
);

CREATE TABLE CoachesTeam (
    Coach_ID INT,
    Team_ID INT,
    Start_Date DATE NOT NULL,
    End_Date DATE NOT NULL,
    PRIMARY KEY (Coach_ID, Team_ID),
    FOREIGN KEY (Coach_ID) REFERENCES Coaches(Coach_ID),
    FOREIGN KEY (Team_ID) REFERENCES Team(Team_ID)
);

CREATE TABLE CoachedIn (
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

CREATE TABLE TakesPlaceIn (
    Game_ID INT,
    Arena_ID INT,
    PRIMARY KEY (Game_ID, Arena_ID),
    FOREIGN KEY (Game_ID) REFERENCES Games(Game_ID),
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
