import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import zip_longest


################################################################################################################################################
######################################################################## ARSENAL SQUAD 2023/2024########################################
################################################################################################################################################

# Define the URL of the Premier League arsenal squad page
arsenal_url = "https://www.premierleague.com/clubs/1/arsenal/squad"

# Send an HTTP GET request to the URL
arsenal_response = requests.get(arsenal_url)

# Check if the request was successful (status code 200)
if arsenal_response.status_code == 200:
    # Parse the HTML content of the page
    arsenal_soup = BeautifulSoup(arsenal_response.text, "html.parser")

    # Find the HTML elements that contain player information (first and last names)
    arsenal_first_name_elements = arsenal_soup.find_all(
        "div", class_="stats-card__player-first"
    )
    arsenal_last_name_elements = arsenal_soup.find_all(
        "div", class_="stats-card__player-last"
    )
    arsenal_player_position_elements = arsenal_soup.find_all(
        "div", class_="stats-card__player-position"
    )
    arsenal_player_squad_number_elements = arsenal_soup.find_all(
        "div", class_="stats-card__squad-number u-hide-mob-l"
    )
    arsenal_Player_Nationality_elements = arsenal_soup.find_all(
        "span", class_="stats-card__player-country"
    )

    # Ensure that both lists have the same length
    arsenal_max_length = max(
        len(arsenal_first_name_elements),
        len(arsenal_last_name_elements),
        len(arsenal_player_position_elements),
        len(arsenal_player_squad_number_elements),
        len(arsenal_Player_Nationality_elements),
    )

    print(arsenal_max_length)

    # Extract first names and last names into separate lists
    arsenal_first_names = [name.text.strip() for name in arsenal_first_name_elements]
    arsenal_last_names = [name.text.strip() for name in arsenal_last_name_elements]
    arsenal_player_position = [
        name.text.strip() for name in arsenal_player_position_elements
    ]
    arsenal_squad_number = [
        name.text.strip() for name in arsenal_player_squad_number_elements
    ]
    arsenal_Player_Nationality = [
        name.text.strip() for name in arsenal_Player_Nationality_elements
    ]

    # Insert an empty string at the 15th position in the first_names list as the player only has a last name on the webpage:
    arsenal_first_names.insert(17, ".")

    # Use zip_longest to ensure both lists have the same length
    # Fill in missing values with None
    merged_names = list(
        zip_longest(
            arsenal_first_names,
            arsenal_last_names,
            arsenal_player_position,
            arsenal_squad_number,
            arsenal_Player_Nationality,
        )
    )

    # Create a DataFrame from the collected data
    arsenal_df = pd.DataFrame(
        merged_names,
        columns=[
            "First_Name",
            "Last_Name",
            "Player_Position",
            "Squad_Number",
            "Player_Nationality",
        ],
    )

    # Add information to the "Player_Position" column based on conditions
    arsenal_df.loc[
        arsenal_df["Player_Position"] == "Goalkeeper", "Player_Position"
    ] = "Goalkeeper (GK)"  # Corrected "goalkeeper" to "(gk)"
    arsenal_df.loc[
        arsenal_df["Player_Position"] == "Forward", "Player_Position"
    ] = "Forward (ST)"
    arsenal_df.loc[
        arsenal_df["Player_Position"] == "Midfielder", "Player_Position"
    ] = "Midfielder (MF)"
    arsenal_df.loc[
        arsenal_df["Player_Position"] == "Defender", "Player_Position"
    ] = "Defender (DF)"

    # Display the DataFrame
    # print(arsenal_df)
else:
    print("Failed to retrieve the web page. Status code:", arsenal_response.status_code)

# Specify the file path where you want to save the CSV file
arsenal_csv_file_path = "/Users/moheeb/Documents/Personal_Project_ideas/Premier_league_squads/arsenal_squad.csv"

# Use the to_csv method to save the DataFrame as a CSV file
arsenal_df.to_csv(arsenal_csv_file_path, index=False)

print(f"CSV file '{arsenal_csv_file_path}' has been created.")


