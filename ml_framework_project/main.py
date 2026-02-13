from ml_framework_project.data_analyzer.data_preprocessing import drop_missing_values, fill_missing_values_with_mean, standardize_data, normalize_data

from ml_framework_project.data_analyzer.data_reader import read_data

def diamonds_regression_pipeline(file_path: str):
    # Step 1: Read the data
    df = read_data(file_path)

    # Step 2: Drop rows with missing values
    df_cleaned = drop_missing_values(df)
    
    # Step 3: Fill missing values (if any) with mean, median, or mode
    df_filled_mean = fill_missing_values_with_mean(df_cleaned, 'price')
    
    # Step 4: Standardize the 'price' column
    df_standardized = standardize_data(df_filled_mean, 'price')

    # Step 5: Normalize the 'price' column
    df_normalized = normalize_data(df_standardized, 'price')

    # Further steps for regression analysis would go here (e.g., feature engineering, model training, etc.)


def diamonds_classification_pipeline(file_path: str):

    # Step 1: Read the data
    df = read_data(file_path)

    # Step 2: Drop rows with missing values
    df_cleaned = drop_missing_values(df)
    
    # Step 3: Fill missing values (if any) with mean, median, or mode
    df_filled_mean = fill_missing_values_with_mean(df_cleaned, 'cut')
    
    # Step 4: Standardize the 'cut' column
    df_standardized = standardize_data(df_filled_mean, 'cut')

    # Step 5: Normalize the 'cut' column
    df_normalized = normalize_data(df_standardized, 'cut')

    # Further steps for classification analysis would go here (e.g., feature engineering, model training, etc.)
def main():
    print("Hello from ml-framework-project!")


if __name__ == "__main__":
    main()
