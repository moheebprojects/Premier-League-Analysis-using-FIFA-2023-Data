import pandas as pd
import numpy as np
from unidecode import unidecode
import sqlite3
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import mplcursors


# Create a new SQLite database (or connect to an existing one)
conn = sqlite3.connect(
    "/Users/moheeb/Documents/Personal_Project_ideas/Premier_league_squads/Premier_league_squads.db"
)


################################################################################################################################################
######################################################################## FIFA 2023 PLAYER DATA #################################################
################################################################################################################################################
# Reading fifa 2023 player data CSV file into a pandas DataFrame

fifa_player_data_df = pd.read_csv(
    "/Users/moheeb/Documents/Personal_Project_ideas/Premier_league_squads/fifa_23_280922.csv",
    encoding="utf-8",
)


# print(fifa_player_data_df)

###################################################Cleaning Data##################################################

### unidecode library to remove accents and convert special characters to their closest ASCII representation.


def clean_name(name):
    return unidecode(name)


fifa_player_data_df["Player_Name"] = fifa_player_data_df["Player_Name"].apply(
    clean_name
)


###Splitting first and last name into two


def split_name(name):
    parts = name.split()
    first_name = parts[0]
    last_name = " ".join(parts[1:])  # Join the remaining parts as the last name
    return first_name, last_name


fifa_player_data_df[["First_Name_initial", "Last_Name"]] = fifa_player_data_df[
    "Player_Name"
].apply(lambda x: pd.Series(split_name(x)))

fifa_player_data_df["First_Name_initial"] = fifa_player_data_df[
    "First_Name_initial"
].str.title()
fifa_player_data_df["Last_Name"] = fifa_player_data_df["Last_Name"].str.title()


# print(fifa_player_data_df.columns)


###############Use the 'to_sql' method to write the DataFrame to an SQLite table###############

fifa_player_data_df.to_sql("fifa_player_data", conn, if_exists="replace", index=False)


################################################################################################################################################
######################################################################## ARSENAL SQUAD 2023/2024########################################
################################################################################################################################################


# Reading arsenal_ CSV file into a pandas DataFrame
arsenal_df = pd.read_csv(
    "/Users/moheeb/Documents/Personal_Project_ideas/Premier_league_squads/arsenal_squad.csv",
    encoding="utf-8",
)

############--------------------Cleaning arsenal_ Data ----------------------


def clean_name(name):
    return unidecode(name)


arsenal_df["Last_Name"] = arsenal_df["Last_Name"].apply(clean_name)


# Define a custom function to create the "First_Name_initial" column
def create_first_name_initial(arsenal_row):
    if pd.notna(arsenal_row["First_Name"]):
        return arsenal_row["First_Name"][0] + ". "
    else:
        return ""


# Apply the custom function to create the "First_Name_initial" column
arsenal_df["First_Name_initial"] = arsenal_df.apply(create_first_name_initial, axis=1)

arsenal_df["First_Name_initial"] = arsenal_df["First_Name_initial"].str.strip()

# Adding a column with the column name

arsenal_df["Club_Name"] = "Arsenal"


# print(arsenal_df)


# ------------------------------------------------------------------------------------------------------------------------------------------

# Use the 'to_sql' method to write the DataFrame to an SQLite table
arsenal_df.to_sql("arsenal_squad", conn, if_exists="replace", index=False)

# print(arsenal_df)

# print(arsenal_df.columns)
# print(arsenal_df[["First_Name_initial", "Last_Name", "player_nationality"]])


# Create a cursor
arsenal_cursor = conn.cursor()

# Execute SQL queries
arsenal_cursor.execute(
    """SELECT DISTINCT arsenal_squad.First_Name, arsenal_squad.First_Name_initial, arsenal_squad.Last_Name, arsenal_squad.Club_Name, fifa_player_data.Player_Nationality, arsenal_squad.Player_Position,fifa_player_data.Overall_Rating, fifa_player_data.Potential_Rating, fifa_player_data.Average_Performance_Rating, fifa_player_data."Player_Value_(M)", fifa_player_data."Player_Salary_(K)", fifa_player_data.Speed_Rating, fifa_player_data.Endurance_Rating, fifa_player_data.Offensive_Positioning, fifa_player_data.Defensive_Consciousness, fifa_player_data.Effectiveness_Rating, fifa_player_data.GK_Diving, fifa_player_data.GK_Hand_Game, fifa_player_data.GK_Foot_Game, fifa_player_data.GK_Positioning, fifa_player_data.GK_Reflexes, fifa_player_data.Finishing_Rating, fifa_player_data.Heading_Rating, fifa_player_data.Voleys_Rating
FROM fifa_player_data
INNER JOIN arsenal_squad
ON fifa_player_data.First_Name_initial = arsenal_squad.First_Name_initial AND fifa_player_data.Last_Name = arsenal_squad.Last_Name AND fifa_player_data.Player_Nationality = arsenal_squad.Player_Nationality AND fifa_player_data.Club_Name = arsenal_squad.Club_Name;"""
)


# Fetch all the results into a list
arsenal_results = arsenal_cursor.fetchall()


# Print the results with padding to align in columns
for row in arsenal_results:
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

if not arsenal_results:
    print("No results found.")


# Create a set of full names and last names for players retrieved in the SQLite query
arsenal_retrieved_players = set((row[1], row[2]) for row in arsenal_results)

# Filter the arsenal_df DataFrame to get rows not retrieved
arsenal_unretrieved_players_df = arsenal_df[
    ~arsenal_df.apply(
        lambda row: (row["First_Name_initial"], row["Last_Name"])
        in arsenal_retrieved_players,
        axis=1,
    )
]

# Print the unretrieved players
if not arsenal_unretrieved_players_df.empty:
    print(
        arsenal_unretrieved_players_df[
            [
                "First_Name",
                "First_Name_initial",
                "Last_Name",
                "Player_Nationality",
            ]
        ]
    )
else:
    print("All team players retrieved")


# Close the cursor and the connection
arsenal_cursor.close()


################################################################################################################################################
######################################################################## man_city_ SQUAD 2023/2024########################################
################################################################################################################################################


# Reading man_city_ CSV file into a pandas DataFrame
man_city_df = pd.read_csv(
    "/Users/moheeb/Documents/Personal_Project_ideas/Premier_league_squads/man_city_squad.csv",
    encoding="utf-8",
)

############--------------------Cleaning man_city_ Data ----------------------


def clean_name(name):
    return unidecode(name)


man_city_df["Last_Name"] = man_city_df["Last_Name"].apply(clean_name)


# Define a custom function to create the "First_Name_initial" column
def create_first_name_initial(man_city_row):
    if pd.notna(man_city_row["First_Name"]):
        return man_city_row["First_Name"][0] + ". "
    else:
        return ""


# Apply the custom function to create the "First_Name_initial" column
man_city_df["First_Name_initial"] = man_city_df.apply(create_first_name_initial, axis=1)

man_city_df["First_Name_initial"] = man_city_df["First_Name_initial"].str.strip()

# Adding a column with the column name

man_city_df["Club_Name"] = "Manchester City"


# print(man_city_df)


# ------------------------------------------------------------------------------------------------------------------------------------------

