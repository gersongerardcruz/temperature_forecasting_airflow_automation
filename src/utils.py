import pandas as pd

def remove_id_column(df):
    """
    Removes the ID column from a pandas dataframe.
    Takes into account different spellings of "ID" and "Unnamed: 0".
    Parameters:
        df (pandas.DataFrame): The input dataframe.
    Returns:
        pandas.DataFrame: The dataframe with the ID column removed.
    """
    id_columns = ['ID', 'Id', 'id', 'Unnamed: 0']
    for col in id_columns:
        if col in df.columns:
            return df.drop(columns=[col])
    return df