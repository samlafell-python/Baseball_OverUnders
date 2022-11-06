from datetime import timedelta, datetime
import pandas as pd
import pybaseball as pb

def game_performances(game_day, player_id_df, lookback_period):
    first_day_range = (datetime.strptime(game_day, '%Y-%m-%d') - timedelta(days = lookback_period)).strftime('%Y-%m-%d')
    last_day_range = (datetime.strptime(game_day, '%Y-%m-%d') - timedelta(days = 1)).strftime('%Y-%m-%d')

    batting_performances = pd.DataFrame()
    for player in player_id_df['key_mlbam'].values:
        data = pb.statcast_batter(first_day_range, last_day_range, player)
        batting_performances = pd.concat([batting_performances, data])

    # Look at the performance of all Atlanta batters on the day of
    return batting_performances