# Use the 'to_sql' method to write the DataFrame to an SQLite table
man_city_df.to_sql("man_city_squad", conn, if_exists="replace", index=False)

# print(man_city_df)

# print(man_city_df.columns)
# print(man_city_df[["First_Name_initial", "Last_Name", "player_nationality"]])


# Create a cursor
man_city_cursor = conn.cursor()

# Execute SQL queries
man_city_cursor.execute(
    """SELECT DISTINCT man_city_squad.First_Name, man_city_squad.First_Name_initial, man_city_squad.Last_Name, man_city_squad.Club_Name, fifa_player_data.Player_Nationality, man_city_squad.Player_Position, fifa_player_data.Overall_Rating, fifa_player_data.Potential_Rating, fifa_player_data.Average_Performance_Rating, fifa_player_data."Player_Value_(M)", fifa_player_data."Player_Salary_(K)", fifa_player_data.Speed_Rating, fifa_player_data.Endurance_Rating, fifa_player_data.Offensive_Positioning, fifa_player_data.Defensive_Consciousness, fifa_player_data.Effectiveness_Rating,  fifa_player_data.GK_Diving, fifa_player_data.GK_Hand_Game, fifa_player_data.GK_Foot_Game, fifa_player_data.GK_Positioning, fifa_player_data.GK_Reflexes, fifa_player_data.Finishing_Rating, fifa_player_data.Heading_Rating, fifa_player_data.Voleys_Rating
FROM fifa_player_data
INNER JOIN man_city_squad
ON fifa_player_data.First_Name_initial = man_city_squad.First_Name_initial AND fifa_player_data.Last_Name = man_city_squad.Last_Name AND fifa_player_data.Player_Nationality = man_city_squad.Player_Nationality AND fifa_player_data.Club_Name = man_city_squad.Club_Name;"""
)


# Fetch all the results into a list
man_city_results = man_city_cursor.fetchall()


# Print the results with padding to align in columns
for row in man_city_results:
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

if not man_city_results:
    print("No results found.")


# Create a set of full names and last names for players retrieved in the SQLite query
man_city_retrieved_players = set((row[1], row[2]) for row in man_city_results)

# Filter the man_city_df DataFrame to get rows not retrieved
man_city_unretrieved_players_df = man_city_df[
    ~man_city_df.apply(
        lambda row: (row["First_Name_initial"], row["Last_Name"])
        in man_city_retrieved_players,
        axis=1,
    )
]

# Print the unretrieved players
if not man_city_unretrieved_players_df.empty:
    print(
        man_city_unretrieved_players_df[
            [
                "First_Name",
                "First_Name_initial",
                "Last_Name",
                "Player_Nationality",
            ]
        ]
    )
else:
    print("All team players retrieved")


# Close the cursor and the connection
man_city_cursor.close()


################################################################################################################################################
######################################################################## LIVERPOOL SQUAD 2023/2024########################################
################################################################################################################################################

# Reading liverpool_ CSV file into a pandas DataFrame
liverpool_df = pd.read_csv(
    "/Users/moheeb/Documents/Personal_Project_ideas/Premier_league_squads/liverpool_squad.csv",
    encoding="utf-8",
)

############--------------------Cleaning liverpool_ Data ----------------------


def clean_name(name):
    return unidecode(name)


liverpool_df["Last_Name"] = liverpool_df["Last_Name"].apply(clean_name)


# Define a custom function to create the "First_Name_initial" column
def create_first_name_initial(liverpool_row):
    if pd.notna(liverpool_row["First_Name"]):
        return liverpool_row["First_Name"][0] + ". "
    else:
        return ""


# Apply the custom function to create the "First_Name_initial" column
liverpool_df["First_Name_initial"] = liverpool_df.apply(
    create_first_name_initial, axis=1
)

liverpool_df["First_Name_initial"] = liverpool_df["First_Name_initial"].str.strip()

# Adding a column with the column name

liverpool_df["Club_Name"] = "Liverpool"


# print(liverpool_df)


# ------------------------------------------------------------------------------------------------------------------------------------------

# Use the 'to_sql' method to write the DataFrame to an SQLite table
liverpool_df.to_sql("liverpool_squad", conn, if_exists="replace", index=False)

# print(liverpool_df)

# print(liverpool_df.columns)
# print(liverpool_df[["First_Name_initial", "Last_Name", "player_nationality"]])


# Create a cursor
liverpool_cursor = conn.cursor()

# Execute SQL queries
liverpool_cursor.execute(
    """SELECT DISTINCT liverpool_squad.First_Name, liverpool_squad.First_Name_initial, liverpool_squad.Last_Name, liverpool_squad.Club_Name, fifa_player_data.Player_Nationality, liverpool_squad.Player_Position, fifa_player_data.Overall_Rating, fifa_player_data.Potential_Rating, fifa_player_data.Average_Performance_Rating, fifa_player_data."Player_Value_(M)", fifa_player_data."Player_Salary_(K)", fifa_player_data.Speed_Rating, fifa_player_data.Endurance_Rating, fifa_player_data.Offensive_Positioning, fifa_player_data.Defensive_Consciousness, fifa_player_data.Effectiveness_Rating, fifa_player_data.GK_Diving, fifa_player_data.GK_Hand_Game, fifa_player_data.GK_Foot_Game, fifa_player_data.GK_Positioning, fifa_player_data.GK_Reflexes, fifa_player_data.Finishing_Rating, fifa_player_data.Heading_Rating, fifa_player_data.Voleys_Rating
FROM fifa_player_data
INNER JOIN liverpool_squad
ON fifa_player_data.First_Name_initial = liverpool_squad.First_Name_initial AND fifa_player_data.Last_Name = liverpool_squad.Last_Name AND fifa_player_data.Player_Nationality = liverpool_squad.Player_Nationality AND fifa_player_data.Club_Name = liverpool_squad.Club_Name;"""
)


# Fetch all the results into a list
liverpool_results = liverpool_cursor.fetchall()


# Print the results with padding to align in columns
for row in liverpool_results:
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

if not liverpool_results:
    print("No results found.")


# Create a set of full names and last names for players retrieved in the SQLite query
liverpool_retrieved_players = set((row[1], row[2]) for row in liverpool_results)

# Filter the liverpool_df DataFrame to get rows not retrieved
liverpool_unretrieved_players_df = liverpool_df[
    ~liverpool_df.apply(
        lambda row: (row["First_Name_initial"], row["Last_Name"])
        in liverpool_retrieved_players,
        axis=1,
    )
]

# Print the unretrieved players
if not liverpool_unretrieved_players_df.empty:
    print(
        liverpool_unretrieved_players_df[
            [
                "First_Name",
                "First_Name_initial",
                "Last_Name",
                "Player_Nationality",
            ]
        ]
    )
else:
    print("All team players retrieved")


# Close the cursor and the connection
liverpool_cursor.close()


################################################################################################################################################
######################################################################## MAN UNITED SQUAD 2023/2024########################################
################################################################################################################################################

# Reading man_united_ CSV file into a pandas DataFrame
man_united_df = pd.read_csv(
    "/Users/moheeb/Documents/Personal_Project_ideas/Premier_league_squads/man_united_squad.csv",
    encoding="utf-8",
)

############--------------------Cleaning man_united_ Data ----------------------


