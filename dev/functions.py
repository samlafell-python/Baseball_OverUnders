from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
import numpy as np


class Game_Ids:
    def __init__(self, year):
        self.year = year
        self.file_location = f'/Users/samlafell/Documents/Learning/sports_betting_project/data/interim/games{self.year}.csv'
        self.file_exists = os.path.exists(self.file_location)
    
    def scape_schedules(self):
        schedule_url = f'https://www.baseball-reference.com/leagues/majors/{self.year}-schedule.shtml'
        schedule_request = requests.get(schedule_url)
        self.schedule_html = BeautifulSoup(schedule_request.text, 'html.parser')

    def game_ids_to_scape(self):
        if self.file_exists:
            # Just the games that are left to fill in
            games = pd.read_csv(self.file_location)
            return games[games['Away_Score'].isnull()].index.values
        else:
            ######### Total Games in Season #############
            return np.array([i for i in range(len(self.schedule_html.find_all(class_="game")))])