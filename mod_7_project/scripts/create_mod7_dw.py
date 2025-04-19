"""
Module 4: Data Warehouse Creation Script
File: mod_7_project/scripts/create_mod7_dw.py

This script handles the creation of the SQLite data warehouse. It creates tables
for customer, product, and sale in the 'data/smart_sale.db' database.
Each table creation is handled in a separate function for easier testing and error handling.
"""

import sqlite3
import sys
import pathlib

# For local imports, temporarily add project root to Python sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Now we can import local modules
from utils.logger import logger  # noqa: E402

# Constants
DW_DIR: pathlib.Path = pathlib.Path("mod_7_project", "data").joinpath("dw")
DB_PATH: pathlib.Path = DW_DIR.joinpath("spotify_data.db")

# Ensure the 'data/dw' directory exists
DW_DIR.mkdir(parents=True, exist_ok=True)

# Delete data warehouse file if it exists
if DB_PATH.exists():
    try:
        DB_PATH.unlink()  # Deletes the file
        logger.info(f"Existing database {DB_PATH} deleted.")
    except Exception as e:
        logger.error(f"Error deleting existing database {DB_PATH}: {e}")

def create_users_table(cursor: sqlite3.Cursor) -> None:
    """Create users table in the data warehouse."""
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                age TEXT,
                gender TEXT,
                spotify_usage_period TEXT,
                spotify_subscription_plan TEXT,
                premium_sub_willingness TEXT,
                preferred_premium_plan TEXT,
                FOREIGN KEY (spotify_subscription_plan) REFERENCES prices (spotify_subscription_plan)
            )
        """)
        logger.info("users table created.")
    except sqlite3.Error as e:
        logger.error(f"Error creating users table: {e}")

def create_prices_table(cursor: sqlite3.Cursor) -> None:
    """Create prices table in the data warehouse."""
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prices (
                spotify_subscription_plan TEXT PRIMARY KEY,
                price_per_month TEXT
            )
        """)
        logger.info("prices table created.")
    except sqlite3.Error as e:
        logger.error(f"Error creating prices table: {e}")

def create_dw() -> None:
    """Create the data warehouse by creating users and prices tables."""
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create tables
        create_users_table(cursor)
        create_prices_table(cursor)

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
        logger.info("Data warehouse created successfully.")

    except sqlite3.Error as e:
        logger.error(f"Error connecting to the database: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()

def main() -> None:
    """Main function to create the data warehouse."""
    logger.info("Starting data warehouse creation...")
    create_dw()
    logger.info("Data warehouse creation complete.")

if __name__ == "__main__":
    main()