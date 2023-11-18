# Premier-League-EDA-using-FIFA-2023-Data
I web scraped 7 current Premier league teams and conducted an exploratory data analysis (EDA) of the 7 teams using FIFA 2023 player data. 


# Web Scraping 7 Premier league Squads from the Web 

In the data_scraping file, I web scraped information about all players in the football squad for each of the same 7 premier league squads 2023/24, that were chosen to carry out an Exploratory Data Analysis (EDA) on using FIFA 2023 player data. Information I web scraped for each club from the official Premier League site included players first name, last name, position, squad number and nationality. This was achieved in the following steps:

-	I first imported the necessary python libraries including “request” and “BeautifulSoup” for web scraping, “pandas” and "numpy" for data manipulation. 

-	I then defined the URL of the Premier League squad webpage for each of the 7 clubs in the official Premier League website (Arsenal, Manchester city. Liverpool, Manchester United, Chelsea, Newcastle United and Tottenham Hotspur)


-	I used the “request.get()” function to send a HTTP GET request to the specified URL and checked the request was successful (status code 200). It was successful and I 
received a valid response. 

-	I used “BeautifulSoup” to parse the HTML content of the webpage for each club (e.g. ‘arsenal_soup’ or ‘man_city_soup’) to ensure it is structured and specific elements are extracted from it. The BeautifulSoup’s “find_all()” method was used to extract players first name, last name, position, squad number and nationality.

-	To ensure data consistency I ensured all the lists containing player information have the same length by finding the maximum length amongst them (e.g. “arsenal_max_length” and “man_ city_max_lenght”). 

-	I then extracted and processed data from HTML elements into separate lists (e.g. “arsenal_first_names” and “man_city_last_names”), using list comprehension. These lists contained player information. 

-	The data was then cleaned and manipulated for preparation. This included inserting empty strings in “first_name” where players only went by their last name to align the data and used ‘zip_longest’ function to ensure all lists have the same length, filling in missing values with “None”.

-	The data was then transformed to update player position from “Goalkeeper” to “Goalkeeper (GK)” for consistency. 

-	The file path was specified where the DataFrame will be saved as a CSV file (e.g. ‘arsenal_csv_file_path’ or ‘man_city_csv_file_path’) and the ‘to_csv()’ is used to save the DataFrame to the file. Finally, a print message indicting the CSV file has been created and the steps above where repeated for 7 selected premier league teams. 


  ### Data Processing, Pandas Library Storage and SQLITE Database:

In the data_processing file, i carried out data cleaning and processing tasks to prepare the FIFA 2023 player data for storage in an SQLite database. The data is cleaned, by removing accents, splitting and capitalised names, making the data more suitable for analysis. Once cleaned the data is saved into an SQLite database. 


1)	Importing Libraries:

First the necessary python libraries that will be used are imported, including ‘pandas’ for data manipulation, ‘numpy’ for numerical operation, ‘unidecode’ for removing accents and special characters for text, ‘sqlite3’ for interacting with the SQLite databases, and several data visualisation libraries (‘matplotlib’, ‘plotly’, ‘seaborn’, ‘mplcursors’ for creating plots and graphs. 

2)	Creating and Connecting to SQLite Database:

The ‘sqlite3.connect()’ function was used to create a new SQLite database. The ‘conn’ variable holds the connect to the database. 

3)	Reading the FIFA 2023 Player Data: 

Using the pandas DataFrame using ‘pd.read_csv()’ function, the “fifa_player_data_df” was read from a csv file. The csv file path was specified and the “utf-8” encoding was used for proper character encoding. 

4)	Data Cleaning with Unicode:

A custom function ‘clean_name()’ that used the ‘unidecode’ library was defined to remove accents and convert special characteristics in player names to their closest ASCII represenatation. This was applied to the “Player_Name” column of the DataFrame, cleaning up player names.

