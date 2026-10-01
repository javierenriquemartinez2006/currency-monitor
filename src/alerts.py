# -- alerts.py --

from typing import Optional

from src.schemas import ExchangeRate, AlertSchema
from src.config import Config


def triggers(rate: ExchangeRate, alert: AlertSchema) -> bool:
    """Check if a rate triggers an alert (direct match only).
    
    Return:
        True if the alert's pair matches and threshold is crossed"""
    
    # Discard dismatching pairs
    if rate.base_currency != alert.base_currency:
        return False
    if rate.target_currency != alert.target_currency:
        return False
    
    if alert.direction == 'above':
        return rate.rate > alert.threshold
    return rate.rate < alert.threshold
    
def evaluate_alerts(rate: ExchangeRate) -> Optional[AlertSchema]:
    """Evaluate all configured alerts against a single rate.
    
    Returns:
        The highest-priority triggered alert, or None if none triggered
    """
    
    triggered = []
    
    # Store all triggered alerts
    for alert in Config.CONFIGURED_ALERTS:
        if triggers(rate, alert):
            triggered.append(alert)
            
    # Sort by relative surplus. 
    triggered.sort(key=lambda alert: abs(rate.rate - alert.threshold) / alert.threshold)
    
    highest = triggered[0] if triggered else None
    return highest
