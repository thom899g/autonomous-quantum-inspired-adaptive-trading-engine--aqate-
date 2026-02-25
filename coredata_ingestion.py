"""
Real-time market data ingestion module with error handling and Firebase integration.
"""
import asyncio
import ccxt
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
import traceback
from dataclasses import dataclass

from config.aqate_config import config
from utils.firebase_manager import FirebaseManager

logger = logging.getLogger(__name__)

@dataclass
class MarketData:
    """Market data container with validation"""
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    vwap: Optional[float] = None
    
    def validate(self)