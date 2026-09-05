import logging
import time
import schedule
from datetime import (datetime, timedelta)

from src.config import Config
from src.logging_setup import setup_logging
from src.database import init_database, insert_record
from src.api_client import get_latest_rates, process_rates


# Configure logging
setup_logging()
logger = logging.getLogger(__name__)



def fecth_and_store():
    """Fecth rates and store in database."""
    
    try:
        # Data retrieval
        logger.info('Fetching rates...')
        raw_responses = get_latest_rates(Config.PRIMARY_CURRENCIES, Config.TRACKED_CURRENCIES)
        # Data validation
        records = process_rates(raw_responses)
        
        # Data storage
        for record in records:
            insert_record(**record.model_dump())
            logger.info(f'Stored: {record.base_currency}->{record.target_currency} = {record.rate}')
        
        logger.info(f'Successfuly stored: {len(records)} rates')
        
        
    except Exception as e:
        logger.error(f'Failed to fecth/store: {e}')

def log_next_update():
    next_time = datetime.now() + timedelta(hours=Config.FETCH_INTERVAL_HOURS)
    logger.info(f'Next update at {next_time.strftime('[%H:%M:%S]')}')

def main():
    """Main entry point"""
    
    init_database()
    logger.info(f'Starting app. Tracking: {Config.TRACKED_CURRENCIES}')
    
    # Immediate execution
    fecth_and_store()
    log_next_update()
    
    
    # Schedule periodic runs
    schedule.every(Config.FETCH_INTERVAL_HOURS).hours.do(fecth_and_store)
    schedule.every(Config.FETCH_INTERVAL_HOURS).hours.do(log_next_update)
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(10)

if __name__ == '__main__':
    main()
