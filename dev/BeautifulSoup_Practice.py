'''
Beautiful Soup Practice
Sam LaFell
08/02/2022

Beautiful Soup is definitely the best way to get game-by-game data for batters, pitchers, teams. This will help us have a more concise model.
'''

from bs4 import BeautifulSoup
import requests
import re
from datetime import date, datetime
from time import strptime
import numpy as np
import os
import pandas as pd
import sys
sys.path.append('dev/')
import functions as f

#tables = my_object.find_all('table', class='teams')
#tables
#finals = my_object.find('table', class_="teams")
#finals.a

# What's happening right now is I need to use the base URL to grab the associated URLs for the games that occurred on this day

################################################################
##################### Grab all the Base URLs ###################
################################################################


x = f.Game_Ids(2022)

x.find_file()
x.schedule_html()
x.game_ids_to_scape()

x.find_file()
x.file_exists()

x.game_ids_to_scape

schedule_html = x.schedule_html()
print(schedule_html)


schedule_url = 'https://www.baseball-reference.com/leagues/majors/2022-schedule.shtml'
schedule_request = requests.get(schedule_url)
schedule_html = BeautifulSoup(schedule_request.text, 'html.parser')
######### Total Games in Season #############
total_games = len(schedule_html.find_all(class_="game"))

######### if before today, grab the score, if not, leave score blank #############
score_pattern = re.compile("(\d)")

######### All Game Days in Season #############
game_days = [day.text for day in schedule_html.find_all('h3')]


######### Total Games in Season #############
game_list = []


indexes_needed = game_ids_to_scape(2022)


for game_num in indexes_needed:
    ############ Day of Game Played ############
    game_day = schedule_html.find_all(class_="game")[game_num].parent.h3.text
    if game_day == "Today's Games":
        game_day = date.today().strftime('%A, %B %d, %Y')
    #game_year, game_month, game_mday = strptime(game_day, '%A, %B %d, %Y')[0], strptime(game_day, '%A, %B %d, %Y')[1], strptime(game_day, '%A, %B %d, %Y')[2]
    gameday_asdate = datetime.strptime(game_day, '%A, %B %d, %Y').date()
    date_string_to_append = gameday_asdate.strftime('%m/%d/%Y')
    
    ######### Score Information #############
    regex_text = schedule_html.find_all(class_="game")[game_num].text
    if gameday_asdate < date.today():
        ######### Away Team Information #############
        away_team_raw = schedule_html.find_all(class_="game")[game_num].contents[1].text.strip()
        away_team = away_team_raw.split('\n', 1)[0]
        away_team_score = int(re.findall(score_pattern, regex_text)[0])
        
        ######### Home Team Information ############# 
        home_team_raw = schedule_html.find_all(class_="game")[game_num].contents[3].text.strip()
        home_team = home_team_raw.split('\n', 1)[0]
        home_team_score = int(re.findall(score_pattern, regex_text)[1])
        
    else:
        ######### Away Team Information #############
        away_team = schedule_html.find_all(class_="game")[game_num].contents[3].text.strip()
        away_team_score = np.NaN
        
        ######### Home Team Information ############# 
        home_team = schedule_html.find_all(class_="game")[game_num].contents[5].text.strip()
        home_team_score = np.NaN
        
    if game_num %% 100 == 0:
        print(f'Game Number: {game_num} of {total_games} games.')
    game_list.append([date_string_to_append, away_team, home_team, away_team_score, home_team_score])
    
    
games2022 = pd.DataFrame(game_list, columns=['Date', 'Away_Team', 'Home_Team', 'Away_Score', 'Home_Score'])
games2022.to_csv('data/interim/games2022.csv')


year = 2022
if games_file_path:
    games = pd.read_csv(games_file_path)
    game_ids_to_scrape = games[games['Away_Score'].isnull()].index
    
    

#################################################################################
##################### Grab all the boxscore URLs for that day ###################
#################################################################################

# Load in CSV with all game days
games2022 = pd.read_csv('/Users/samlafell/Documents/Learning/Sports_Betting_Project/Data/Intermediate/games2022.csv')

# Format URL
game_days = games2022.iloc[:,0]
opening_day = game_days[0]
opening_day.date()
url = 'https://www.baseball-reference.com/boxes/?month=4&day=7&year=2022'



my_result = requests.get(url)
my_object = BeautifulSoup(my_result.text, 'html.parser')
# Search the Webpage for all the box scores available for the day and append them to a list
pattern = re.compile("/boxes/[a-zA-Z]{3}/[a-zA-Z]{3}[0-9]{9}.shtml")
for item in my_object.find_all(href=pattern):
    print('https://www.baseball-reference.com'+ re.findall(pattern, str(item))[0])
    print()


