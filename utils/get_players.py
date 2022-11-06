import pandas as pd
import pybaseball as pb
from datetime import datetime
from pybaseball import batting_stats

def get_players(game_day, team, min_abs_season):
    
    game_year = datetime.strptime(game_day, '%Y-%m-%d').year
    # get all of this season's batting data so far
    team_data = batting_stats(game_year, qual=min_abs_season)

    # Filter to Team
    team_data = team_data.loc[team_data['Team'] == team]

    # Names
    team_data['name_first'] = team_data.Name.str.split(" ").str[0].str.lower()
    team_data['name_last'] = team_data.Name.str.split(" ").str[1].str.lower()
    enhanced_player_lookup_pt1 = team_data[['IDfg', 'Season', 'Name', 'Team', 'Age', 'name_first', 'name_last']]

    # Get the player id dataframe
    player_id_df = pd.DataFrame()
    for name in list(zip(enhanced_player_lookup_pt1.name_last.values, enhanced_player_lookup_pt1.name_first.values)):
        players = pb.playerid_lookup(last=name[0])
        batter = players.loc[players['name_first'] == name[1].lower()]
        player_id_df = pd.concat([player_id_df, batter])
        
    return player_id_df