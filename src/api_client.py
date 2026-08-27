import requests
import logging
import time
from pydantic import ValidationError
from typing import List

from src.config import Config
from src.schemas import ExchangeRate

# Logger
logger = logging.getLogger(__name__)


def fetch_with_retry(url: str, max_retries: int = 3) -> List[dict]:
    """Fetch url with exponential backoff.
    
    Return:
        List of rates as dict
        """
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.HTTPError) as e:
            if attempt == max_retries - 1:
                logger.error(f'All retries failed: {e}')
                raise
            # Exponential backoff
            wait = 2 ** attempt
            logger.warning(f'Attempt {attempt+1} failed, retrying in {wait}s')
            time.sleep(wait)

def get_latest_rates(bases: List[str], targets: List[str]) -> List[dict]:
    """Fetch all rates for tracked currencies efficiently. Uses retry logic.
    
    Return: List with latest rates as dicts"""
    
    # Rates for tracked currencies
    tracked_rates = []
    
    # URL formation
    url = f'{Config.API_BASE_URL}/rates'
    # Fetch API rates data
    rates = fetch_with_retry(url)
    # Filter rates of tracked currencies:
    for rate in rates:
        if rate['base'] in bases and rate['quote'] in targets:
            # Prevent from autoreferenced rates
            if rate['base'] == rate['quote']:
                continue
            tracked_rates.append(rate)
            
    return tracked_rates

def process_rates(raw_rates: List[dict]) -> List[ExchangeRate]:
    """Validate and convert raw data into internal data schema (ExchangeRate)."""
    
    # List of validated instances of the internal model (ExchangeRate)
    records = []
    
    for raw_rate in raw_rates:
        
        try:
            # Pydantic validation
            valid_rate = ExchangeRate(base_currency=raw_rate['base'],
                                        target_currency=raw_rate['quote'],
                                        rate=raw_rate['rate'],
                                        timestamp=raw_rate['date']
                                        )
            records.append(valid_rate)
            
        except ValidationError as e:
            logger.error(f'Validation failed for {raw_rate}: {e}')
            raise
        except KeyError as e:
            logger.error(f'Missing expected field: {e}')
            raise
        
    return records


    
  
# -- Testing --

if __name__ == '__main__':
    
    # Variables
    URL = Config.API_BASE_URL
    BASES = Config.PRIMARY_CURRENCIES
    TARGETS = Config.WATCH_CURRENCIES
    

    res = get_latest_rates(BASES, TARGETS)
    print(res)
    
    # Uncomment for visualizing raw API response
    # api_data = requests.get(f'{URL}/rates')
    # print(f'\n{api_data.json()}')

