import pandas as pd


def drop_missing_values(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    """
    Drops rows with any missing values from the DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    columns (list, optional): List of columns to check for missing values. 
                              If None, checks all columns. Defaults to None.

    Returns:
    pd.DataFrame: DataFrame with rows containing missing values removed.
    """
    if columns is not None:
        df = df.dropna(subset=columns)
    else:
        df = df.dropna()
    return df