def clean_name(name):
    return unidecode(name)


man_united_df["Last_Name"] = man_united_df["Last_Name"].apply(clean_name)


# Define a custom function to create the "First_Name_initial" column
def create_first_name_initial(man_united_row):
    if pd.notna(man_united_row["First_Name"]):
        return man_united_row["First_Name"][0] + ". "
    else:
        return ""


# Apply the custom function to create the "First_Name_initial" column
man_united_df["First_Name_initial"] = man_united_df.apply(
    create_first_name_initial, axis=1
)

man_united_df["First_Name_initial"] = man_united_df["First_Name_initial"].str.strip()

# Adding a column with the column name

man_united_df["Club_Name"] = "Manchester United"


# print(man_united_df)


# ------------------------------------------------------------------------------------------------------------------------------------------

# Use the 'to_sql' method to write the DataFrame to an SQLite table
man_united_df.to_sql("man_united_squad", conn, if_exists="replace", index=False)

# print(man_united_df)

# print(man_united_df.columns)
# print(man_united_df[["First_Name_initial", "Last_Name", "player_nationality"]])


# Create a cursor
man_united_cursor = conn.cursor()

# Execute SQL queries
man_united_cursor.execute(
    """SELECT DISTINCT man_united_squad.First_Name, man_united_squad.First_Name_initial, man_united_squad.Last_Name, man_united_squad.Club_Name, fifa_player_data.Player_Nationality, man_united_squad.Player_Position, fifa_player_data.Overall_Rating, fifa_player_data.Potential_Rating, fifa_player_data.Average_Performance_Rating, fifa_player_data."Player_Value_(M)", fifa_player_data."Player_Salary_(K)", fifa_player_data.Speed_Rating, fifa_player_data.Endurance_Rating, fifa_player_data.Offensive_Positioning, fifa_player_data.Defensive_Consciousness, fifa_player_data.Effectiveness_Rating, fifa_player_data.GK_Diving, fifa_player_data.GK_Hand_Game, fifa_player_data.GK_Foot_Game, fifa_player_data.GK_Positioning, fifa_player_data.GK_Reflexes, fifa_player_data.Finishing_Rating, fifa_player_data.Heading_Rating, fifa_player_data.Voleys_Rating
FROM fifa_player_data
INNER JOIN man_united_squad
ON fifa_player_data.First_Name_initial = man_united_squad.First_Name_initial AND fifa_player_data.Last_Name = man_united_squad.Last_Name AND fifa_player_data.Player_Nationality = man_united_squad.Player_Nationality AND fifa_player_data.Club_Name = man_united_squad.Club_Name;"""
)


# Fetch all the results into a list
man_united_results = man_united_cursor.fetchall()


# Print the results with padding to align in columns
for row in man_united_results:
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

if not man_united_results:
    print("No results found.")


# Create a set of full names and last names for players retrieved in the SQLite query
man_united_retrieved_players = set((row[1], row[2]) for row in man_united_results)

# Filter the man_united_df DataFrame to get rows not retrieved
man_united_unretrieved_players_df = man_united_df[
    ~man_united_df.apply(
        lambda row: (row["First_Name_initial"], row["Last_Name"])
        in man_united_retrieved_players,
        axis=1,
    )
]

# Print the unretrieved players
if not man_united_unretrieved_players_df.empty:
    print(
        man_united_unretrieved_players_df[
            [
                "First_Name",
                "First_Name_initial",
                "Last_Name",
                "Player_Nationality",
            ]
        ]
    )
else:
    print("All team players retrieved")


# Close the cursor and the connection
man_united_cursor.close()


################################################################################################################################################
######################################################################## CHELSEA SQUAD 2023/2024########################################
################################################################################################################################################

# Reading chelsea_ CSV file into a pandas DataFrame
chelsea_df = pd.read_csv(
    "/Users/moheeb/Documents/Personal_Project_ideas/Premier_league_squads/chelsea_squad.csv",
    encoding="utf-8",
)

############--------------------Cleaning chelsea_ Data ----------------------


def clean_name(name):
    return unidecode(name)


chelsea_df["Last_Name"] = chelsea_df["Last_Name"].apply(clean_name)


# Define a custom function to create the "First_Name_initial" column
def create_first_name_initial(chelsea_row):
    if pd.notna(chelsea_row["First_Name"]):
        return chelsea_row["First_Name"][0] + ". "
    else:
        return ""


# Apply the custom function to create the "First_Name_initial" column
chelsea_df["First_Name_initial"] = chelsea_df.apply(create_first_name_initial, axis=1)

chelsea_df["First_Name_initial"] = chelsea_df["First_Name_initial"].str.strip()

# Adding a column with the column name

chelsea_df["Club_Name"] = "Chelsea"


# print(chelsea_df)


# ------------------------------------------------------------------------------------------------------------------------------------------

# Use the 'to_sql' method to write the DataFrame to an SQLite table
chelsea_df.to_sql("chelsea_squad", conn, if_exists="replace", index=False)

# print(chelsea_df)

# print(chelsea_df.columns)
# print(chelsea_df[["First_Name_initial", "Last_Name", "player_nationality"]])


# Create a cursor
chelsea_cursor = conn.cursor()

# Execute SQL queries
chelsea_cursor.execute(
    """SELECT DISTINCT chelsea_squad.First_Name, chelsea_squad.First_Name_initial, chelsea_squad.Last_Name, chelsea_squad.Club_Name, fifa_player_data.Player_Nationality, chelsea_squad.Player_Position, fifa_player_data.Overall_Rating, fifa_player_data.Potential_Rating, fifa_player_data.Average_Performance_Rating, fifa_player_data."Player_Value_(M)", fifa_player_data."Player_Salary_(K)", fifa_player_data.Speed_Rating, fifa_player_data.Endurance_Rating, fifa_player_data.Offensive_Positioning, fifa_player_data.Defensive_Consciousness, fifa_player_data.Effectiveness_Rating, fifa_player_data.GK_Diving, fifa_player_data.GK_Hand_Game, fifa_player_data.GK_Foot_Game, fifa_player_data.GK_Positioning, fifa_player_data.GK_Reflexes, fifa_player_data.Finishing_Rating, fifa_player_data.Heading_Rating, fifa_player_data.Voleys_Rating
FROM fifa_player_data
INNER JOIN chelsea_squad
ON fifa_player_data.First_Name_initial = chelsea_squad.First_Name_initial AND fifa_player_data.Last_Name = chelsea_squad.Last_Name AND fifa_player_data.Player_Nationality = chelsea_squad.Player_Nationality AND fifa_player_data.Club_Name = chelsea_squad.Club_Name;"""
)


# Fetch all the results into a list
chelsea_results = chelsea_cursor.fetchall()


# Print the results with padding to align in columns
for row in chelsea_results:
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

if not chelsea_results:
    print("No results found.")


# Create a set of full names and last names for players retrieved in the SQLite query
chelsea_retrieved_players = set((row[1], row[2]) for row in chelsea_results)

# Filter the chelsea_df DataFrame to get rows not retrieved
chelsea_unretrieved_players_df = chelsea_df[
    ~chelsea_df.apply(
        lambda row: (row["First_Name_initial"], row["Last_Name"])
        in chelsea_retrieved_players,
        axis=1,
    )
]

