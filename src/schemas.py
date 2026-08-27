from pydantic import BaseModel
from datetime import datetime


# Internal data schema
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
