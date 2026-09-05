import os
from dotenv import load_dotenv
from typing import List

# Load .env configuration
load_dotenv()

class Config:
    
    # Helper
    def _parse_list(value: str) -> List[str]:
        """Converts a string of comma-separated values into a list"""
        if not value:
            return []
        
        return [item.strip().upper() for item in value.split(',') if item.split()]
    
    # API Configuration
    API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.frankfurter.dev/v2')
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', 10))
    
    # Currencies to track
    PRIMARY_CURRENCIES = _parse_list(os.getenv('PRIMARY_CURRENCIES', 'USD,EUR,GBP'))
    WATCH_CURRENCIES = _parse_list(os.getenv('WATCH_CURRENCIES', 'JPY,CHF,CAD'))
    TRACKED_CURRENCIES = list(set(PRIMARY_CURRENCIES) | set(WATCH_CURRENCIES))
    
    # Scheduling
    FETCH_INTERVAL_HOURS = int(os.getenv('FETCH_INTERVAL_HOURS', 1))
    
    # Database
    DB_PATH = os.getenv('DB_PATH', 'currency_exhange_rates.db')
    
    # Logging
    LOG_FILE = os.getenv('LOG_FILE', 'logs/currency_monitor.log')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    CONSOLE_LEVEL = os.getenv('CONSOLE_LEVEL', 'INFO')