# Print the unretrieved players
if not chelsea_unretrieved_players_df.empty:
    print(
        chelsea_unretrieved_players_df[
            [
                "First_Name",
                "First_Name_initial",
                "Last_Name",
                "Player_Nationality",
            ]
        ]
    )
else:
    print("All team players retrieved")


# Close the cursor and the connection
chelsea_cursor.close()


################################################################################################################################################
######################################################################## NEWCASTLE SQUAD 2023/2024########################################
################################################################################################################################################


# Reading newcastle_ CSV file into a pandas DataFrame
newcastle_df = pd.read_csv(
    "/Users/moheeb/Documents/Personal_Project_ideas/Premier_league_squads/newcastle_squad.csv",
    encoding="utf-8",
)

############--------------------Cleaning newcastle_ Data ----------------------


def clean_name(name):
    return unidecode(name)


newcastle_df["Last_Name"] = newcastle_df["Last_Name"].apply(clean_name)


# Define a custom function to create the "First_Name_initial" column
def create_first_name_initial(newcastle_row):
    if pd.notna(newcastle_row["First_Name"]):
        return newcastle_row["First_Name"][0] + ". "
    else:
        return ""


# Apply the custom function to create the "First_Name_initial" column
newcastle_df["First_Name_initial"] = newcastle_df.apply(
    create_first_name_initial, axis=1
)

newcastle_df["First_Name_initial"] = newcastle_df["First_Name_initial"].str.strip()

# Adding a column with the column name

newcastle_df["Club_Name"] = "Newcastle United"


# print(newcastle_df)


# ------------------------------------------------------------------------------------------------------------------------------------------

# Use the 'to_sql' method to write the DataFrame to an SQLite table
newcastle_df.to_sql("newcastle_squad", conn, if_exists="replace", index=False)

# print(newcastle_df)

# print(newcastle_df.columns)
# print(newcastle_df[["First_Name_initial", "Last_Name", "player_nationality"]])


# Create a cursor
newcastle_cursor = conn.cursor()

# Execute SQL queries
newcastle_cursor.execute(
    """SELECT DISTINCT newcastle_squad.First_Name, newcastle_squad.First_Name_initial, newcastle_squad.Last_Name, newcastle_squad.Club_Name, fifa_player_data.Player_Nationality, newcastle_squad.Player_Position, fifa_player_data.Overall_Rating, fifa_player_data.Potential_Rating, fifa_player_data.Average_Performance_Rating, fifa_player_data."Player_Value_(M)", fifa_player_data."Player_Salary_(K)", fifa_player_data.Speed_Rating, fifa_player_data.Endurance_Rating, fifa_player_data.Offensive_Positioning, fifa_player_data.Defensive_Consciousness, fifa_player_data.Effectiveness_Rating, fifa_player_data.GK_Diving, fifa_player_data.GK_Hand_Game, fifa_player_data.GK_Foot_Game, fifa_player_data.GK_Positioning, fifa_player_data.GK_Reflexes, fifa_player_data.Finishing_Rating, fifa_player_data.Heading_Rating, fifa_player_data.Voleys_Rating
FROM fifa_player_data
INNER JOIN newcastle_squad
ON fifa_player_data.First_Name_initial = newcastle_squad.First_Name_initial AND fifa_player_data.Last_Name = newcastle_squad.Last_Name AND fifa_player_data.Player_Nationality = newcastle_squad.Player_Nationality AND fifa_player_data.Club_Name = newcastle_squad.Club_Name;"""
)


# Fetch all the results into a list
newcastle_results = newcastle_cursor.fetchall()


# Print the results with padding to align in columns
for row in newcastle_results:
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

if not newcastle_results:
    print("No results found.")


# Create a set of full names and last names for players retrieved in the SQLite query
newcastle_retrieved_players = set((row[1], row[2]) for row in newcastle_results)

# Filter the newcastle_df DataFrame to get rows not retrieved
newcastle_unretrieved_players_df = newcastle_df[
    ~newcastle_df.apply(
        lambda row: (row["First_Name_initial"], row["Last_Name"])
        in newcastle_retrieved_players,
        axis=1,
    )
]

# Print the unretrieved players
if not newcastle_unretrieved_players_df.empty:
    print(
        newcastle_unretrieved_players_df[
            [
                "First_Name",
                "First_Name_initial",
                "Last_Name",
                "Player_Nationality",
            ]
        ]
    )
else:
    print("All team players retrieved")


# Close the cursor and the connection
newcastle_cursor.close()


################################################################################################################################################
######################################################################## TOTTENHAM SQUAD 2023/2024########################################
################################################################################################################################################

# Reading tottenham_ CSV file into a pandas DataFrame
tottenham_df = pd.read_csv(
    "/Users/moheeb/Documents/Personal_Project_ideas/Premier_league_squads/tottenham_squad.csv",
    encoding="utf-8",
)

############--------------------Cleaning tottenham_ Data ----------------------


def clean_name(name):
    return unidecode(name)


tottenham_df["Last_Name"] = tottenham_df["Last_Name"].apply(clean_name)


# Define a custom function to create the "First_Name_initial" column
def create_first_name_initial(tottenham_row):
    if pd.notna(tottenham_row["First_Name"]):
        return tottenham_row["First_Name"][0] + ". "
    else:
        return ""


# Apply the custom function to create the "First_Name_initial" column
tottenham_df["First_Name_initial"] = tottenham_df.apply(
    create_first_name_initial, axis=1
)

tottenham_df["First_Name_initial"] = tottenham_df["First_Name_initial"].str.strip()

# Adding a column with the column name

tottenham_df["Club_Name"] = "Tottenham Hotspur"


# print(tottenham_df)


# ------------------------------------------------------------------------------------------------------------------------------------------

# Use the 'to_sql' method to write the DataFrame to an SQLite table
tottenham_df.to_sql("tottenham_squad", conn, if_exists="replace", index=False)

# print(tottenham_df)

# print(tottenham_df.columns)
# print(tottenham_df[["First_Name_initial", "Last_Name", "player_nationality"]])


# Create a cursor
tottenham_cursor = conn.cursor()

# Execute SQL queries
tottenham_cursor.execute(
    """SELECT DISTINCT tottenham_squad.First_Name, tottenham_squad.First_Name_initial, tottenham_squad.Last_Name, tottenham_squad.Club_Name, fifa_player_data.Player_Nationality, tottenham_squad.Player_Position, fifa_player_data.Overall_Rating, fifa_player_data.Potential_Rating, fifa_player_data.Average_Performance_Rating, fifa_player_data."Player_Value_(M)", fifa_player_data."Player_Salary_(K)", fifa_player_data.Speed_Rating, fifa_player_data.Endurance_Rating, fifa_player_data.Offensive_Positioning, fifa_player_data.Defensive_Consciousness, fifa_player_data.Effectiveness_Rating, fifa_player_data.GK_Diving, fifa_player_data.GK_Hand_Game, fifa_player_data.GK_Foot_Game, fifa_player_data.GK_Positioning, fifa_player_data.GK_Reflexes, fifa_player_data.Finishing_Rating, fifa_player_data.Heading_Rating, fifa_player_data.Voleys_Rating
FROM fifa_player_data
INNER JOIN tottenham_squad
ON fifa_player_data.First_Name_initial = tottenham_squad.First_Name_initial AND fifa_player_data.Last_Name = tottenham_squad.Last_Name AND fifa_player_data.Player_Nationality = tottenham_squad.Player_Nationality AND fifa_player_data.Club_Name = tottenham_squad.Club_Name;"""
)