################################################################################################################################################
######################################################################## MANCHESTER CITY SQUAD 2023/2024########################################
################################################################################################################################################

# Define the URL of the Premier League arsenal squad page
man_city_url = "https://www.premierleague.com/clubs/11/Manchester-City/squad"

# Send an HTTP GET request to the URL
man_city_response = requests.get(man_city_url)

# Check if the request was successful (status code 200)
if man_city_response.status_code == 200:
    # Parse the HTML content of the page
    man_city_soup = BeautifulSoup(man_city_response.text, "html.parser")

    # Find the HTML elements that contain player information (first and last names)
    man_city_first_name_elements = man_city_soup.find_all(
        "div", class_="stats-card__player-first"
    )
    man_city_last_name_elements = man_city_soup.find_all(
        "div", class_="stats-card__player-last"
    )
    man_city_player_position_elements = man_city_soup.find_all(
        "div", class_="stats-card__player-position"
    )
    man_city_player_squad_number_elements = man_city_soup.find_all(
        "div", class_="stats-card__squad-number u-hide-mob-l"
    )
    man_city_Player_Nationality_elements = man_city_soup.find_all(
        "span", class_="stats-card__player-country"
    )

    # Ensure that both lists have the same length
    man_city_max_length = max(
        len(man_city_first_name_elements),
        len(man_city_last_name_elements),
        len(man_city_player_position_elements),
        len(man_city_player_squad_number_elements),
        len(man_city_Player_Nationality_elements),
    )

    print(man_city_max_length)

    # Extract first names and last names into separate lists
    man_city_first_names = [name.text.strip() for name in man_city_first_name_elements]
    man_city_last_names = [name.text.strip() for name in man_city_last_name_elements]
    man_city_player_position = [
        name.text.strip() for name in man_city_player_position_elements
    ]
    man_city_squad_number = [
        name.text.strip() for name in man_city_player_squad_number_elements
    ]
    man_city_Player_Nationality = [
        name.text.strip() for name in man_city_Player_Nationality_elements
    ]

    # Insert an empty string at the 1th and 13th position in the first_names list as the player only has a last name on the webpage:

    man_city_first_names.insert(1, ".")
    man_city_first_names.insert(13, ".")

    # Use zip_longest to ensure both lists have the same length
    # Fill in missing values with None
    man_city_merged_names = list(
        zip_longest(
            man_city_first_names,
            man_city_last_names,
            man_city_player_position,
            man_city_squad_number,
            man_city_Player_Nationality,
        )
    )

    # Create a DataFrame from the collected data
    man_city_df = pd.DataFrame(
        man_city_merged_names,
        columns=[
            "First_Name",
            "Last_Name",
            "Player_Position",
            "Squad_Number",
            "Player_Nationality",
        ],
    )

    # Add information to the "Player_Position" column based on conditions
    man_city_df.loc[
        man_city_df["Player_Position"] == "Goalkeeper", "Player_Position"
    ] = "Goalkeeper (GK)"  # Corrected "goalkeeper" to "(gk)"
    man_city_df.loc[
        man_city_df["Player_Position"] == "Forward", "Player_Position"
    ] = "Forward (ST)"
    man_city_df.loc[
        man_city_df["Player_Position"] == "Midfielder", "Player_Position"
    ] = "Midfielder (MF)"
    man_city_df.loc[
        man_city_df["Player_Position"] == "Defender", "Player_Position"
    ] = "Defender (DF)"

    # Display the DataFrame
    # print(man_city_df)
else:
    print(
        "Failed to retrieve the web page. Status code:", man_city_response.status_code
    )

# Specify the file path where you want to save the CSV file
man_city_csv_file_path = "/Users/moheeb/Documents/Personal_Project_ideas/Premier_league_squads/man_city_squad.csv"

# Use the to_csv method to save the DataFrame as a CSV file
man_city_df.to_csv(man_city_csv_file_path, index=False)

print(f"CSV file '{man_city_csv_file_path}' has been created.")

