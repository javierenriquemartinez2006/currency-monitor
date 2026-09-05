import sqlite3
import logging
from contextlib import contextmanager
from pathlib import Path
from datetime import datetime
from typing import Generator

from src.config import Config

# Database path
DB_PATH = Path(Config.DB_PATH)
# Ensure parent directory exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Logger
logger = logging.getLogger(__name__)



# Connect to Database using context manager
@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    """Context manager for database connections."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        
    except Exception as e:
        conn.rollback()
        logger.error(f'Database error: {e}')
        raise
    finally:
        conn.close()

# Initialize Database
def init_database():
    """Creates the tables if they dont exists."""
    
    with get_connection() as conn:
        
        # Table for tracked currency rates
        conn.execute("""
		CREATE TABLE IF NOT EXISTS exchange_rates (
		"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
  		"base_currency"	TEXT NOT NULL,
		"target_currency"	TEXT NOT NULL,
		"rate"	REAL NOT NULL,
		"timestamp" TEXT NOT NULL,
		UNIQUE(base_currency, target_currency, timestamp)
		);""")
        conn.commit()
        logger.info(f'Database initialized at {DB_PATH}')
        

# Insert rate record operation
def insert_record(base_currency: str, target_currency: str, rate: float, timestamp: datetime):
    """Insert a single rate record"""
    
    # Format timestamp, and add current time (API only provides date information)
    now = datetime.now()
    full_timestamp = timestamp.replace(hour=now.hour, minute=now.minute)
    formatted = full_timestamp.strftime('%Y-%m-%d %H:%M')
    
    with get_connection() as conn:
        conn.execute("""
                     INSERT OR IGNORE INTO exchange_rates
                     (base_currency, target_currency, rate, timestamp)
                     VALUES (?, ?, ?, ?)
                     """, (base_currency, target_currency, rate, formatted))
        conn.commit()
