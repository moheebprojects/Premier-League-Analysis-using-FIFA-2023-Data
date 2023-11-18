import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import zip_longest


def scrape_team_data(team_url, team_name):
    # Sending an HTTP GET request to the URL
    response = requests.get(team_url)

    # Ensuring the request was successful (status code 200)
    if response.status_code == 200:
        # Parsing through the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Finding the HTML elements that contain player information
        elements = {
            "first_name": soup.find_all("div", class_="stats-card__player-first"),
            "last_name": soup.find_all("div", class_="stats-card__player-last"),
            "player_position": soup.find_all(
                "div", class_="stats-card__player-position"
            ),
            "squad_number": soup.find_all(
                "div", class_="stats-card__squad-number u-hide-mob-l"
            ),
            "player_nationality": soup.find_all(
                "span", class_="stats-card__player-country"
            ),
        }

        # Creating lists for the extracted data
        data = {
            key: [item.text.strip() for item in value]
            for key, value in elements.items()
        }

        def handle_special_cases(team_name, data, special_cases):
            if team_name in special_cases:
                for index in special_cases[team_name]:
                    data["first_name"].insert(index, ".")

        # Define the special cases for each team
        special_cases = {
            "Arsenal": [17],
            "Manchester City": [1, 13],
            "Liverpool": [1, 25],
            "Manchester United": [16, 27],
            "Newcastle United": [25],
            "Tottenham Hotspur": [24],
        }

        # Inside your scraping function, call the above function
        handle_special_cases(team_name, data, special_cases)

        # Zipping data together
        merged_data = list(zip_longest(*data.values()))

        # Creating a DataFrame
        df = pd.DataFrame(
            merged_data,
            columns=[
                "First_Name",
                "Last_Name",
                "Player_Position",
                "Squad_Number",
                "Player_Nationality",
            ],
        )

        # Adding acronyms to positions
        position_acronyms = {
            "Goalkeeper": "Goalkeeper (GK)",
            "Forward": "Forward (ST)",
            "Midfielder": "Midfielder (MF)",
            "Defender": "Defender (DF)",
        }
        df["Player_Position"] = (
            df["Player_Position"].map(position_acronyms).fillna(df["Player_Position"])
        )

        return df
    else:
        print(
            f"Failed to retrieve the web page for {team_name}. Status code:",
            response.status_code,
        )
        return None

    # Team URLs and names


teams = {
    "Arsenal": "https://www.premierleague.com/clubs/1/arsenal/squad",
    "Manchester City": "https://www.premierleague.com/clubs/11/Manchester-City/squad",
    "Liverpool": "https://www.premierleague.com/clubs/10/liverpool/squad",
    "Manchester United": "https://www.premierleague.com/clubs/12/Manchester-United/squad",
    "Chelsea": "https://www.premierleague.com/clubs/4/Chelsea/squad",
    "Newcastle United": "https://www.premierleague.com/clubs/23/Newcastle-United/squad",
    "Tottenham Hotspur": "https://www.premierleague.com/clubs/21/Tottenham-Hotspur/squad",
}


# Process each team
for team_name, url in teams.items():
    team_df = scrape_team_data(url, team_name)
    if team_df is not None:
        csv_file_path = f"/Users/moheeb/Documents/Personal_Project_ideas/{team_name.replace(' ', '_').lower()}_squad.csv"
        team_df.to_csv(csv_file_path, index=False)
        print(f"CSV file '{csv_file_path}' has been created.")
