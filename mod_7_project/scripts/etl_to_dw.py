import pandas as pd
import sqlite3
import pathlib
import sys

# For local imports, temporarily add project root to sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Constants
DW_DIR = pathlib.Path("mod_7_project", "data").joinpath("dw")
DB_PATH = DW_DIR.joinpath("spotify_data.db")
DATA_DIR = pathlib.Path("mod_7_project", "data")

def create_schema(cursor: sqlite3.Cursor) -> None:
    """Create tables in the data warehouse if they don't exist."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            age TEXT,
            gender TEXT,
            spotify_usage_period TEXT,
            spotify_subscription_plan TEXT,
            premium_sub_willingness TEXT,
            preferred_premium_plan TEXT,
            FOREIGN KEY (spotify_subscription_plan) REFERENCES prices (spotify_subscription_plan),
            FOREIGN KEY (preferred_premium_plan) REFERENCES prices(spotify_subscription_plan)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            spotify_subscription_plan TEXT PRIMARY KEY,
            price_per_month INTEGER
        )
    """)

def delete_existing_records(cursor: sqlite3.Cursor) -> None:
    """Delete all existing records from the users and prices tables."""
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM prices")

def insert_users(users_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert users data into the users table."""
    users_df.to_sql("users", cursor.connection, if_exists="append", index=False)

def insert_prices(prices_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert prices data into the prices table."""
    prices_df.to_sql("prices", cursor.connection, if_exists="append", index=False)

def load_data_to_db() -> None:
    try:
        # Connect to SQLite – will create the file if it doesn't exist
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create schema and clear existing records
        create_schema(cursor)
        delete_existing_records(cursor)


        # Load prepared data using pandas
        users_df = pd.read_csv(DATA_DIR.joinpath("users_data_prepared.csv"))
        prices_df = pd.read_csv(DATA_DIR.joinpath("spotify_premium_prices.csv"))

        # Insert data into the database
        insert_users(users_df, cursor)
        insert_prices(prices_df, cursor)

        conn.commit()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    load_data_to_db()