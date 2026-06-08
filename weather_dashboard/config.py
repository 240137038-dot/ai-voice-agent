import os
from dotenv import load_dotenv
from pydantic import BaseSettings
from typing import Optional

load_dotenv()

class WeatherSettings(BaseSettings):
    """Weather Dashboard Configuration"""
    
    # API Configuration
    openweather_api_key: str = os.getenv("OPENWEATHER_API_KEY", "")
    openweather_base_url: str = os.getenv("OPENWEATHER_BASE_URL", "https://api.openweathermap.org/data/2.5")
    
    # Database Configuration
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///weather_dashboard.db")
    
    # Cache Configuration
    cache_ttl: int = int(os.getenv("CACHE_TTL", "300"))  # 5 minutes
    
    # UI Configuration
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    
    # Features
    enable_forecasts: bool = os.getenv("ENABLE_FORECASTS", "True").lower() == "true"
    enable_alerts: bool = os.getenv("ENABLE_ALERTS", "True").lower() == "true"
    enable_history: bool = os.getenv("ENABLE_HISTORY", "True").lower() == "true"
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "logs/weather_dashboard.log")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

weather_settings = WeatherSettings()