# Fetch all the results into a list
tottenham_results = tottenham_cursor.fetchall()


# Print the results with padding to align in columns
for row in tottenham_results:
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

if not tottenham_results:
    print("No results found.")


# Create a set of full names and last names for players retrieved in the SQLite query
tottenham_retrieved_players = set((row[1], row[2]) for row in tottenham_results)

# Filter the tottenham_df DataFrame to get rows not retrieved
tottenham_unretrieved_players_df = tottenham_df[
    ~tottenham_df.apply(
        lambda row: (row["First_Name_initial"], row["Last_Name"])
        in tottenham_retrieved_players,
        axis=1,
    )
]

# Print the unretrieved players
if not tottenham_unretrieved_players_df.empty:
    print(
        tottenham_unretrieved_players_df[
            [
                "First_Name",
                "First_Name_initial",
                "Last_Name",
                "Player_Nationality",
            ]
        ]
    )
else:
    print("All team players retrieved")


# Close the cursor and the connection
tottenham_cursor.close()

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################


conn.close()

################################################################################################################################################
################################################################################################################################################
########################################################### Generating Data visualisation #######################################################
################################################################################################################################################
################################################################################################################################################


# Create lists of team names and average overall ratings
team_names = [
    "Arsenal",
    "Manchester City",
    "Liverpool",
    "Manchester United",
    "Chelsea",
    "Newcastle United",
    "Tottenham Hotspur",
]

# ----------------------------------------------------- Comparing The Average Overall Rating ----------------------


average_overall_ratings = [
    np.mean([row[6] for row in arsenal_results]),
    np.mean([row[6] for row in man_city_results]),
    np.mean([row[6] for row in liverpool_results]),
    np.mean([row[6] for row in man_united_results]),
    np.mean([row[6] for row in chelsea_results]),
    np.mean([row[6] for row in newcastle_results]),
    np.mean([row[6] for row in tottenham_results]),
]
average_performance_ratings = [
    np.mean([row[8] for row in arsenal_results]),
    np.mean([row[8] for row in man_city_results]),
    np.mean([row[8] for row in liverpool_results]),
    np.mean([row[8] for row in man_united_results]),
    np.mean([row[8] for row in chelsea_results]),
    np.mean([row[8] for row in newcastle_results]),
    np.mean([row[8] for row in tottenham_results]),
]

potential_average_overall_ratings = [
    np.mean([row[7] for row in arsenal_results]),
    np.mean([row[7] for row in man_city_results]),
    np.mean([row[7] for row in liverpool_results]),
    np.mean([row[7] for row in man_united_results]),
    np.mean([row[7] for row in chelsea_results]),
    np.mean([row[7] for row in newcastle_results]),
    np.mean([row[7] for row in tottenham_results]),
]

team_ratings_data = {
    "Club Names": team_names,
    "Overall Average Team Rating": average_overall_ratings,
    "Potential Average Team Rating": potential_average_overall_ratings,
    "Average Performance Team Rating": average_performance_ratings,
}

# Create a DataFrame from the calculated ratings
team_ratings_df = pd.DataFrame(team_ratings_data)

# Set the "Club Names" column as the index
team_ratings_df.set_index("Club Names", inplace=True)

# Plot the grouped bar chart
ax = team_ratings_df.plot(kind="bar", figsize=(12, 8), width=0.8)

# Set labels and title
ax.set_xlabel("Club Names")
ax.set_ylabel("Average Ratings")
ax.set_title("Average Team Ratings by Club")

# Set x-axis ticks and labels
ax.set_xticklabels(team_names, rotation=45)
plt.legend(title="Rating Category")

# Show the plot
plt.tight_layout()
plt.show()

# ------------------------------------------------------- Overall Goalkeeper Abilities ---------------------------------------------------------------------

# Overall Goalkeeping abilities
overall_goalkeeping_abilities = {
    team: {
        "Diving": [],
        "Hand-Game": [],
        "Foot-Game": [],
        "Positioning": [],
        "Reflexes": [],
    }
    for team in team_names
}

# Collect goalkeeping abilities data for all goalkeepers in each team
for team_results in [
    arsenal_results,
    man_city_results,
    liverpool_results,
    man_united_results,
    chelsea_results,
    newcastle_results,
    tottenham_results,
]:
    for row in team_results:
        if row[5] == "Goalkeeper (GK)":
            team_name = row[3]
            overall_goalkeeping_abilities[team_name]["Diving"].append(row[16])
            overall_goalkeeping_abilities[team_name]["Hand-Game"].append(row[17])
            overall_goalkeeping_abilities[team_name]["Foot-Game"].append(row[18])
            overall_goalkeeping_abilities[team_name]["Positioning"].append(row[19])
            overall_goalkeeping_abilities[team_name]["Reflexes"].append(row[20])

# Calculate the average goalkeeping abilities for each team
average_goalkeeping_abilities = {
    team: {
        "Diving": np.mean(abilities["Diving"]),
        "Hand-Game": np.mean(abilities["Hand-Game"]),
        "Foot-Game": np.mean(abilities["Foot-Game"]),
        "Positioning": np.mean(abilities["Positioning"]),
        "Reflexes": np.mean(abilities["Reflexes"]),
    }
    for team, abilities in overall_goalkeeping_abilities.items()
}

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 8))

# Define the number of teams and bar width
num_teams = len(team_names)
bar_width = 0.15
index = np.arange(num_teams)

# Create bars for each ability
for i, ability in enumerate(
    ["Diving", "Hand-Game", "Foot-Game", "Positioning", "Reflexes"]
):
    ability_values = [
        average_goalkeeping_abilities[team][ability] for team in team_names
    ]
    ax.bar(index + i * bar_width, ability_values, bar_width, label=ability)

# Set labels and title
ax.set_xlabel("Teams")
ax.set_ylabel("Average Goalkeeping Abilities")
ax.set_title("Average Goalkeeping Abilities for Goalkeepers by Team")

# Set x-axis ticks and labels
ax.set_xticks(index + (bar_width * (num_teams - 1)) / 2)
ax.set_xticklabels(team_names, rotation=45)

# Add legend
ax.legend()

# Show the plot
plt.tight_layout()
plt.show()


# ------------------------------------Bar Chart Comparing Average Overall Rating for Goalkeeping, Defensive, Midfielding and Striking Overall Rating ----------------------------------------------------------------


average_goalkeeper_ratings = [
    np.mean([row[6] for row in arsenal_results if row[5] == "Goalkeeper (GK)"]),
    np.mean([row[6] for row in man_city_results if row[5] == "Goalkeeper (GK)"]),
    np.mean([row[6] for row in liverpool_results if row[5] == "Goalkeeper (GK)"]),
    np.mean([row[6] for row in man_united_results if row[5] == "Goalkeeper (GK)"]),
    np.mean([row[6] for row in chelsea_results if row[5] == "Goalkeeper (GK)"]),
    np.mean([row[6] for row in newcastle_results if row[5] == "Goalkeeper (GK)"]),
    np.mean([row[6] for row in tottenham_results if row[5] == "Goalkeeper (GK)"]),
]


