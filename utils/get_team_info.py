'''
Title: Get Game/Team Info

Date: 11/19/2022

Purpose: We grab a single day and a team of interest

'''

import pandas as pd
from datetime import datetime, timedelta
import pybaseball as pb
from pybaseball import statcast



def get_games(game_day, lookback_period, team):
    """_summary_

    Args:
        game_day (_type_): _description_
        team (_type_): _description_
        min_abs_season (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    # Using lookback period to calculate various stats
    first_day_range = (datetime.strptime(game_day, '%Y-%m-%d') - timedelta(days = lookback_period)).strftime('%Y-%m-%d')
    last_day_range = (datetime.strptime(game_day, '%Y-%m-%d') - timedelta(days = 1)).strftime('%Y-%m-%d')
    
    # Return game info
    games = statcast(start_dt=first_day_range, end_dt=last_day_range, team=team)
    
    # Get all games
    return games




# Run function and get games
atl_games = get_games('2018-05-13', 28, 'ATL')
# atl_games[['game_date', 'home_team', 'away_team', 'game_pk']].drop_duplicates().reset_index(drop=True)

#atl_games.batter.unique().tolist()
#atl_games.pitcher.unique().tolist()

# Put game ids into a list
atl_games_to_search = atl_games['game_pk'].tolist()

# Players to find
from pybaseball import playerid_reverse_lookup
atl_batters = playerid_reverse_lookup(atl_games.batter.unique().tolist(), key_type='mlbam')
atl_pitchers = playerid_reverse_lookup(atl_games.pitcher.unique().tolist(), key_type='mlbam')

# Want to know which batters are ATL/MIA
from pybaseball.lahman import *
batting_stats = batting()[['playerID', 'yearID', 'teamID']]
pitching_stats = pitching()[['playerID', 'yearID', 'teamID']]

# Merge
game_day = '2018-05-13'
year = datetime.strptime(game_day, '%Y-%m-%d').year


# Batter Info
# -----------------------------------------------
atl_battersv2 = batting_stats.loc[(batting_stats['yearID'] == year)]
batters_team_id = atl_batters.merge(atl_battersv2, left_on = 'key_bbref', right_on = 'playerID')
batters_team_id.loc[batters_team_id['teamID'] == 'ATL']
# Find out by doing this that statcast() is giving us pitching information for ATL, right?


# Pitcher Info
# -----------------------------------------------
atl_pitchersv2 = pitching_stats.loc[pitching_stats['yearID'] == year]
pitchers_team_id = atl_pitchers.merge(atl_pitchersv2, left_on = 'key_bbref', right_on = 'playerID')
pitchers_team_id
pitchers_team_id.loc[pitchers_team_id['teamID'] == 'ATL']
# Find out by doing this that statcast() is giving us pitching information for ATL.


# Find Out ATL Batters
# -----------------------------------------------