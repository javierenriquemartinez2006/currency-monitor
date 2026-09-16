# -- schemas.py --

from pydantic import BaseModel, Field
from datetime import datetime

# Internal data schema for exchange rates
class ExchangeRate(BaseModel):
    """Response from Frankfurter API."""
    
    base_currency: str
    target_currency: str
    rate: float
    timestamp: datetime
  
# Schema for configured alerts
class AlertSchema(BaseModel):
    """User-configured alert. Used for alert evaluation logic"""
    base_currency: str
    target_currency: str
    threshold: float
    direction: str = Field(default='above', pattern="^(above|below)$")
    
    # Utility for calculating reciprocal AlertSchema
    def reciprocal(self) -> AlertSchema:
        """Calculate the reciprocal equivalent to an alert"""
        
        reciprocal = AlertSchema(
            # Invert base and target currencies
            base_currency = self.target_currency,
            target_currency = self.base_currency,
        
            # Calculate reciprocal 
            threshold = 1 / self.threshold,
            
            # Invert trigger direction
            direction = 'above' if self.direction == 'below' else 'below'
        )
            
        return reciprocal

# DB record schema for alerts
class AlertEventRecord(AlertSchema):
    """Database record model for alerts"""
    trigger_rate: float
    timestamp: datetime
    rate_id: int
