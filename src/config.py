import os
from dotenv import load_dotenv
from typing import List
from src.schemas import AlertSchema

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
    
    # Alerts
    def _parse_alerts(value: str) -> List[AlertSchema]:
        """ 
        Parse 'USD:EUR:0.85:above,USD:GBP:0.75:below'
        Returns list of AlertSchema.
        """

        if not value:
            return []

        alerts = []

        for alert_str in value.split(','):

            parts = alert_str.strip().split(':')
            if len(parts) != 4:
                continue  # Skip malformed alerts
            base, target, threshold, direction = parts
            alerts.append(AlertSchema(
                base_currency=base.upper(),
                target_currency=target.upper(),
                threshold=float(threshold),
                direction=direction.lower()
                ))
            
        return alerts
    CONFIGURED_ALERTS = _parse_alerts(os.getenv('ALERTS', ''))
    
    # Scheduling
    FETCH_INTERVAL_HOURS = int(os.getenv('FETCH_INTERVAL_HOURS', 1))
    
    # Database
    DB_PATH = os.getenv('DB_PATH', 'currency_exhange_rates.db')
    
    # Logging
    LOG_FILE = os.getenv('LOG_FILE', 'logs/currency_monitor.log')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    CONSOLE_LEVEL = os.getenv('CONSOLE_LEVEL', 'INFO')
    

# -- Testing --
if __name__ == "__main__":
    
    print(Config.CONFIGURED_ALERTS)
