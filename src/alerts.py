# -- alerts.py --

from src.schemas import ExchangeRate, AlertSchema, AlertEventRecord
from src.config import Config
from typing import List


# Alert evaluation
def triggers_alert(rate: ExchangeRate, alert: AlertSchema) -> bool:
    """Evaluate a single alert upon target_rate. 
    Triggers for exact equality (rate == threshold)
    
    Returns:
        Bool based on evaluation result
    """
    
    # Verify currency matching for evaluation
    # Direct matching
    if rate.base_currency == alert.base_currency and rate.target_currency == alert.target_currency:
        if alert.direction == 'above' and rate.rate > alert.threshold:
            return True
        elif alert.direction == 'below' and rate.rate < alert.threshold:
            return True
        else:
            return False
        
    # Inverse match
    if rate.base_currency == alert.target_currency and rate.target_currency == alert.base_currency:
        effective_threshold = 1 / alert.threshold
        effective_direction = 'above' if alert.direction == 'below' else 'below'
        if effective_direction == 'above' and rate.rate > effective_threshold:
            return True
        elif effective_direction == 'below' and rate.rate < effective_threshold:
            return True
        else:
            return False
        
    # No match: discard
    else:
        return False
    


    
    