Another custom function was defined ‘split_name()’ that splits full name column into first name and last name. it splits the names based on the spaces and returns them separately. The “Full_Name” Column is split into “First_Name_Initial” and “Last_Name” columns to store the results. The first letter of the first and last name was also capitalised. 


5)	Database Table Creation:

The ‘to_sql()’ method of the pandas DataFrame is then used to write the cleaned data to SQLite table named “fifa_player_data” within the SQLite database specified by the ‘conn’ connection. If the table already exists, it replaces it (‘if_exists=” replace”’). The data is stored without an index column (‘index=False’).




### Data Process 7 Selected  PREMIER LEAGUE (PL) CLUBS DATA:

In summary, the 7 Premier league (PL) clubs CSV file produced through web scraping for each team is read, cleaned and pre-processed, it is then stored in an SQLite database table, where SQL queries are executed to retrieve player information from both the 7 PL teams datasets and the FIFA player dataset. And finally display player information for both the retrieved and unretrieved players in each of the 7 PL datasets. 

1)	Reading PL Squad CSV File:

Initially the Premier League (PL) squad CSV file which was created by web scraping (read notes above). The file path is specified in the pandas DataFrame and read using the ‘pd.read_csv()’ function. The data is located into squad-name_df (e.g. “arsenal_df”, “newcastle_df” or “man_united_df”). 

2)	Cleaning PL Squad Data:

The function ‘clean_name()’ that uses ‘unidecode’ library was defined to remove accents and convert special characters in the “Last_Name” column of the DataFrame to ensure consistent and clean data. 

The custom function ‘create_first_name_initial()’ was defined to extract the first letter from the “First_Name” column and adds a period (e.g. “John” becomes “J”).
This function is applied to create the “First_Name_Initial” column. All leading or trailing spaces in the “First_Name_Initial” column were stripped. 

A new column was created called “Club_Name” to the DataFrame and set it as the names of the 7 PL clubs selected for EDA (“Arsenal”, “Manchester City”, “Liverpool”, “Manchester United”, “Chelsea”, “Newcastle United” and “Tottenham Hotspur”) respectively for all rows in each squad dataframe. The purpose behind this was to ensure the right player was retrieved when executing SQLite queries. 

3)	Storing Data in SQLite Databases:

The ‘to_sql()’ method was used for the 7 PL dataframe (e.g. ‘arsenal_df’, ‘man_city_df’, ‘newcastle_df’) to write the DataFrame to an SQLite table named (e.g. ‘arsenal_squad’, ‘man_city_squad’, ‘newcastle_squad’) with the SQLite database specified by the ‘conn’ connection. If the table already exists it replaces (if_exists=” replace”’) to ensure the latest data is stored in the table. The data is stored without an index column (‘index=False’). 

4)	Executing SQL Queries:

A cursor was created using the ‘conn.cursor()’ to interact with the SQLite database. An SQL query was then executed that selects distinct player information from both the “fifa_player_data” and the 7 PL SQLite DataFrames created for each team (e.g. ‘arsenal_squad’, ‘man_city_squad’, ‘newcastle_squad’) using an ‘INNER JOIN’ clause. The query retrieves database on matching conditions like “First_Name_Initial”, Last_Name, Player_Nationality and Club_Name. the retrieved data is stored in a variable as a lists of tuples named (e.g. ‘arsenal_results, ‘tottenham_results’, ‘man_city_results’)


5)	Displaying Retrieved Data

a loop is created through the results of the SQL query e.g. ‘arsenal_results, ‘tottenham_results’, ‘man_city_results’) and the player information is printed in the formatted manner, including details like first name, last name, club name, player nationality, player position, player rating and other attributes. If there are no results (empty), “No results found” is printed. 

6)	Filtering Unretrieved Players:

A set was created for all the 7 PL teams called (e.g. ‘arsenal_retrieved_players’, ‘man_city_retrieved_players’, ‘chelsea_retrieved_players’) to store the tuples of the first name initials, and last names for players retrieved in the SQLite query. 

