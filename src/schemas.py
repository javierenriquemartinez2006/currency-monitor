from pydantic import BaseModel, Field
from datetime import datetime


# Internal data schema for exchange rates
class ExchangeRate(BaseModel):
    """Response from Frankfurter API."""
    
    base_currency: str
    target_currency: str
    rate: float
    timestamp: datetime
    
# Utility
def transform_api_response(raw_data: dict):
    """Convert Frankfurter API response data to a dict as the internal model."""
    
    return {'base_currency': raw_data['base'],
            'target_currency': raw_data['quote'],
            'rate': raw_data['rate'],
            'timestamp': raw_data['date']}
    
# Schema for configured alerts
class AlertSchema(BaseModel):
    """User-configured alert. Used for alert evaluation logic"""
    base_currency: str
    target_currency: str
    threshold: float
    direction: str = Field(default='above', pattern="^(above|below)$")
    
# DB record schema for alerts
class AlertEventRecord(AlertSchema):
    """Database record model for alerts"""
    trigger_rate: float
    timestamp: datetime
    rate_id: int
