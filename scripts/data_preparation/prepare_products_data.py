"""
scripts/data_preparation/prepare_products_data.py

This script reads product data from the data/raw folder, cleans the data, 
and writes the cleaned version to the data/prepared folder.

Tasks:
- Remove duplicates
- Handle missing values
- Remove outliers
- Ensure consistent formatting

-----------------------------------
How to Run:
1. Open a terminal in the main root project folder.
2. Activate the local project virtual environment.
3. Choose the correct commands for your OS to run this script:

Example (Windows/PowerShell) - do NOT include the > prompt:
> .venv\Scripts\activate
> py scripts\data_preparation\prepare_products_data.py

Example (Mac/Linux) - do NOT include the $ prompt:
$ source .venv/bin/activate
$ python3 scripts/data_preparation/prepare_products_data.py
"""

import pathlib
import sys
import pandas as pd

# For local imports, temporarily add project root to Python sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Now we can import local modules
from utils.logger import logger  # noqa: E402

# Constants
DATA_DIR: pathlib.Path = PROJECT_ROOT.joinpath("data")
RAW_DATA_DIR: pathlib.Path = DATA_DIR.joinpath("raw")
PREPARED_DATA_DIR: pathlib.Path = DATA_DIR.joinpath("prepared")

# -------------------
# Reusable Functions
# -------------------

def read_raw_data(file_name: str) -> pd.DataFrame:
    """
    Read raw data from CSV.

    Args:
        file_name (str): Name of the CSV file to read.
    
    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    logger.info(f"FUNCTION START: read_raw_data with file_name={file_name}")
    file_path = RAW_DATA_DIR.joinpath(file_name)
    logger.info(f"Reading data from {file_path}")
    df = pd.read_csv(file_path)
    logger.info(f"Loaded dataframe with {len(df)} rows and {len(df.columns)} columns")
    
    # TODO: OPTIONAL Add data profiling here to understand the dataset
    # Suggestion: Log the datatypes of each column and the number of unique values
    # Example:
    # logger.info(f"Column datatypes: \n{df.dtypes}")
    # logger.info(f"Number of unique values: \n{df.nunique()}")

    logger.info(f"Column datatypes: \n{df.dtypes}")
    logger.info(f"Number of unique values per column: \n{df.nunique()}")

    return df

def save_prepared_data(df: pd.DataFrame, file_name: str) -> None:
    """
    Save cleaned data to CSV.

    Args:
        df (pd.DataFrame): Cleaned DataFrame.
        file_name (str): Name of the output file.
    """
    logger.info(f"FUNCTION START: save_prepared_data with file_name={file_name}, dataframe shape={df.shape}")
    file_path = PREPARED_DATA_DIR.joinpath(file_name)
    df.to_csv(file_path, index=False)
    logger.info(f"Data saved to {file_path}")

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with duplicates removed.
    """
    logger.info(f"FUNCTION START: remove_duplicates with dataframe shape={df.shape}")
    initial_count = len(df)
    
    # TODO: Consider which columns should be used to identify duplicates
    # Example: For products, SKU or product code is typically unique
    # So we could do something like this:
    # df = df.drop_duplicates(subset=['product_code'])
    if 'ProductID' in df.columns:
        df = df.drop_duplicates(subset=['ProductID'])
    else:
        df = df.drop_duplicates()
    
    removed_count = initial_count - len(df)
    logger.info(f"Removed {removed_count} duplicate rows")
    logger.info(f"{len(df)} records remaining after removing duplicates.")
    return df

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values by filling or dropping.
    This logic is specific to the actual data and business rules.

    Args:
        df (pd.DataFrame): Input DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with missing values handled.
    """
    logger.info(f"FUNCTION START: handle_missing_values with dataframe shape={df.shape}")
    
    # Log missing values by column before handling
    missing_by_col = df.isna().sum()
    logger.info(f"Missing values by column before handling:\n{missing_by_col}")
    
    # Fill missing Supplier based on Category mapping
    df['Supplier'].fillna(df['Category'].map({
        'Clothing': 'BigTimeOutfitters',
        'Sports': 'ScoreMore',
        'Electronics': 'IGS'
    }), inplace=True)

    # Fill remaining missing values with empty strings
    df.fillna('', inplace=True)

    # Log missing values by column after handling
    missing_after = df.isna().sum()
    logger.info(f"Missing values by column after handling:\n{missing_after}")
    logger.info(f"{len(df)} records remaining after handling missing values.")
    
    return df

def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove outliers based on the IQR method for numeric columns.

    Args:
        df (pd.DataFrame): Input DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with outliers removed.
    """
    logger.info(f"FUNCTION START: remove_outliers with dataframe shape={df.shape}")
    initial_count = len(df)

    # TODO: Identify numeric columns that might have outliers.
    # Recommended - just use ranges based on reasonable data
    # People should not be 22 feet tall, etc. 
    # OPTIONAL ADVANCED: Use IQR method to identify outliers in numeric columns
    # Example:
    # for col in ['price', 'weight', 'length', 'width', 'height']:
    #     if col in df.columns and df[col].dtype in ['int64', 'float64']:
    #         Q1 = df[col].quantile(0.25)
    #         Q3 = df[col].quantile(0.75)
    #         IQR = Q3 - Q1
    #         lower_bound = Q1 - 1.5 * IQR
    #         upper_bound = Q3 + 1.5 * IQR
    #         df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    #         logger.info(f"Applied outlier removal to {col}: bounds [{lower_bound}, {upper_bound}]")

    ranges = {
        'UnitPrice': (0, 10_000),     # Prices should be between $0 and $10,000
        'Quantity': (0, 1_000_000)    # Quantity between 0 and 1,000,000
    }

    # Apply the range filters
    for col, (min_val, max_val) in ranges.items():
        if col in df.columns and df[col].dtype in ['int64', 'float64']:
            before_filter = len(df)
            df = df[(df[col] >= min_val) & (df[col] <= max_val)]
            removed = before_filter - len(df)
            logger.info(f"Filtered out {removed} rows from '{col}' outside range [{min_val}, {max_val}]")

    removed_count = initial_count - len(df)
    logger.info(f"Removed {removed_count} outlier rows")
    logger.info(f"{len(df)} records remaining after removing outliers.")
    
    return df

