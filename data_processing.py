import pandas as pd
import numpy as np
import sqlite3
from unidecode import unidecode
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import mplcursors
from data_scraping import scrape_team_data

# Database connection
conn = sqlite3.connect(
    "/Users/moheeb/Documents/Personal_Project_ideas/Premier_league_squads.db"
)


def clean_and_store_fifa_data(fifa_player_data_path, db_connection):
    # Read CSV file into a pandas DataFrame
    fifa_player_data_df = pd.read_csv(fifa_player_data_path, encoding="utf-8")

    # Clean player names
    def clean_name(name):
        return unidecode(name)

    fifa_player_data_df["Player_Name"] = fifa_player_data_df["Player_Name"].apply(
        clean_name
    )

    # Splitting first and last name
    def split_name(name):
        parts = name.split()
        first_name = parts[0]
        last_name = " ".join(parts[1:])
        return first_name, last_name

    fifa_player_data_df[["First_Name_initial", "Last_Name"]] = fifa_player_data_df[
        "Player_Name"
    ].apply(lambda x: pd.Series(split_name(x)))
    fifa_player_data_df["First_Name_initial"] = fifa_player_data_df[
        "First_Name_initial"
    ].str.title()
    fifa_player_data_df["Last_Name"] = fifa_player_data_df["Last_Name"].str.title()

    # Save the cleaned DataFrame to an SQLite table
    fifa_player_data_df.to_sql(
        "fifa_player_data", db_connection, if_exists="replace", index=False
    )

    # print(fifa_player_data_df.columns)


# Example usage
fifa_player_data_path = "/Users/moheeb/Documents/Personal_Project_ideas/fifa_23_280922.csv"  # Replace with your CSV file path
clean_and_store_fifa_data(fifa_player_data_path, conn)


# Cleaning and manipulating the 7 Premier League teams dataframe.


# Function to clean names
def clean_name(name):
    return unidecode(name)


# Function to create first name initial
def create_first_name_initial(row):
    if pd.notna(row["First_Name"]):
        return row["First_Name"][0] + ". "
    else:
        return ""


# Function to process each team's data
def process_team_data(team_name, file_path, db_connection):
    df = pd.read_csv(file_path, encoding="utf-8")
    df["Last_Name"] = df["Last_Name"].apply(clean_name)
    df["First_Name_initial"] = df.apply(create_first_name_initial, axis=1).str.strip()
    df["Club_Name"] = team_name
    df.to_sql(
        team_name.lower().replace(" ", "_") + "_squad",
        db_connection,
        if_exists="replace",
        index=False,
    )
    return df


# Dictionary of teams and their respective file paths
teams_file_paths = {
    "Arsenal": "/Users/moheeb/Documents/Personal_Project_ideas/arsenal_squad.csv",
    "Manchester City": "/Users/moheeb/Documents/Personal_Project_ideas/manchester_city_squad.csv",
    "Liverpool": "/Users/moheeb/Documents/Personal_Project_ideas/liverpool_squad.csv",
    "Manchester United": "/Users/moheeb/Documents/Personal_Project_ideas/manchester_united_squad.csv",
    "Chelsea": "/Users/moheeb/Documents/Personal_Project_ideas/chelsea_squad.csv",
    "Newcastle United": "/Users/moheeb/Documents/Personal_Project_ideas/newcastle_united_squad.csv",
    "Tottenham Hotspur": "/Users/moheeb/Documents/Personal_Project_ideas/tottenham_hotspur_squad.csv",
}

# Process each team's data
team_df = {}
for team, path in teams_file_paths.items():
    for team, path in teams_file_paths.items():
        team_df = process_team_data(team, path, conn)
        # print(f"{team} DataFrame head:")
        # print(team_df.head())
        # print(team_df.columns)
        # print()


