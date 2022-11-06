import pandas as pd

def plate_appearances(df, min_pas):
    """_summary_

    Args:
        df (_type_): _description_
        min_pas (_type_): _description_
    """
    atbats = df.groupby(['game_date', 'batter', 'at_bat_number']).agg({'batter':'nunique'})
    atbats.columns = ['batter_count']
    atbats = atbats.reset_index()
    atbats = atbats.drop(columns=['at_bat_number'], axis=1).groupby('batter').sum(numeric_only=True).reset_index()
    atbats = atbats.loc[atbats['batter_count'] >= min_pas]
    return atbats
    