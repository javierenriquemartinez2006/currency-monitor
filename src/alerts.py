# -- alerts.py --

from enum import Enum
from typing import List, Optional, Tuple

from src.schemas import ExchangeRate, AlertSchema
from src.config import Config


class MatchType(Enum):
    DIRECT = 'direct'
    INVERSE = 'inverse'
    NONE = 'none'

def match_alert(rate: ExchangeRate, alert: AlertSchema):
    """Classify how rate relates to alert's currency pair."""
    
    if rate.base_currency == alert.base_currency and rate.target_currency == alert.target_currency:
        return MatchType.DIRECT
    if rate.base_currency == alert.target_currency and rate.target_currency == alert.base_currency:
        return MatchType.INVERSE
    return MatchType.NONE

def triggers(rate: float, threshold: float, direction: str) -> bool:
    """Check if a value crosses a threshold in a given direction."""
    if direction == 'above':
        return rate > threshold
    return rate < threshold
    
def evaluate_alert(rate: ExchangeRate, alert: AlertSchema) -> Optional[float]:
    """Evaluate a single alert against a rate. 
    
    Returns:
        Effective rate that triggered the alert, or None.
    """
    
    # Verify currency matching for evaluation
    match_type = match_alert(rate, alert)
    
    # Direct match
    if match_type == MatchType.DIRECT:
        if triggers(rate.rate, alert.threshold, alert.direction):
            return rate.rate
        
    # Inverse match
    if match_type == MatchType.INVERSE:
        effective_rate = 1 / rate.rate
        if triggers(effective_rate, alert.threshold, alert.direction):
            return effective_rate
        
    # No match or trigger: discard
    return None

def severity(alert: AlertSchema, effective_rate: float) -> float:
    """Difference of the effective rate against the threshold"""
    if alert.direction == 'above':
        return abs(effective_rate - alert.threshold)
    return abs(alert.threshold - effective_rate)

def evaluate_all_alerts(rate: ExchangeRate) -> List[Tuple[AlertSchema, float]]:
    """Evaluate all configured alerts against rate.
    
    Returns:
        List of (alerts, effective_rate) tuples, sorted by severity (highest first).
    """
    triggered = []
    
    for alert in Config.CONFIGURED_ALERTS:
        effective_rate = evaluate_alert(rate, alert)
        if effective_rate is not None:
            triggered.append((alert, effective_rate))
            
    # Sort by threshold/rate difference
    triggered.sort(key=lambda pair: severity(pair[0], pair[1]))
    
    return triggered