################################################################################################################################################
######################################################################## LIVERPOOL SQUAD 2023/2024########################################
################################################################################################################################################


# Define the URL of the Premier League liverpool squad page
liverpool_url = "https://www.premierleague.com/clubs/10/liverpool/squad"

# Send an HTTP GET request to the URL
liverpool_response = requests.get(liverpool_url)

# Check if the request was successful (status code 200)
if liverpool_response.status_code == 200:
    # Parse the HTML content of the page
    liverpool_soup = BeautifulSoup(liverpool_response.text, "html.parser")

    # Find the HTML elements that contain player information (first and last names)
    liverpool_first_name_elements = liverpool_soup.find_all(
        "div", class_="stats-card__player-first"
    )
    liverpool_last_name_elements = liverpool_soup.find_all(
        "div", class_="stats-card__player-last"
    )
    liverpool_player_position_elements = liverpool_soup.find_all(
        "div", class_="stats-card__player-position"
    )
    liverpool_player_squad_number_elements = liverpool_soup.find_all(
        "div", class_="stats-card__squad-number u-hide-mob-l"
    )
    liverpool_Player_Nationality_elements = liverpool_soup.find_all(
        "span", class_="stats-card__player-country"
    )

    # Ensure that both lists have the same length
    liverpoool_max_length = max(
        len(liverpool_first_name_elements),
        len(liverpool_last_name_elements),
        len(liverpool_player_position_elements),
        len(liverpool_player_squad_number_elements),
        len(liverpool_Player_Nationality_elements),
    )

    print(liverpoool_max_length)

    # Extract first names and last names into separate lists
    liverpool_first_names = [
        name.text.strip() for name in liverpool_first_name_elements
    ]
    liverpool_last_names = [name.text.strip() for name in liverpool_last_name_elements]
    liverpool_player_position = [
        name.text.strip() for name in liverpool_player_position_elements
    ]
    liverpool_squad_number = [
        name.text.strip() for name in liverpool_player_squad_number_elements
    ]
    liverpool_Player_Nationality = [
        name.text.strip() for name in liverpool_Player_Nationality_elements
    ]

    # Insert an empty string at the 15th position in the first_names list as the player only has a last name on the webpage:
    liverpool_first_names.insert(1, ".")

    # Use zip_longest to ensure both lists have the same length
    # Fill in missing values with None
    merged_names = list(
        zip_longest(
            liverpool_first_names,
            liverpool_last_names,
            liverpool_player_position,
            liverpool_squad_number,
            liverpool_Player_Nationality,
        )
    )

    # Create a DataFrame from the collected data
    liverpool_df = pd.DataFrame(
        merged_names,
        columns=[
            "First_Name",
            "Last_Name",
            "Player_Position",
            "Squad_Number",
            "Player_Nationality",
        ],
    )

    # Add information to the "Player_Position" column based on conditions
    liverpool_df.loc[
        liverpool_df["Player_Position"] == "Goalkeeper", "Player_Position"
    ] = "Goalkeeper (GK)"  # Corrected "goalkeeper" to "(gk)"
    liverpool_df.loc[
        liverpool_df["Player_Position"] == "Forward", "Player_Position"
    ] = "Forward (ST)"
    liverpool_df.loc[
        liverpool_df["Player_Position"] == "Midfielder", "Player_Position"
    ] = "Midfielder (MF)"
    liverpool_df.loc[
        liverpool_df["Player_Position"] == "Defender", "Player_Position"
    ] = "Defender (DF)"

    # Display the DataFrame
    # print(liverpool_df)
else:
    print(
        "Failed to retrieve the web page. Status code:", liverpool_response.status_code
    )

# Specify the file path where you want to save the CSV file
liverpool_csv_file_path = "/Users/moheeb/Documents/Personal_Project_ideas/Premier_league_squads/liverpool_squad.csv"

# Use the to_csv method to save the DataFrame as a CSV file
liverpool_df.to_csv(liverpool_csv_file_path, index=False)

print(f"CSV file '{liverpool_csv_file_path}' has been created.")