average_defender_ratings = [
    np.mean([row[6] for row in arsenal_results if row[5] == "Defender (DF)"]),
    np.mean([row[6] for row in man_city_results if row[5] == "Defender (DF)"]),
    np.mean([row[6] for row in liverpool_results if row[5] == "Defender (DF)"]),
    np.mean([row[6] for row in man_united_results if row[5] == "Defender (DF)"]),
    np.mean([row[6] for row in chelsea_results if row[5] == "Defender (DF)"]),
    np.mean([row[6] for row in newcastle_results if row[5] == "Defender (DF)"]),
    np.mean([row[6] for row in tottenham_results if row[5] == "Defender (DF)"]),
]


average_midfielder_ratings = [
    np.mean([row[6] for row in arsenal_results if row[5] == "Midfielder (MF)"]),
    np.mean([row[6] for row in man_city_results if row[5] == "Midfielder (MF)"]),
    np.mean([row[6] for row in liverpool_results if row[5] == "Midfielder (MF)"]),
    np.mean([row[6] for row in man_united_results if row[5] == "Midfielder (MF)"]),
    np.mean([row[6] for row in chelsea_results if row[5] == "Midfielder (MF)"]),
    np.mean([row[6] for row in newcastle_results if row[5] == "Midfielder (MF)"]),
    np.mean([row[6] for row in tottenham_results if row[5] == "Midfielder (MF)"]),
]

average_forward_ratings = [
    np.mean([row[6] for row in arsenal_results if row[5] == "Forward (ST)"]),
    np.mean([row[6] for row in man_city_results if row[5] == "Forward (ST)"]),
    np.mean([row[6] for row in liverpool_results if row[5] == "Forward (ST)"]),
    np.mean([row[6] for row in man_united_results if row[5] == "Forward (ST)"]),
    np.mean([row[6] for row in chelsea_results if row[5] == "Forward (ST)"]),
    np.mean([row[6] for row in newcastle_results if row[5] == "Forward (ST)"]),
    np.mean([row[6] for row in tottenham_results if row[5] == "Forward (ST)"]),
]

overall_player_rating_multibar_all_results = [
    row
    for overall_player_rating_results in [
        average_goalkeeper_ratings,
        average_defender_ratings,
        average_midfielder_ratings,
        average_forward_ratings,
    ]
    for row in overall_player_rating_results
]

retrieved_defender_rating_data_df = pd.DataFrame(
    overall_player_rating_multibar_all_results,
    columns=["Overall_Rating"],
)


# Create a DataFrame to hold the average ratings for each position
position_ratings_df = pd.DataFrame(
    {
        "Club Names": team_names,
        "Goalkeeper (GK)": average_goalkeeper_ratings,
        "Defender (DF)": average_defender_ratings,
        "Midfielder (MF)": average_midfielder_ratings,
        "Forward (ST)": average_forward_ratings,
    }
)

# Set the positions as the index
position_ratings_df.set_index("Club Names", inplace=True)

# Plot the grouped bar chart
ax = position_ratings_df.plot(kind="bar", figsize=(12, 8), width=0.8)

# Set labels and title
ax.set_xlabel("Club Names")
ax.set_ylabel("Average Overall Player Rating")
ax.set_title("Average Overall Player Rating by Position and Club")

# Set x-axis ticks and labels
ax.set_xticklabels(team_names, rotation=45)
plt.legend(title="Positions")

# Show the plot
plt.tight_layout()
plt.show()


# ----------------------------------------------------- Player Overall Rating Distribution ---------------------------------------------------------------

player_overall_rating_distribution = [
    ((row[3], row[2], row[6]) for row in arsenal_results),
    ((row[3], row[2], row[6]) for row in man_city_results),
    ((row[3], row[2], row[6]) for row in liverpool_results),
    ((row[3], row[2], row[6]) for row in man_united_results),
    ((row[3], row[2], row[6]) for row in chelsea_results),
    ((row[3], row[2], row[6]) for row in newcastle_results),
    ((row[3], row[2], row[6]) for row in tottenham_results),
]

player_rating_distribution_all_results = [
    row
    for player_rating_results in player_overall_rating_distribution
    for row in player_rating_results
]

# Create a DataFrame from the combined results
retrieved_player_rating_data_df = pd.DataFrame(
    player_rating_distribution_all_results,
    columns=["Club_Name", "Last_Name", "Overall_Rating"],
)


# Create a histogram
fig = px.histogram(
    retrieved_player_rating_data_df,
    x="Overall_Rating",
    color="Club_Name",
    nbins=33,
    marginal="box",
)

fig.update_xaxes(title="Overall Rating")

fig.update_yaxes(title="Player Count")
fig.update_layout(title="Distribution of Overall Ratings of Players Grouped by Club")
fig.show()


# ----------------------------------------------------------- Distribution Curve  for defensive Overall Rating -  --------------------------------------------------------

defender_overall_rating_distribution = [
    (
        [
            (row[3], row[2], row[6])
            for row in arsenal_results
            if row[5] == "Defender (DF)"
        ]
    ),
    (
        [
            (row[3], row[2], row[6])
            for row in man_city_results
            if row[5] == "Defender (DF)"
        ]
    ),
    (
        [
            (row[3], row[2], row[6])
            for row in liverpool_results
            if row[5] == "Defender (DF)"
        ]
    ),
    (
        [
            (row[3], row[2], row[6])
            for row in man_united_results
            if row[5] == "Defender (DF)"
        ]
    ),
    (
        [
            (row[3], row[2], row[6])
            for row in chelsea_results
            if row[5] == "Defender (DF)"
        ]
    ),
    (
        [
            (row[3], row[2], row[6])
            for row in newcastle_results
            if row[5] == "Defender (DF)"
        ]
    ),
    (
        [
            (row[3], row[2], row[6])
            for row in tottenham_results
            if row[5] == "Defender (DF)"
        ]
    ),
]


defender_rating_distribtuion_all_results = [
    row
    for defender_rating_results in defender_overall_rating_distribution
    for row in defender_rating_results
]

# Create a DataFrame from the combined results
retrieved_defender_rating_data_df = pd.DataFrame(
    defender_rating_distribtuion_all_results,
    columns=["Club_Name", "Last_Name", "Overall_Rating"],
)


# Create a histogram
fig = px.histogram(
    retrieved_defender_rating_data_df,
    x="Overall_Rating",
    color="Club_Name",
    nbins=20,
    marginal="box",
)

fig.update_xaxes(title="Overall Rating")

fig.update_yaxes(title="Defender Count")
fig.update_layout(title="Distribution of Overall Ratings of Defenders Grouped by Club")
fig.show()


# ----------------------------------------------------------- Distribution Curve  for Midfielders Overall Rating -  --------------------------------------------------------

