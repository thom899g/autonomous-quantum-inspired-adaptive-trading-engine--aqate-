"""
AQATE Configuration Module
Centralized configuration management with environment variables and defaults.
"""
import os
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

# Environment variable fallbacks with production-safe defaults
class Environment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

@dataclass
class ExchangeConfig:
    """Exchange-specific configuration"""
    name: str = "binance"
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    testnet: bool = True
    rate_limit: bool = True
    timeout: int = 30000  # milliseconds
    enable_rate_limit: bool = True
    
    def __post_init__(self):
        self.api_key = os.getenv(f"{self.name.upper()}_API_KEY", self.api_key)
        self.api_secret = os.getenv(f"{self.name.upper()}_API_SECRET", self.api_secret)

@dataclass
class FirebaseConfig:
    """Firebase configuration for state management"""
    project_id: Optional[str] = None
    credentials_path: Optional[str] = None
    firestore_collection: str = "aqate_state"
    realtime_database_url: Optional[str] = None
    
    def __post_init__(self):
        self.project_id = os.getenv("FIREBASE_PROJECT_ID", self.project_id)
        self.credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH", self.credentials_path)

@dataclass
class TradingConfig:
    """Trading parameters"""
    symbols: list = field(default_factory=lambda: ["BTC/USDT", "ETH/USDT"])
    timeframe: str = "1h"
    initial_capital: float = 10000.0
    risk_per_trade: float = 0.02  # 2% risk per trade
    max_position_size: float = 0.1  # 10% of capital
    commission: float = 0.001  # 0.1% commission

@dataclass
class QIAlgorithmConfig:
    """Quantum-Inspired Algorithm configuration"""
    population_size: int = 100
    num_generations: int = 50
    mutation_rate: float = 0.1
    crossover_rate: float = 0.7
    qubit_rotation_angle: float = 0.01 * 3.14159
    measurement_iterations: int = 1000

@dataclass
class RLConfig:
    """Reinforcement Learning configuration"""
    state_size: int = 10
    action_size: int = 3  # Buy, Sell, Hold
    learning_rate: float = 0.001
    discount_factor: float = 0.95
    epsilon_start: float = 1.0
    epsilon_end: float = 0.01
    epsilon_decay: float = 0.995
    memory_size: int = 2000
    batch_size: int = 32

class AQATEConfig:
    """Main configuration class"""
    
    def __init__(self, env: str = None):
        self.environment = Environment(env or os.getenv("AQATE_ENV", "development"))
        self.exchange = ExchangeConfig()
        self.firebase = FirebaseConfig()
        self.trading = TradingConfig()
        self.qi_algorithm = QIAlgorithmConfig()
        self.rl = RLConfig()
        self.log_level = logging.DEBUG if self.environment == Environment.DEVELOPMENT else logging.INFO
        
        # Validate critical configurations
        self._validate_config()
        
    def _validate_config(self) -> None:
        """Validate critical configuration values"""
        if not self.exchange.api_key and not self.exchange.testnet:
            logging.warning("No API key provided - using testnet mode")
            self.exchange.testnet = True
            
        if not self.firebase.project_id and self.environment == Environment.PRODUCTION:
            logging.error("Firebase project ID required for production")
            raise ValueError("Firebase configuration required")
            
    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary for logging"""
        config_dict = {
            "environment": self.environment.value,
            "exchange": {
                "name": self.exchange.name,
                "testnet": self.exchange.testnet,
                "timeout": self.exchange.timeout
            },
            "trading": {
                "symbols": self.trading.symbols,
                "timeframe": self.trading.timeframe,
                "initial_capital": self.trading.initial_capital
            }
        }
        return config_dict

# Global configuration instance
config = AQATEConfig()