################################################################################################################################################
######################################################################## MAN UNITED SQUAD 2023/2024########################################
################################################################################################################################################


# Define the URL of the Premier League man_united squad page
man_united_url = "https://www.premierleague.com/clubs/12/Manchester-United/squad"

# Send an HTTP GET request to the URL
man_united_response = requests.get(man_united_url)

# Check if the request was successful (status code 200)
if man_united_response.status_code == 200:
    # Parse the HTML content of the page
    man_united_soup = BeautifulSoup(man_united_response.text, "html.parser")

    # Find the HTML elements that contain player information (first and last names)
    man_united_first_name_elements = man_united_soup.find_all(
        "div", class_="stats-card__player-first"
    )
    man_united_last_name_elements = man_united_soup.find_all(
        "div", class_="stats-card__player-last"
    )
    man_united_player_position_elements = man_united_soup.find_all(
        "div", class_="stats-card__player-position"
    )
    man_united_player_squad_number_elements = man_united_soup.find_all(
        "div", class_="stats-card__squad-number u-hide-mob-l"
    )
    man_united_Player_Nationality_elements = man_united_soup.find_all(
        "span", class_="stats-card__player-country"
    )

    # Ensure that both lists have the same length
    liverpoool_max_length = max(
        len(man_united_first_name_elements),
        len(man_united_last_name_elements),
        len(man_united_player_position_elements),
        len(man_united_player_squad_number_elements),
        len(man_united_Player_Nationality_elements),
    )

    print(liverpoool_max_length)

    # Extract first names and last names into separate lists
    man_united_first_names = [
        name.text.strip() for name in man_united_first_name_elements
    ]
    man_united_last_names = [
        name.text.strip() for name in man_united_last_name_elements
    ]
    man_united_player_position = [
        name.text.strip() for name in man_united_player_position_elements
    ]
    man_united_squad_number = [
        name.text.strip() for name in man_united_player_squad_number_elements
    ]
    man_united_Player_Nationality = [
        name.text.strip() for name in man_united_Player_Nationality_elements
    ]

    # Insert an empty string at the 15th position in the first_names list as the player only has a last name on the webpage:
    man_united_first_names.insert(16, ".")
    man_united_first_names.insert(27, ".")

    # Use zip_longest to ensure both lists have the same length
    # Fill in missing values with None
    merged_names = list(
        zip_longest(
            man_united_first_names,
            man_united_last_names,
            man_united_player_position,
            man_united_squad_number,
            man_united_Player_Nationality,
        )
    )

    # Create a DataFrame from the collected data
    man_united_df = pd.DataFrame(
        merged_names,
        columns=[
            "First_Name",
            "Last_Name",
            "Player_Position",
            "Squad_Number",
            "Player_Nationality",
        ],
    )

    # Add information to the "Player_Position" column based on conditions
    man_united_df.loc[
        man_united_df["Player_Position"] == "Goalkeeper", "Player_Position"
    ] = "Goalkeeper (GK)"  # Corrected "goalkeeper" to "(gk)"
    man_united_df.loc[
        man_united_df["Player_Position"] == "Forward", "Player_Position"
    ] = "Forward (ST)"
    man_united_df.loc[
        man_united_df["Player_Position"] == "Midfielder", "Player_Position"
    ] = "Midfielder (MF)"
    man_united_df.loc[
        man_united_df["Player_Position"] == "Defender", "Player_Position"
    ] = "Defender (DF)"

    # Display the DataFrame
    # print(man_united_df)
else:
    print(
        "Failed to retrieve the web page. Status code:", man_united_response.status_code
    )

# Specify the file path where you want to save the CSV file
man_united_csv_file_path = "/Users/moheeb/Documents/Personal_Project_ideas/Premier_league_squads/man_united_squad.csv"

# Use the to_csv method to save the DataFrame as a CSV file
man_united_df.to_csv(man_united_csv_file_path, index=False)

print(f"CSV file '{man_united_csv_file_path}' has been created.")

