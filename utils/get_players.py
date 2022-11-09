import pandas as pd
import pybaseball as pb
from datetime import datetime
from pybaseball import batting_stats
from pybaseball.lahman import fielding

def get_players(game_day, team, min_abs_season):
    """_summary_

    Args:
        game_day (_type_): _description_
        team (_type_): _description_
        min_abs_season (_type_): _description_

    Returns:
        _type_: _description_
    """
    
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
        
    players_positions = fielding().drop_duplicates(subset=['playerID'], keep='last')[['playerID', 'POS']]
    player_id_df = player_id_df.merge(players_positions, left_on='key_bbref', right_on = 'playerID')

    return player_id_df