I filtered through the 7 PL clubs dataframes (e.g. “arsenal_df”, “newcastle_df” or “man_united_df”) to obtain rows where the players first name initial and last name do not match the retrieved players. This results in an unretrieved players data frame for each club (e.g. ‘arsenal_unretrieved_players_df’, ‘man_city_unretrieved_players_df’, ‘chelsea_unretrieved_players_df’). 

The unretrieved players details including first name initials, last name and player nationality are printed so they can be further investigated. If all players from the 7 PL clubs dataframes (e.g. “arsenal_df”, “newcastle_df” or “man_united_df”) are retrieved the message “All team players retrieved” is printed. 

7)	Closing Cursor and Connection:

The cursor for each of the 7 PL clubs is closed (e.g. ‘arsenal_cursor_close’, ‘man_united_cursor_close’, ‘tottenham_cursor_close’) and subsequently, closing the connection to the SQLite database. 

Finally the database connection is closed using the ‘conn.close()’ to protect the SQLite databases after all the necessary SQL queries have been executed. 





# EDA and Data Visualisation of the SQL Query Results: 

In the data_visualisations file, a comprehensive analysis of 7 Premier League teams is carried out against FIFA 2023 player data. This includes player ratings, abilities, positions and other attributes and uses various data visualisation to present findings. 


1)	Team Names and Average Ratings Lists:

 A list of football team names is created.

2)	Calculating Average Ratings:

For each team, the script calculates three types of average ratings: overall average team rating, potential average team rating, and average performance team rating.
These ratings are calculated based on specific data for each team, such as 'arsenal_results,' 'man_city_results,' etc.

3)	Creating a DataFrame:

The calculated ratings are stored in dictionaries.
These dictionaries are then used to create a Pandas DataFrame (team_ratings_df) for better data organization.

4)	Plotting a Grouped Bar Chart:

The Pandas DataFrame is used to plot a grouped bar chart using Matplotlib.
The chart displays the average team ratings for each club.

<img width="1125" alt="average_team_rating" src="https://github.com/moheebprojects/Premier-League-Analysis-using-FIFA-2023-Data/assets/125134551/e329412e-2e5f-4f4c-970e-ce4bf991ff31">


5)	Overall Goalkeeper Abilities:

A dictionary named overall_goalkeeping_abilities is created to store various goalkeeping abilities (Diving, Hand-Game, Foot-Game, Positioning, Reflexes) for each team.
Data for goalkeeping abilities is collected from different sets of team results (e.g., arsenal_results) based on player positions.

<img width="1200" alt="average_goalkeeping_abilities" src="https://github.com/moheebprojects/Premier-League-Analysis-using-FIFA-2023-Data/assets/125134551/b935738f-9d1d-4bc8-92b7-928aa8412a30">

<img width="1200" alt="average_goalkeeping_abilities" src="https://github.com/moheebprojects/Premier-League-Analysis-using-FIFA-2023-Data/assets/125134551/a324d93d-5494-4477-aaf9-6c98237f5ee5">


9)	Creating a Grouped Bar Chart for Average Player Ratings:

A grouped bar chart is created to compare the average overall player ratings for different positions within each team.

<img width="1178" alt="average_overall_player_rating" src="https://github.com/moheebprojects/Premier-League-Analysis-using-FIFA-2023-Data/assets/125134551/95cf135d-3b0b-44ab-bc2b-a93bbbedfef1">


10)	Player Overall Rating Distribution:

The script collects data about player overall ratings from different teams and stores it in a DataFrame. It then creates a histogram to visualize the distribution of player overall ratings across all teams.

<img width="1426" alt="overall_player_rating distribution" src="https://github.com/moheebprojects/Premier-League-Analysis-using-FIFA-2023-Data/assets/125134551/a3335235-faab-41c0-82e8-e25b29c63afa">


11)	Distribution Curve for Defensive Overall Rating:

Similar to the player overall rating distribution, this section focuses on defenders. It collects data on defensive overall ratings and creates a histogram.