midfielder_overall_rating_distribution = [
    (
        [
            (row[3], row[2], row[6])
            for row in arsenal_results
            if row[5] == "Midfielder (MF)"
        ]
    ),
    (
        [
            (row[3], row[2], row[6])
            for row in man_city_results
            if row[5] == "Midfielder (MF)"
        ]
    ),
    (
        [
            (row[3], row[2], row[6])
            for row in liverpool_results
            if row[5] == "Midfielder (MF)"
        ]
    ),
    (
        [
            (row[3], row[2], row[6])
            for row in man_united_results
            if row[5] == "Midfielder (MF)"
        ]
    ),
    (
        [
            (row[3], row[2], row[6])
            for row in chelsea_results
            if row[5] == "Midfielder (MF)"
        ]
    ),
    (
        [
            (row[3], row[2], row[6])
            for row in newcastle_results
            if row[5] == "Midfielder (MF)"
        ]
    ),
    (
        [
            (row[3], row[2], row[6])
            for row in tottenham_results
            if row[5] == "Midfielder (MF)"
        ]
    ),
]


midfielder_rating_distribtuion_all_results = [
    row
    for midfielder_rating_results in midfielder_overall_rating_distribution
    for row in midfielder_rating_results
]

# Create a DataFrame from the combined results
retrieved_midfielder_rating_data_df = pd.DataFrame(
    midfielder_rating_distribtuion_all_results,
    columns=["Club_Name", "Last_Name", "Overall_Rating"],
)


# Create a histogram
fig = px.histogram(
    retrieved_midfielder_rating_data_df,
    x="Overall_Rating",
    color="Club_Name",
    nbins=25,
    marginal="box",
)

fig.update_xaxes(title="Overall Rating")

fig.update_yaxes(title="Midfielder Count")
fig.update_layout(
    title="Distribution of Overall Ratings of Midfielders Grouped by Club"
)
fig.show()


# ----------------------------------------------------------- Distribution Curve  for Strikers Overall Rating -  --------------------------------------------------------


striker_overall_rating_distribution = [
    ([(row[3], row[2], row[6]) for row in arsenal_results if row[5] == "Forward (ST)"]),
    (
        [
            (row[3], row[2], row[6])
            for row in man_city_results
            if row[5] == "Forward (ST)"
        ]
    ),
    (
        [
            (row[3], row[2], row[6])
            for row in liverpool_results
            if row[5] == "Forward (ST)"
        ]
    ),
    (
        [
            (row[3], row[2], row[6])
            for row in man_united_results
            if row[5] == "Forward (ST)"
        ]
    ),
    ([(row[3], row[2], row[6]) for row in chelsea_results if row[5] == "Forward (ST)"]),
    (
        [
            (row[3], row[2], row[6])
            for row in newcastle_results
            if row[5] == "Forward (ST)"
        ]
    ),
    (
        [
            (row[3], row[2], row[6])
            for row in tottenham_results
            if row[5] == "Forward (ST)"
        ]
    ),
]


striker_rating_distribtuion_all_results = [
    row
    for striker_rating_results in striker_overall_rating_distribution
    for row in striker_rating_results
]

# Create a DataFrame from the combined results
retrieved_striker_rating_data_df = pd.DataFrame(
    striker_rating_distribtuion_all_results,
    columns=["Club_Name", "Last_Name", "Overall_Rating"],
)


# Create a histogram
fig = px.histogram(
    retrieved_striker_rating_data_df,
    x="Overall_Rating",
    color="Club_Name",
    nbins=26,
    marginal="box",
)

fig.update_xaxes(title="Overall Rating")

fig.update_yaxes(title="Striker Count")
fig.update_layout(title="Distribution of Overall Ratings of Striker Grouped by Club")
fig.show()


# ----------------------------------------------------------- Comparing Striker  Overall Rating -  --------------------------------------------------------


# Overall Forward (ST) scoring abilities
overall_forward_scoring_abilities = {
    team: {
        "Volleying": [],
        "Finishing": [],
        "Heading": [],
    }
    for team in team_names
}

# Collect scoring abilities data for all strikers in each team
for team_results in [
    arsenal_results,
    man_city_results,
    liverpool_results,
    man_united_results,
    chelsea_results,
    newcastle_results,
    tottenham_results,
]:
    for row in team_results:
        if row[5] == "Forward (ST)":
            team_name = row[3]
            overall_forward_scoring_abilities[team_name]["Volleying"].append(row[23])
            overall_forward_scoring_abilities[team_name]["Finishing"].append(row[21])
            overall_forward_scoring_abilities[team_name]["Heading"].append(row[22])

# Calculate the average scoring abilities for each team
average_scoring_abilities = {
    team: {
        "Volleying": np.mean(abilities["Volleying"]),
        "Finishing": np.mean(abilities["Finishing"]),
        "Heading": np.mean(abilities["Heading"]),
    }
    for team, abilities in overall_forward_scoring_abilities.items()
}

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 8))

# Define the number of teams and bar width
num_teams = len(team_names)
bar_width = 0.2
index = np.arange(num_teams)

# Create bars for each scoring ability (Volleying, Finishing, Heading)
for i, ability in enumerate(["Volleying", "Finishing", "Heading"]):
    ability_values = [average_scoring_abilities[team][ability] for team in team_names]
    ax.bar(
        index + i * bar_width,
        ability_values,
        bar_width,
        label=ability,
    )

# Set labels and title
ax.set_xlabel("Teams")
ax.set_ylabel("Average Scoring Abilities")
ax.set_title("Average Scoring Abilities for Forward Players by Team")

# Set x-axis ticks and labels
ax.set_xticks(index + bar_width)
ax.set_xticklabels(team_names, rotation=45)

# Add legend
ax.legend()

# Show the plot
plt.tight_layout()
plt.show()


# -------------------------------------------------- scatter Graph comparing player Effectiveness Rating and Overall Rating---------------------------------------------------------------------


player_effectivenss_rating_results = [
    ((row[3], row[2], row[5], row[6], row[15]) for row in arsenal_results),
    ((row[3], row[2], row[5], row[6], row[15]) for row in man_city_results),
    ((row[3], row[2], row[5], row[6], row[15]) for row in liverpool_results),
    ((row[3], row[2], row[5], row[6], row[15]) for row in man_united_results),
    ((row[3], row[2], row[5], row[6], row[15]) for row in chelsea_results),
    ((row[3], row[2], row[5], row[6], row[15]) for row in newcastle_results),
    ((row[3], row[2], row[5], row[6], row[15]) for row in tottenham_results),
]

effectivenss_rating_results = [
    row
    for effectiveness_results in player_effectivenss_rating_results
    for row in effectiveness_results
]


# Create a DataFrame from the combined results
player_effectiveness_data_df = pd.DataFrame(
    effectivenss_rating_results,
    columns=[
        "Club_Name",
        "Last_Name",
        "Player_Position",
        "Overall_Rating",
        "Effectiveness_Rating",
    ],
)

player_effectiveness_data_df["Hover_Label"] = (
    player_effectiveness_data_df["Last_Name"]
    + " ("
    + player_effectiveness_data_df["Player_Position"]
    + ")"
)


# Create the scatter plot
fig = px.scatter(
    player_effectiveness_data_df,
    x="Overall_Rating",
    y="Effectiveness_Rating",
    color="Club_Name",
    hover_name="Hover_Label",  # Use the new hover label column
    title="Player Effectiveness",
)