# Function to execute SQL queries and print results
def execute_sql_query(conn, table_name):
    cursor = conn.cursor()
    query = f"""SELECT DISTINCT {table_name}.First_Name, {table_name}.First_Name_initial, {table_name}.Last_Name, {table_name}.Club_Name, fifa_player_data.Player_Nationality, {table_name}.Player_Position,fifa_player_data.Overall_Rating, fifa_player_data.Potential_Rating, fifa_player_data.Average_Performance_Rating, fifa_player_data."Player_Value_(M)", fifa_player_data."Player_Salary_(K)", fifa_player_data.Speed_Rating, fifa_player_data.Endurance_Rating, fifa_player_data.Offensive_Positioning, fifa_player_data.Defensive_Consciousness, fifa_player_data.Effectiveness_Rating, fifa_player_data.GK_Diving, fifa_player_data.GK_Hand_Game, fifa_player_data.GK_Foot_Game, fifa_player_data.GK_Positioning, fifa_player_data.GK_Reflexes, fifa_player_data.Finishing_Rating, fifa_player_data.Heading_Rating, fifa_player_data.Voleys_Rating FROM fifa_player_data INNER JOIN {table_name} ON fifa_player_data.First_Name_initial = {table_name}.First_Name_initial AND fifa_player_data.Last_Name = {table_name}.Last_Name AND fifa_player_data.Player_Nationality = {table_name}.Player_Nationality AND fifa_player_data.Club_Name = {table_name}.Club_Name;"""
    cursor.execute(query)
    return cursor.fetchall()
    conn.close()


# Execute the query for each team
arsenal_results = execute_sql_query(conn, "arsenal_squad")
man_city_results = execute_sql_query(conn, "manchester_city_squad")
liverpool_results = execute_sql_query(conn, "liverpool_squad")
man_united_results = execute_sql_query(conn, "manchester_united_squad")
chelsea_results = execute_sql_query(conn, "chelsea_squad")
newcastle_results = execute_sql_query(conn, "newcastle_united_squad")
tottenham_results = execute_sql_query(conn, "tottenham_hotspur_squad")

team_results_dict = {
    "Arsenal": arsenal_results,
    "Manchester City": man_city_results,
    "Liverpool": liverpool_results,
    "Manchester United": man_united_results,
    "Chelsea": chelsea_results,
    "Newcastle United": newcastle_results,
    "Tottenham Hotspur": tottenham_results,
}


for team_name, team_data in team_results_dict.items():
    print(f"All players in {team_name} and found in FIFA player data:")
    for row in team_data:
        print(
            row[0],  # First Name
            row[1],  # Full_Initial_Name
            row[2],  # Last Name
            row[3],  # Club Name
            row[4],  # Player Nationality
            row[5],  # Player Position
            row[6],  # Overall Rating
            row[7],  # Potential Rating
            row[8],  # Average Performance Rating
            row[9],  # Player Value
            row[10],  # Player Salary
            row[11],  # Speed Rating
            row[12],  # Endurance Rating
            row[13],  # Offensive Positioning
            row[14],  # Defensive Consciousness
            row[15],  # Effectiveness Rating
            row[16],  # GK_Diving
            row[17],  # GK_Hand_Game
            row[18],  # GK_Foot_Game
            row[19],  # GK_Positioning
            row[20],  # GK_Reflexes
            row[21],  # Finishing ability
            row[22],  # Heading ability
            row[23],  # Voleying ability
        )
    print("\n")


def execute_sql_query_for_missing_players(conn, table_name):
    cursor = conn.cursor()
    query = f"""
        SELECT 
            {table_name}.First_Name,
            {table_name}.First_Name_initial,
            {table_name}.Last_Name,
            {table_name}.Player_Nationality
        FROM 
            {table_name}
        LEFT JOIN 
            fifa_player_data
        ON 
            fifa_player_data.First_Name_initial = {table_name}.First_Name_initial
            AND fifa_player_data.Last_Name = {table_name}.Last_Name
            AND fifa_player_data.Player_Nationality = {table_name}.Player_Nationality
        WHERE 
            fifa_player_data.Player_Name IS NULL;
    """
    cursor.execute(query)
    missing_players = cursor.fetchall()

    if not missing_players:
        print(f"All players in {table_name} are found in FIFA player data.")
    else:
        print(f"Players in {table_name} not found in FIFA player data:")
        for player in missing_players:
            print(
                f"First Name: {player[0]}, Initial: {player[1]}, Last Name: {player[2]}, Nationality: {player[3]}"
            )


# Execute the query for each team
team_tables = [
    "arsenal_squad",
    "manchester_city_squad",
    "liverpool_squad",
    "manchester_united_squad",
    "chelsea_squad",
    "newcastle_united_squad",
    "tottenham_hotspur_squad",
]

for team_table in team_tables:
    execute_sql_query_for_missing_players(conn, team_table)
