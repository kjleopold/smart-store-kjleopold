"""
Module 3: Data Preparation Script
File: mod_7_project\scripts\data_prep.py

This script is just one example of a possible data preparation process.
It loads raw CSV files from the 'data/raw/' directory, cleans and prepares each file, 
and saves the prepared data to 'data/prepared/'.
The data preparation steps include removing duplicates, handling missing values, 
trimming whitespace, and more.

This script uses the general DataScrubber class and its methods to perform common, reusable tasks.

To run it, open a terminal in the root project folder.
Activate the local project virtual environment.
Choose the correct command for your OS to run this script.

py scripts\data_prep.py
python3 scripts\data_prep.py

NOTE: I use the ruff linter. 
It warns if all import statements are not at the top of the file.  
I was having trouble with the relative paths, so I  
temporarily add the project root before I can import. 
By adding this comment at the end of an import line noqa: E402
ruff will ignore the warning on just that line. 
"""

import pathlib
import sys
import pandas as pd

# Set project root (one level up from this script)
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent

# Add project root to system path so local imports work
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Import logger
from utils.logger import logger  # noqa: E402

# Correct folder paths
DATA_DIR: pathlib.Path = PROJECT_ROOT.joinpath("data")

def read_raw_data(file_name: str) -> pd.DataFrame:
    file_path: pathlib.Path = DATA_DIR.joinpath(file_name)
    return pd.read_csv(file_path)

def save_prepared_data(df: pd.DataFrame, file_name: str) -> None:
    """Save cleaned data to CSV."""
    file_path: pathlib.Path = DATA_DIR.joinpath(file_name)
    df.to_csv(file_path, index=False)
    logger.info(f"Data saved to {file_path}")

def main() -> None:
    """Main function for pre-processing user data."""
    logger.info("======================")
    logger.info("STARTING data_prep.py")
    logger.info("======================")

    # Read raw user data
    df_users = read_raw_data("spotify_data.csv")

    columns_to_keep = [
        'age',
        'gender',
        'spotify_usage_period',
        'spotify_subscription_plan',
        'premium_sub_willingness',
        'preferred_premium_plan'
    ]
    
    # Keep only the needed columns
    df_users = df_users[columns_to_keep]

    # Save the cleaned data
    save_prepared_data(df_users, "users_data_prepared.csv")

    logger.info("======================")
    logger.info("FINISHED data_prep.py")
    logger.info("======================")

if __name__ == "__main__":
    main()