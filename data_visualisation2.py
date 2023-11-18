import pandas as pd
import numpy as np
import sqlite3
from unidecode import unidecode
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import mplcursors
from data_processing import execute_sql_query, conn  # Importing from data_processing


def create_visualizations(conn):
    # Fetching The Data
    arsenal_results = execute_sql_query(conn, "arsenal_squad")
    man_city_results = execute_sql_query(conn, "manchester_city_squad")
    liverpool_results = execute_sql_query(conn, "liverpool_squad")
    man_united_results = execute_sql_query(conn, "manchester_united_squad")
    chelsea_results = execute_sql_query(conn, "chelsea_squad")
    newcastle_results = execute_sql_query(conn, "newcastle_united_squad")
    tottenham_results = execute_sql_query(conn, "tottenham_hotspur_squad")
    # Create lists of team names
    team_names = [
        "Arsenal",
        "Manchester City",
        "Liverpool",
        "Manchester United",
        "Chelsea",
        "Newcastle United",
        "Tottenham Hotspur",
    ]

    ### Calculate the averages###
    average_overall_ratings = [
        np.mean([row[6] for row in team_results])
        for team_results in [
            arsenal_results,
            man_city_results,
            liverpool_results,
            man_united_results,
            chelsea_results,
            newcastle_results,
            tottenham_results,
        ]
    ]
    average_performance_ratings = [
        np.mean([row[8] for row in team_results])
        for team_results in [
            arsenal_results,
            man_city_results,
            liverpool_results,
            man_united_results,
            chelsea_results,
            newcastle_results,
            tottenham_results,
        ]
    ]

    potential_average_overall_ratings = [
        np.mean([row[7] for row in team_results])
        for team_results in [
            arsenal_results,
            man_city_results,
            liverpool_results,
            man_united_results,
            chelsea_results,
            newcastle_results,
            tottenham_results,
        ]
    ]

    # Create a DataFrame

    team_ratings_data = {
        "Club Names": team_names,
        "Overall Average Team Rating": average_overall_ratings,
        "Potential Average Team Rating": potential_average_overall_ratings,
        "Average Performance Team Rating": average_performance_ratings,
    }

    team_ratings_df = pd.DataFrame(team_ratings_data)
    team_ratings_df.set_index("Club Names", inplace=True)

    # Plotting the multi-bar chart
    ax = team_ratings_df.plot(kind="bar", figsize=(12, 8), width=0.8)
    ax.set_xlabel("Club Names")
    ax.set_ylabel("Average Ratings")
    ax.set_title("Average Team Ratings by Club")
    ax.set_xticklabels(team_names, rotation=45)
    plt.legend(title="Rating Category")
    plt.tight_layout()
    plt.show()

    ### Calculating overall goalkeepers abilities###

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

    # Collecting goalkeeping abilities data for all goalkeepers in each team

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

    # Calculating the average goalkeeping abilities for each team

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

    # Creating a bar chart figure and axis

    fig, ax = plt.subplots(figsize=(12, 8))

    # Defining the number of teams and bar width

    num_teams = len(team_names)
    bar_width = 0.15
    index = np.arange(num_teams)

    # Creating bars for each ability measured
    for i, ability in enumerate(
        ["Diving", "Hand-Game", "Foot-Game", "Positioning", "Reflexes"]
    ):
        ability_values = [
            average_goalkeeping_abilities[team][ability] for team in team_names
        ]
        ax.bar(index + i * bar_width, ability_values, bar_width, label=ability)

    # Seting the labels and title for the bar chart
    ax.set_xlabel("Teams")
    ax.set_ylabel("Average Goalkeeping Abilities")
    ax.set_title("Average Goalkeeping Abilities for Goalkeepers by Team")

    # Seting the x-axis ticks and labels
    ax.set_xticks(index + (bar_width * (num_teams - 1)) / 2)
    ax.set_xticklabels(team_names, rotation=45)

    # Adding in a legend
    ax.legend()

    # Showing the plot
    plt.tight_layout()
    plt.show()

    ### Bar Chart Comparing Average Overall Rating for Goalkeeping, Defensive, Midfielding and Striking Overall Rating ###

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

    # Creating a DataFrame to hold the average ratings for each position
    position_ratings_df = pd.DataFrame(
        {
            "Club Names": team_names,
            "Goalkeeper (GK)": average_goalkeeper_ratings,
            "Defender (DF)": average_defender_ratings,
            "Midfielder (MF)": average_midfielder_ratings,
            "Forward (ST)": average_forward_ratings,
        }
    )

    # Seting the positions as the index
    position_ratings_df.set_index("Club Names", inplace=True)

    # Ploting the grouped bar chart
    ax = position_ratings_df.plot(kind="bar", figsize=(12, 8), width=0.8)

    # Seing labels and title
    ax.set_xlabel("Club Names")
    ax.set_ylabel("Average Overall Player Rating")
    ax.set_title("Average Overall Player Rating by Position and Club")

    # Seting the x-axis ticks and labels
    ax.set_xticklabels(team_names, rotation=45)
    plt.legend(title="Positions")

    # Showing the plot
    plt.tight_layout()
    plt.show()

    ### Player Overall Rating Distribution ###

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

    # Creating a DataFrame from the combined results
    retrieved_player_rating_data_df = pd.DataFrame(
        player_rating_distribution_all_results,
        columns=["Club_Name", "Last_Name", "Overall_Rating"],
    )

    # Creating a histogram
    fig = px.histogram(
        retrieved_player_rating_data_df,
        x="Overall_Rating",
        color="Club_Name",
        nbins=33,
        marginal="box",
    )

    fig.update_xaxes(title="Overall Rating")
    fig.update_yaxes(title="Player Count")
    fig.update_layout(
        title="Distribution of Overall Ratings of Players Grouped by Club"
    )
    fig.show()

    # ---------------------------------------------- Distribution Curve  for defensive Overall Rating -------------------------------------------------------

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

    # Creating a DataFrame from the combined results
    retrieved_defender_rating_data_df = pd.DataFrame(
        defender_rating_distribtuion_all_results,
        columns=["Club_Name", "Last_Name", "Overall_Rating"],
    )

    # Creating a histogram
    fig = px.histogram(
        retrieved_defender_rating_data_df,
        x="Overall_Rating",
        color="Club_Name",
        nbins=20,
        marginal="box",
    )

    fig.update_xaxes(title="Overall Rating")

    fig.update_yaxes(title="Defender Count")
    fig.update_layout(
        title="Distribution of Overall Ratings of Defenders Grouped by Club"
    )
    fig.show()

    # --------------------------------------------- Distribution Curve  for Midfielders Overall Rating --------------------------------------------------------

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

    # Creating a DataFrame from the combined results
    retrieved_midfielder_rating_data_df = pd.DataFrame(
        midfielder_rating_distribtuion_all_results,
        columns=["Club_Name", "Last_Name", "Overall_Rating"],
    )

    # Creating a histogram
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

    # ------------------------------------------------- Distribution Curve  for Strikers Overall Rating -  --------------------------------------------------------

    striker_overall_rating_distribution = [
        (
            [
                (row[3], row[2], row[6])
                for row in arsenal_results
                if row[5] == "Forward (ST)"
            ]
        ),
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
        (
            [
                (row[3], row[2], row[6])
                for row in chelsea_results
                if row[5] == "Forward (ST)"
            ]
        ),
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

    # Creating a DataFrame from the combined results
    retrieved_striker_rating_data_df = pd.DataFrame(
        striker_rating_distribtuion_all_results,
        columns=["Club_Name", "Last_Name", "Overall_Rating"],
    )

    # Creating a histogram
    fig = px.histogram(
        retrieved_striker_rating_data_df,
        x="Overall_Rating",
        color="Club_Name",
        nbins=26,
        marginal="box",
    )

    fig.update_xaxes(title="Overall Rating")

    fig.update_yaxes(title="Striker Count")
    fig.update_layout(
        title="Distribution of Overall Ratings of Striker Grouped by Club"
    )
    fig.show()

    # -------------------------------------------------------- Comparing Striker  Overall Rating -  --------------------------------------------------------

    # Overall Forward (ST) scoring abilities
    overall_forward_scoring_abilities = {
        team: {
            "Volleying": [],
            "Finishing": [],
            "Heading": [],
        }
        for team in team_names
    }

    # Collecting scoring abilities data for all strikers in each team
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
                overall_forward_scoring_abilities[team_name]["Volleying"].append(
                    row[23]
                )
                overall_forward_scoring_abilities[team_name]["Finishing"].append(
                    row[21]
                )
                overall_forward_scoring_abilities[team_name]["Heading"].append(row[22])

    # Calculating the average scoring abilities for each team
    average_scoring_abilities = {
        team: {
            "Volleying": np.mean(abilities["Volleying"]),
            "Finishing": np.mean(abilities["Finishing"]),
            "Heading": np.mean(abilities["Heading"]),
        }
        for team, abilities in overall_forward_scoring_abilities.items()
    }

    # Creating figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))

    # Defining the number of teams and bar width
    num_teams = len(team_names)
    bar_width = 0.2
    index = np.arange(num_teams)

    # Creating bars for each scoring ability (Volleying, Finishing, Heading)
    for i, ability in enumerate(["Volleying", "Finishing", "Heading"]):
        ability_values = [
            average_scoring_abilities[team][ability] for team in team_names
        ]
        ax.bar(
            index + i * bar_width,
            ability_values,
            bar_width,
            label=ability,
        )

    # Seting labels and title
    ax.set_xlabel("Teams")
    ax.set_ylabel("Average Scoring Abilities")
    ax.set_title("Average Scoring Abilities for Forward Players by Team")

    # Seting x-axis ticks and labels
    ax.set_xticks(index + bar_width)
    ax.set_xticklabels(team_names, rotation=45)

    # Adding a legend
    ax.legend()

    # Showing the plot
    plt.tight_layout()
    plt.show()

    # ----------------------------------------- scatter Graph comparing player Effectiveness Rating and Overall Rating----------------------------------------------

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

    # Creating a DataFrame from the combined results
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

    # Creating the scatter plot
    fig = px.scatter(
        player_effectiveness_data_df,
        x="Overall_Rating",
        y="Effectiveness_Rating",
        color="Club_Name",
        hover_name="Hover_Label",  # Use the new hover label column
        title="Player Effectiveness",
    )

    # Showing the scatter plot
    fig.show()

    # -------------------------------------------- scatter Graph comparing team defensive conciousness and offensive position----------------------------------------

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

    # Creating a DataFrame from the combined results
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

    # Creating the scatter plot
    fig = px.scatter(
        offensive_defensive_retrieved_data_df,
        x="Offensive_Positioning",
        y="Defensive_Consciousness",
        color="Club_Name",
        hover_name="Hover_Label",  # Use the new hover label column
        title="Player Attributes Scatter Plot",
    )

    # Showing the scatter plot
    fig.show()

    # -------------------------------- correlation Chart comparing player value by player rating for each football club -----------------------------------------

    # Defining a function to convert player values to numeric
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

    # Creating a DataFrame from the combined results
    retrieved_player_value_data_df = pd.DataFrame(
        player_value_results,
        columns=[
            "Club_Name",
            "Player_Value",
            "Overall_Rating",
            "Last_Name",
        ],
    )

    # Grouping the results by Club_Name, Player_Salary, Overall_Rating, and Last_Name, then count the players in each group
    player_value_grouped = (
        retrieved_player_value_data_df.groupby(
            ["Club_Name", "Player_Value", "Overall_Rating", "Last_Name"]
        )
        .size()
        .reset_index(name="Count")
    )

    # Creating the scatter plot
    fig = px.scatter(
        player_value_grouped,
        x="Overall_Rating",
        y="Player_Value",
        color="Club_Name",
        hover_name="Last_Name",
        title="Player Value (euro)",
    )

    # Showing the scatter plot
    fig.show()

    # ----------------------------- correlation chart comparing  player salary to overall rating for each football club --------------------------------------------

    # Defining a function to convert player salarys to numeric
    def convert_player_salary(salary):
        salary = salary.replace("€", "")  # Remove Euro symbol
        if salary.endswith("K"):
            return float(salary[:-1]) * 1000  # Convert K to thousands
        elif salary.endswith("M"):
            return float(salary[:-1]) * 1000000  # Convert M to millions
        else:
            return float(salary)

    # Collecting player salary results
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

    # Creating a DataFrame from the combined results
    retrieved_player_salary_data_df = pd.DataFrame(
        player_salary_results,
        columns=[
            "Club_Name",
            "Player_salary",
            "Overall_Rating",
            "Last_Name",
        ],
    )

    # Grouping the results by Club_Name, Player_Salary, Overall_Rating, and Last_Name, then count the players in each group
    player_salary_grouped = (
        retrieved_player_salary_data_df.groupby(
            ["Club_Name", "Player_salary", "Overall_Rating", "Last_Name"]
        )
        .size()
        .reset_index(name="Count")
    )

    # Creating the scatter plot
    fig = px.scatter(
        player_salary_grouped,
        x="Overall_Rating",
        y="Player_salary",
        color="Club_Name",
        hover_name="Last_Name",
        title="Players Weekly Salary (euro)",
    )

    # Showing the scatter plot
    fig.show()

    # ------------------------------ treemap and histogram for the number of Player from each country in each team for each team ---------------------------------

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

    # Creating a DataFrame from the combined results
    retrieved_data_df = pd.DataFrame(
        all_results,
        columns=["Club_Name", "Player_Nationality", "Last_Name"],
    )

    # Grouping the results by Club_Name and Player_Nationality, then count the players in each group
    player_nationality_grouped = (
        retrieved_data_df.groupby(["Club_Name", "Player_Nationality", "Last_Name"])
        .size()
        .reset_index(name="Count")
    )

    # Creating the treemap
    fig = px.treemap(
        player_nationality_grouped,
        path=["Club_Name", "Player_Nationality", "Last_Name"],  # Define the hierarchy
        values="Count",  # Size of rectangles (count of players)
        color="Count",  # Color of rectangles (count of players)
        color_continuous_scale="YlGnBu",  # Choose a different color scale
        title="Player Nationalities by Team",
    )

    # Showing the treemap
    fig.show()

    # creating and showing a Histogram  distribution of nationality in each team

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


if __name__ == "__main__":
    create_visualizations(conn)