def standardize_formats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize the formatting of various columns.

    Args:
        df (pd.DataFrame): Input DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with standardized formatting.
    """
    logger.info(f"FUNCTION START: standardize_formats with dataframe shape={df.shape}")
    
    # TODO: OPTIONAL ADVANCED Implement standardization for product data
    # Suggestion: Consider standardizing text fields, units, and categorical variables
    # Examples (update based on your column names and types):
    # df['product_name'] = df['product_name'].str.title()  # Title case for product names
    # df['category'] = df['category'].str.lower()  # Lowercase for categories
    # df['price'] = df['price'].round(2)  # Round prices to 2 decimal places
    # df['weight_unit'] = df['weight_unit'].str.upper()  # Uppercase units
    
    # Standardize ProductName (title case) and Category (lowercase)
    df['ProductName'] = df['ProductName'].str.title()
    df['Category'] = df['Category'].str.lower()
    
    # Round UnitPrice to 2 decimal places
    df['UnitPrice'] = df['UnitPrice'].round(2)

    logger.info("Completed standardizing formats")
    return df

def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate data against business rules.

    Args:
        df (pd.DataFrame): Input DataFrame.
    
    Returns:
        pd.DataFrame: Validated DataFrame.
    """
    logger.info(f"FUNCTION START: validate_data with dataframe shape={df.shape}")
    
    # TODO: Implement data validation rules specific to products
    # Suggestion: Check for valid values in critical fields
    # Example:
    # invalid_prices = df[df['price'] < 0].shape[0]
    # logger.info(f"Found {invalid_prices} products with negative prices")
    # df = df[df['price'] >= 0]
    
    # Remove rows with negative prices or quantities
    df = df[(df['UnitPrice'] >= 0) & (df['Quantity'] >= 0)]

    logger.info("Data validation complete")
    return df

def main() -> None:
    """
    Main function for processing product data.
    """
    logger.info("==================================")
    logger.info("STARTING prepare_products_data.py")
    logger.info("==================================")

    logger.info(f"Root project folder: {PROJECT_ROOT}")
    logger.info(f"data / raw folder: {RAW_DATA_DIR}")
    logger.info(f"data / prepared folder: {PREPARED_DATA_DIR}")

    input_file = "products_data.csv"
    output_file = "products_data_prepared.csv"
    
    # Read raw data
    df = read_raw_data(input_file)

    # Log initial dataframe information
    logger.info(f"Initial dataframe columns: {', '.join(df.columns.tolist())}")
    logger.info(f"Initial dataframe shape: {df.shape}")
    
    # Clean column names
    original_columns = df.columns.tolist()
    df.columns = df.columns.str.strip().str.replace(' ', '_')
    
    # Log if any column names changed
    changed_columns = [f"{old} -> {new}" for old, new in zip(original_columns, df.columns) if old != new]
    if changed_columns:
        logger.info(f"Cleaned column names: {', '.join(changed_columns)}")

    # Process data
    df = remove_duplicates(df)
    df = handle_missing_values(df)
    df = standardize_formats(df)
    df = remove_outliers(df)
    df = validate_data(df)

    # Save prepared data
    save_prepared_data(df, output_file)

    logger.info("==================================")
    logger.info("FINISHED prepare_products_data.py")
    logger.info("==================================")

# -------------------
# Conditional Execution Block
# -------------------

if __name__ == "__main__":
    main()