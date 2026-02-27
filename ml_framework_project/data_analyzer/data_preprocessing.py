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


def fill_missing_values(df: pd.DataFrame, column: str, value) -> pd.DataFrame:
    """
    Fills missing values in a specified column with a given value.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    column (str): The column in which to fill missing values.
    value: The value to use for filling missing values.

    Returns:
    pd.DataFrame: DataFrame with missing values filled.
    """
    df[column] = df[column].fillna(value)
    return df


def fill_missing_values_with_mean(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Fills missing values in a specified column with the mean of that column.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    column (str): The column in which to fill missing values.

    Returns:
    pd.DataFrame: DataFrame with missing values filled with the mean.
    """
    mean_value = df[column].mean()
    df[column] = df[column].fillna(mean_value)
    return df


def fill_missing_values_with_median(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Fills missing values in a specified column with the median of that column.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    column (str): The column in which to fill missing values.

    Returns:
    pd.DataFrame: DataFrame with missing values filled with the median.
    """
    median_value = df[column].median()
    df[column] = df[column].fillna(median_value)
    return df


def fill_missing_values_with_mode(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Fills missing values in a specified column with the mode of that column.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    column (str): The column in which to fill missing values.

    Returns:
    pd.DataFrame: DataFrame with missing values filled with the mode.
    """
    mode_value = df[column].mode()[0]
    df[column] = df[column].fillna(mode_value)
    return df


def standardize_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Standardizes a specified column by subtracting the mean and dividing by the standard deviation.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    column (str): The column to standardize.

    Returns:
    pd.DataFrame: DataFrame with the specified column standardized.
    """
    mean = df[column].mean()
    std = df[column].std()
    df[column] = (df[column] - mean) / std
    return df


def normalize_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Normalizes a specified column by scaling the values to a range of [0, 1].

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    column (str): The column to normalize.

    Returns:
    pd.DataFrame: DataFrame with the specified column normalized.
    """
    min_value = df[column].min()
    max_value = df[column].max()
    df[column] = (df[column] - min_value) / (max_value - min_value)
    return df


def normalize_columns(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    """
    Normalizes multiple specified columns by scaling the values to a range of [0, 1].

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    columns (list): List of columns to normalize.

    Returns:
    pd.DataFrame: DataFrame with the specified columns normalized.
    """
    if columns is None:
        columns = df.columns

    for column in columns:
        df = normalize_column(df, column)
    return df


def shuffle_dataframe(df: pd.DataFrame, random_state: int = None) -> pd.DataFrame:
    """
    Shuffles the rows of the DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    random_state (int, optional): Random seed for reproducibility. Defaults to None.

    Returns:
    pd.DataFrame: Shuffled DataFrame.
    """
    return df.sample(frac=1, random_state=random_state).reset_index(drop=True)


def encode_categorical_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Encodes a categorical column using one-hot encoding.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    column (str): The categorical column to encode.

    Returns:
    pd.DataFrame: DataFrame with the specified column one-hot encoded.
    """
    dummies = pd.get_dummies(df[column], prefix=column)
    df = pd.concat([df.drop(column, axis=1), dummies], axis=1)
    return df


def sample_dataframe(
    df: pd.DataFrame, n: int, random_state: int = None
) -> pd.DataFrame:
    """
    Samples n random rows from the DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    n (int): Number of rows to sample.
    random_state (int, optional): Random seed for reproducibility. Defaults to None.

    Returns:
    pd.DataFrame: Sampled DataFrame.
    """
    return df.sample(n=n, random_state=random_state).reset_index(drop=True)