################################################################################################################################################
######################################################################## CHELSEA SQUAD 2023/2024########################################
################################################################################################################################################


# Define the URL of the Premier League chelsea squad page
chelsea_url = "https://www.premierleague.com/clubs/4/Chelsea/squad"

# Send an HTTP GET request to the URL
chelsea_response = requests.get(chelsea_url)

# Check if the request was successful (status code 200)
if chelsea_response.status_code == 200:
    # Parse the HTML content of the page
    chelsea_soup = BeautifulSoup(chelsea_response.text, "html.parser")

    # Find the HTML elements that contain player information (first and last names)
    chelsea_first_name_elements = chelsea_soup.find_all(
        "div", class_="stats-card__player-first"
    )
    chelsea_last_name_elements = chelsea_soup.find_all(
        "div", class_="stats-card__player-last"
    )
    chelsea_player_position_elements = chelsea_soup.find_all(
        "div", class_="stats-card__player-position"
    )
    chelsea_player_squad_number_elements = chelsea_soup.find_all(
        "div", class_="stats-card__squad-number u-hide-mob-l"
    )
    chelsea_Player_Nationality_elements = chelsea_soup.find_all(
        "span", class_="stats-card__player-country"
    )

    # Ensure that both lists have the same length
    liverpoool_max_length = max(
        len(chelsea_first_name_elements),
        len(chelsea_last_name_elements),
        len(chelsea_player_position_elements),
        len(chelsea_player_squad_number_elements),
        len(chelsea_Player_Nationality_elements),
    )

    print(liverpoool_max_length)

    # Extract first names and last names into separate lists
    chelsea_first_names = [name.text.strip() for name in chelsea_first_name_elements]
    chelsea_last_names = [name.text.strip() for name in chelsea_last_name_elements]
    chelsea_player_position = [
        name.text.strip() for name in chelsea_player_position_elements
    ]
    chelsea_squad_number = [
        name.text.strip() for name in chelsea_player_squad_number_elements
    ]
    chelsea_Player_Nationality = [
        name.text.strip() for name in chelsea_Player_Nationality_elements
    ]

    # Insert an empty string at the 15th position in the first_names list as the player only has a last name on the webpage:

    # Use zip_longest to ensure both lists have the same length
    # Fill in missing values with None
    merged_names = list(
        zip_longest(
            chelsea_first_names,
            chelsea_last_names,
            chelsea_player_position,
            chelsea_squad_number,
            chelsea_Player_Nationality,
        )
    )

    # Create a DataFrame from the collected data
    chelsea_df = pd.DataFrame(
        merged_names,
        columns=[
            "First_Name",
            "Last_Name",
            "Player_Position",
            "Squad_Number",
            "Player_Nationality",
        ],
    )

    # Add information to the "Player_Position" column based on conditions
    chelsea_df.loc[
        chelsea_df["Player_Position"] == "Goalkeeper", "Player_Position"
    ] = "Goalkeeper (GK)"  # Corrected "goalkeeper" to "(gk)"
    chelsea_df.loc[
        chelsea_df["Player_Position"] == "Forward", "Player_Position"
    ] = "Forward (ST)"
    chelsea_df.loc[
        chelsea_df["Player_Position"] == "Midfielder", "Player_Position"
    ] = "Midfielder (MF)"
    chelsea_df.loc[
        chelsea_df["Player_Position"] == "Defender", "Player_Position"
    ] = "Defender (DF)"

    # Display the DataFrame
    # print(chelsea_df)
else:
    print("Failed to retrieve the web page. Status code:", chelsea_response.status_code)

# Specify the file path where you want to save the CSV file
chelsea_csv_file_path = "/Users/moheeb/Documents/Personal_Project_ideas/Premier_league_squads/chelsea_squad.csv"

# Use the to_csv method to save the DataFrame as a CSV file
chelsea_df.to_csv(chelsea_csv_file_path, index=False)

print(f"CSV file '{chelsea_csv_file_path}' has been created.")

################################################################################################################################################
######################################################################## NEWCASTLE SQUAD 2023/2024########################################
################################################################################################################################################