<img width="1420" alt="overall_defender_rating_distribution" src="https://github.com/moheebprojects/Premier-League-Analysis-using-FIFA-2023-Data/assets/125134551/efc2708c-22ae-40d2-916f-77e7bf36c1e8">


12)	Distribution Curve for Midfielders Overall Rating:

Similar to the previous section, this part focuses on midfielders' overall ratings and creates a histogram.

<img width="1422" alt="overall_midfielder_rating_distribution" src="https://github.com/moheebprojects/Premier-League-Analysis-using-FIFA-2023-Data/assets/125134551/8bd58911-1984-41c2-8ac1-5299fa1d8fd8">


13)	Distribution Curve for Strikers Overall Rating:

This section, like the previous ones, focuses on strikers' overall ratings and creates a histogram.

<img width="1417" alt="overall_striker_rating_distribution" src="https://github.com/moheebprojects/Premier-League-Analysis-using-FIFA-2023-Data/assets/125134551/8478e93f-03aa-496f-b746-bea365d28cbd">


14)	Comparing Scoring Abilities for Forwards (Strikers):

The script calculates and compares the average scoring abilities (Volleying, Finishing, Heading) of forward players (strikers) for each team.

<img width="1186" alt="average_forward_scoring_ability" src="https://github.com/moheebprojects/Premier-League-Analysis-using-FIFA-2023-Data/assets/125134551/c2076c7d-4487-45f0-baad-e3d7ef690a2f">


15)	Scatter Graph Comparing Player Effectiveness Rating and Overall
Rating:

The script creates a scatter plot to compare player effectiveness ratings and overall ratings for different teams.

<img width="1398" alt="player_effectiveness_overall_rating" src="https://github.com/moheebprojects/Premier-League-Analysis-using-FIFA-2023-Data/assets/125134551/fc5e9c6e-7ddf-45c8-904b-b717a7f05155">


16)	Scatter Graph Comparing Team Defensive Consciousness and Offensive Position:

Another scatter plot is created to compare player attributes related to offensive positioning and defensive consciousness for different teams.

<img width="1414" alt="defensive_conciousness_offensive_positioning" src="https://github.com/moheebprojects/Premier-League-Analysis-using-FIFA-2023-Data/assets/125134551/c8e202b5-7f98-4fa8-b707-6ff57ad4ccb9">


17)	Correlation Chart Comparing Player Value and Overall Rating:

This section collects data on player values and creates a scatter plot to explore the correlation between player values and overall ratings for each club.

<img width="1413" alt="player_value(euro)_player_rating" src="https://github.com/moheebprojects/Premier-League-Analysis-using-FIFA-2023-Data/assets/125134551/e8d801a8-0743-4366-b6b8-58d6d9a0c686">


18)	Correlation Chart Comparing Player Salary and Overall Rating:

Similar to the previous section, this part focuses on player salaries and explores the correlation between salaries and overall ratings for each club.

<img width="1411" alt="player_salary(euro)_player_rating" src="https://github.com/moheebprojects/Premier-League-Analysis-using-FIFA-2023-Data/assets/125134551/0556fb1b-9fb4-4423-894b-c22400abab10">


19)	Treemap and Histogram for Player Nationalities:
http://127.0.0.1:53879/ 
This part creates a treemap visualization to show the distribution of player nationalities within each team.
Additionally, it creates a histogram to visualize the distribution of nationalities within each team.

<img width="1388" alt="player_nationalities_heatmap" src="https://github.com/moheebprojects/Premier-League-Analysis-using-FIFA-2023-Data/assets/125134551/22fc0b48-24f0-4824-83bc-d6ab46fafcce">

<img width="1405" alt="club_players_nationality_distribution" src="https://github.com/moheebprojects/Premier-League-Analysis-using-FIFA-2023-Data/assets/125134551/631263c3-e1e6-4e76-a582-d15abd30ae6d">






