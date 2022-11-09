import pandas as pd

def expected_ba(statcast_df, batter_array):
    """_summary_

    Args:
        statcast_df (_type_): _description_
        batter_array (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    # Use PA to limit the xBA Calc
    sample_df = statcast_df.loc[statcast_df['batter'].isin(batter_array)]
    return sample_df.groupby('batter').agg({'estimated_ba_using_speedangle':'mean'}).reset_index()