# Define the URL of the Premier League newcastle squad page
newcastle_url = "https://www.premierleague.com/clubs/23/Newcastle-United/squad"

# Send an HTTP GET request to the URL
newcastle_response = requests.get(newcastle_url)

# Check if the request was successful (status code 200)
if newcastle_response.status_code == 200:
    # Parse the HTML content of the page
    newcastle_soup = BeautifulSoup(newcastle_response.text, "html.parser")

    # Find the HTML elements that contain player information (first and last names)
    newcastle_first_name_elements = newcastle_soup.find_all(
        "div", class_="stats-card__player-first"
    )
    newcastle_last_name_elements = newcastle_soup.find_all(
        "div", class_="stats-card__player-last"
    )
    newcastle_player_position_elements = newcastle_soup.find_all(
        "div", class_="stats-card__player-position"
    )
    newcastle_player_squad_number_elements = newcastle_soup.find_all(
        "div", class_="stats-card__squad-number u-hide-mob-l"
    )
    newcastle_Player_Nationality_elements = newcastle_soup.find_all(
        "span", class_="stats-card__player-country"
    )

    # Ensure that both lists have the same length
    liverpoool_max_length = max(
        len(newcastle_first_name_elements),
        len(newcastle_last_name_elements),
        len(newcastle_player_position_elements),
        len(newcastle_player_squad_number_elements),
        len(newcastle_Player_Nationality_elements),
    )

    print(liverpoool_max_length)

    # Extract first names and last names into separate lists
    newcastle_first_names = [
        name.text.strip() for name in newcastle_first_name_elements
    ]
    newcastle_last_names = [name.text.strip() for name in newcastle_last_name_elements]
    newcastle_player_position = [
        name.text.strip() for name in newcastle_player_position_elements
    ]
    newcastle_squad_number = [
        name.text.strip() for name in newcastle_player_squad_number_elements
    ]
    newcastle_Player_Nationality = [
        name.text.strip() for name in newcastle_Player_Nationality_elements
    ]

    # Insert an empty string at the 15th position in the first_names list as the player only has a last name on the webpage:

    newcastle_first_names.insert(25, ".")

    # Use zip_longest to ensure both lists have the same length
    # Fill in missing values with None
    merged_names = list(
        zip_longest(
            newcastle_first_names,
            newcastle_last_names,
            newcastle_player_position,
            newcastle_squad_number,
            newcastle_Player_Nationality,
        )
    )

    # Create a DataFrame from the collected data
    newcastle_df = pd.DataFrame(
        merged_names,
        columns=[
            "First_Name",
            "Last_Name",
            "Player_Position",
            "Squad_Number",
            "Player_Nationality",
        ],
    )

    # Add information to the "Player_Position" column based on conditions
    newcastle_df.loc[
        newcastle_df["Player_Position"] == "Goalkeeper", "Player_Position"
    ] = "Goalkeeper (GK)"  # Corrected "goalkeeper" to "(gk)"
    newcastle_df.loc[
        newcastle_df["Player_Position"] == "Forward", "Player_Position"
    ] = "Forward (ST)"
    newcastle_df.loc[
        newcastle_df["Player_Position"] == "Midfielder", "Player_Position"
    ] = "Midfielder (MF)"
    newcastle_df.loc[
        newcastle_df["Player_Position"] == "Defender", "Player_Position"
    ] = "Defender (DF)"

    # Display the DataFrame
    # print(newcastle_df)
else:
    print(
        "Failed to retrieve the web page. Status code:", newcastle_response.status_code
    )

# Specify the file path where you want to save the CSV file
newcastle_csv_file_path = "/Users/moheeb/Documents/Personal_Project_ideas/Premier_league_squads/newcastle_squad.csv"

# Use the to_csv method to save the DataFrame as a CSV file
newcastle_df.to_csv(newcastle_csv_file_path, index=False)

print(f"CSV file '{newcastle_csv_file_path}' has been created.")