# Show the scatter plot
fig.show()


# -------------------------------------------------- scatter Graph comparing team defensive conciousness and offensive position---------------------------------------------------------------------


player_offensive_defensive_consciousness_results = [
    ((row[3], row[2], row[5], row[13], row[14]) for row in arsenal_results),
    ((row[3], row[2], row[5], row[13], row[14]) for row in man_city_results),
    ((row[3], row[2], row[5], row[13], row[14]) for row in liverpool_results),
    ((row[3], row[2], row[5], row[13], row[14]) for row in man_united_results),
    ((row[3], row[2], row[5], row[13], row[14]) for row in chelsea_results),
    ((row[3], row[2], row[5], row[13], row[14]) for row in newcastle_results),
    ((row[3], row[2], row[5], row[13], row[14]) for row in tottenham_results),
]

all_results = [
    row
    for team_results in player_offensive_defensive_consciousness_results
    for row in team_results
]

# Create a DataFrame from the combined results
offensive_defensive_retrieved_data_df = pd.DataFrame(
    all_results,
    columns=[
        "Club_Name",
        "Last_Name",
        "Player_Position",
        "Offensive_Positioning",
        "Defensive_Consciousness",
    ],
)

offensive_defensive_retrieved_data_df["Hover_Label"] = (
    offensive_defensive_retrieved_data_df["Last_Name"]
    + " ("
    + offensive_defensive_retrieved_data_df["Player_Position"]
    + ")"
)

# Create the scatter plot
fig = px.scatter(
    offensive_defensive_retrieved_data_df,
    x="Offensive_Positioning",
    y="Defensive_Consciousness",
    color="Club_Name",
    hover_name="Hover_Label",  # Use the new hover label column
    title="Player Attributes Scatter Plot",
)

# Show the scatter plot
fig.show()


# ------------------------------------------------- correlation Chart comparing player value by player rating for each football club ------------------------------------------------------------------------------


# Define a function to convert player values to numeric
def convert_player_value(value):
    value = value.replace("€", "")  # Remove Euro symbol
    if value.endswith("K"):
        return float(value[:-1]) * 1000  # Convert K to thousands
    elif value.endswith("M"):
        return float(value[:-1]) * 1000000  # Convert M to millions
    else:
        return float(value)


# Player value results
player_value_results = [
    [
        row[3],  # Club Name
        convert_player_value(row[9]),  # Player Value (converted to numeric)
        row[6],  # Overall Rating
        row[2],  # Last Name
    ]
    for team_results in [
        arsenal_results,
        man_city_results,
        liverpool_results,
        man_united_results,
        chelsea_results,
        newcastle_results,
        tottenham_results,
    ]
    for row in team_results
]

# Create a DataFrame from the combined results
retrieved_player_value_data_df = pd.DataFrame(
    player_value_results,
    columns=[
        "Club_Name",
        "Player_Value",
        "Overall_Rating",
        "Last_Name",
    ],
)

# Group by Club_Name, Player_Salary, Overall_Rating, and Last_Name, then count the players in each group
player_value_grouped = (
    retrieved_player_value_data_df.groupby(
        ["Club_Name", "Player_Value", "Overall_Rating", "Last_Name"]
    )
    .size()
    .reset_index(name="Count")
)

# Create the scatter plot
fig = px.scatter(
    player_value_grouped,
    x="Overall_Rating",
    y="Player_Value",
    color="Club_Name",
    hover_name="Last_Name",
    title="Player Value (euro)",
)

# Show the scatter plot
fig.show()


# ------------------------------------------------- correlation chart comparing  player salary to overall rating for each football club ------------------------------------------------------------------------------


# Define a function to convert player salarys to numeric
def convert_player_salary(salary):
    salary = salary.replace("€", "")  # Remove Euro symbol
    if salary.endswith("K"):
        return float(salary[:-1]) * 1000  # Convert K to thousands
    elif salary.endswith("M"):
        return float(salary[:-1]) * 1000000  # Convert M to millions
    else:
        return float(salary)


# Player salary results
player_salary_results = [
    [
        row[3],  # Club Name
        convert_player_salary(row[10]),  # Player salary (converted to numeric)
        row[6],  # Overall Rating
        row[2],  # Last Name
    ]
    for team_results in [
        arsenal_results,
        man_city_results,
        liverpool_results,
        man_united_results,
        chelsea_results,
        newcastle_results,
        tottenham_results,
    ]
    for row in team_results
]

# Create a DataFrame from the combined results
retrieved_player_salary_data_df = pd.DataFrame(
    player_salary_results,
    columns=[
        "Club_Name",
        "Player_salary",
        "Overall_Rating",
        "Last_Name",
    ],
)

# Group by Club_Name, Player_Salary, Overall_Rating, and Last_Name, then count the players in each group
player_salary_grouped = (
    retrieved_player_salary_data_df.groupby(
        ["Club_Name", "Player_salary", "Overall_Rating", "Last_Name"]
    )
    .size()
    .reset_index(name="Count")
)

# Create the scatter plot
fig = px.scatter(
    player_salary_grouped,
    x="Overall_Rating",
    y="Player_salary",
    color="Club_Name",
    hover_name="Last_Name",
    title="Players Weekly Salary (euro)",
)

# Show the scatter plot
fig.show()


# ------------------------------------------------- treemap and histogram for the number of Player from each country in each team for each team -------------------------------------------------------


player_nationality_results = [
    ((row[3], row[4], row[2]) for row in arsenal_results),
    ((row[3], row[4], row[2]) for row in man_city_results),
    ((row[3], row[4], row[2]) for row in liverpool_results),
    ((row[3], row[4], row[2]) for row in man_united_results),
    ((row[3], row[4], row[2]) for row in chelsea_results),
    ((row[3], row[4], row[2]) for row in newcastle_results),
    ((row[3], row[4], row[2]) for row in tottenham_results),
]

all_results = [
    row for team_results in player_nationality_results for row in team_results
]

# Create a DataFrame from the combined results
retrieved_data_df = pd.DataFrame(
    all_results,
    columns=["Club_Name", "Player_Nationality", "Last_Name"],
)

# Group by Club_Name and Player_Nationality, then count the players in each group
player_nationality_grouped = (
    retrieved_data_df.groupby(["Club_Name", "Player_Nationality", "Last_Name"])
    .size()
    .reset_index(name="Count")
)

# Create the treemap
fig = px.treemap(
    player_nationality_grouped,
    path=["Club_Name", "Player_Nationality", "Last_Name"],  # Define the hierarchy
    values="Count",  # Size of rectangles (count of players)
    color="Count",  # Color of rectangles (count of players)
    color_continuous_scale="YlGnBu",  # Choose a different color scale
    title="Player Nationalities by Team",
)

# Show the treemap
fig.show()

# Histogram showing distribution of nationality in each team

fig = px.histogram(
    retrieved_data_df,
    x="Player_Nationality",
    color="Club_Name",
    nbins=50,
    hover_data=["Last_Name", "Club_Name", "Player_Nationality"],
)
fig.update_layout(
    title="Distribution of Nationalities for Each Team", xaxis=dict(tickangle=45)
)
fig.show()

# -------------------------------------------------------------------------------------------------------------------------------------------