################################################################################################################################################
######################################################################## TOTTENHAM SQUAD 2023/2024########################################
################################################################################################################################################


# Define the URL of the Premier League tottenham squad page
tottenham_url = "https://www.premierleague.com/clubs/21/Tottenham-Hotspur/squad"

# Send an HTTP GET request to the URL
tottenham_response = requests.get(tottenham_url)

# Check if the request was successful (status code 200)
if tottenham_response.status_code == 200:
    # Parse the HTML content of the page
    tottenham_soup = BeautifulSoup(tottenham_response.text, "html.parser")

    # Find the HTML elements that contain player information (first and last names)
    tottenham_first_name_elements = tottenham_soup.find_all(
        "div", class_="stats-card__player-first"
    )
    tottenham_last_name_elements = tottenham_soup.find_all(
        "div", class_="stats-card__player-last"
    )
    tottenham_player_position_elements = tottenham_soup.find_all(
        "div", class_="stats-card__player-position"
    )
    tottenham_player_squad_number_elements = tottenham_soup.find_all(
        "div", class_="stats-card__squad-number u-hide-mob-l"
    )
    tottenham_Player_Nationality_elements = tottenham_soup.find_all(
        "span", class_="stats-card__player-country"
    )

    # Ensure that both lists have the same length
    liverpoool_max_length = max(
        len(tottenham_first_name_elements),
        len(tottenham_last_name_elements),
        len(tottenham_player_position_elements),
        len(tottenham_player_squad_number_elements),
        len(tottenham_Player_Nationality_elements),
    )

    print(liverpoool_max_length)

    # Extract first names and last names into separate lists
    tottenham_first_names = [
        name.text.strip() for name in tottenham_first_name_elements
    ]
    tottenham_last_names = [name.text.strip() for name in tottenham_last_name_elements]
    tottenham_player_position = [
        name.text.strip() for name in tottenham_player_position_elements
    ]
    tottenham_squad_number = [
        name.text.strip() for name in tottenham_player_squad_number_elements
    ]
    tottenham_Player_Nationality = [
        name.text.strip() for name in tottenham_Player_Nationality_elements
    ]

    # Insert an empty string at the 15th position in the first_names list as the player only has a last name on the webpage:

    tottenham_first_names.insert(24, ".")

    # Use zip_longest to ensure both lists have the same length
    # Fill in missing values with None
    merged_names = list(
        zip_longest(
            tottenham_first_names,
            tottenham_last_names,
            tottenham_player_position,
            tottenham_squad_number,
            tottenham_Player_Nationality,
        )
    )

    # Create a DataFrame from the collected data
    tottenham_df = pd.DataFrame(
        merged_names,
        columns=[
            "First_Name",
            "Last_Name",
            "Player_Position",
            "Squad_Number",
            "Player_Nationality",
        ],
    )

    # Add information to the "Player_Position" column based on conditions
    tottenham_df.loc[
        tottenham_df["Player_Position"] == "Goalkeeper", "Player_Position"
    ] = "Goalkeeper (GK)"  # Corrected "goalkeeper" to "(gk)"
    tottenham_df.loc[
        tottenham_df["Player_Position"] == "Forward", "Player_Position"
    ] = "Forward (ST)"
    tottenham_df.loc[
        tottenham_df["Player_Position"] == "Midfielder", "Player_Position"
    ] = "Midfielder (MF)"
    tottenham_df.loc[
        tottenham_df["Player_Position"] == "Defender", "Player_Position"
    ] = "Defender (DF)"

    # Display the DataFrame
    # print(tottenham_df)
else:
    print(
        "Failed to retrieve the web page. Status code:", tottenham_response.status_code
    )
# Specify the file path where you want to save the CSV file
tottenham_csv_file_path = "/Users/moheeb/Documents/Personal_Project_ideas/Premier_league_squads/tottenham_squad.csv"

# Use the to_csv method to save the DataFrame as a CSV file
tottenham_df.to_csv(tottenham_csv_file_path, index=False)

print(f"CSV file '{tottenham_csv_file_path}' has been created.")
