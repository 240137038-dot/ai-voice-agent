import requests
from typing import Optional, Dict, Any, List
from datetime import datetime
from loguru import logger
from cachetools import TTLCache
from weather_dashboard.config import weather_settings

class WeatherAPIClient:
    """Client for OpenWeatherMap API"""
    
    def __init__(self):
        self.api_key = weather_settings.openweather_api_key
        self.base_url = weather_settings.openweather_base_url
        self.cache = TTLCache(maxsize=100, ttl=weather_settings.cache_ttl)
        
        if not self.api_key:
            raise ValueError("OpenWeatherMap API key not configured")
        
        logger.info("WeatherAPIClient initialized")
    
    def get_current_weather(self, city: str, units: str = "metric") -> Optional[Dict[str, Any]]:
        try:
            cache_key = f"current_{city}_{units}"
            
            if cache_key in self.cache:
                logger.debug(f"Returning cached weather for {city}")
                return self.cache[cache_key]
            
            logger.info(f"Fetching current weather for {city}")
            
            url = f"{self.base_url}/weather"
            params = {"q": city, "appid": self.api_key, "units": units}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self.cache[cache_key] = data
            
            logger.info(f"Successfully fetched weather for {city}")
            return data
        
        except requests.exceptions.RequestException as e:
            logger.error(f"API request error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error fetching current weather: {e}")
            return None
    
    def get_forecast(self, city: str, count: int = 5, units: str = "metric") -> Optional[Dict[str, Any]]:
        try:
            cache_key = f"forecast_{city}_{count}_{units}"
            
            if cache_key in self.cache:
                logger.debug(f"Returning cached forecast for {city}")
                return self.cache[cache_key]
            
            logger.info(f"Fetching forecast for {city}")
            
            url = f"{self.base_url}/forecast"
            params = {"q": city, "appid": self.api_key, "units": units, "cnt": min(count, 40)}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self.cache[cache_key] = data
            
            logger.info(f"Successfully fetched forecast for {city}")
            return data
        
        except Exception as e:
            logger.error(f"Error fetching forecast: {e}")
            return None
    
    def get_coordinates(self, city: str) -> Optional[Dict[str, float]]:
        try:
            cache_key = f"coords_{city}"
            
            if cache_key in self.cache:
                return self.cache[cache_key]
            
            logger.info(f"Fetching coordinates for {city}")
            
            url = f"{self.base_url.replace('/data/2.5', '')}/geo/1.0/direct"
            params = {"q": city, "appid": self.api_key, "limit": 1}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data:
                coords = {"lat": data[0]["lat"], "lon": data[0]["lon"]}
                self.cache[cache_key] = coords
                return coords
            
            return None
        
        except Exception as e:
            logger.error(f"Error fetching coordinates: {e}")
            return None
    
    def get_weather_by_coordinates(self, lat: float, lon: float, units: str = "metric") -> Optional[Dict[str, Any]]:
        try:
            cache_key = f"coords_weather_{lat}_{lon}_{units}"
            
            if cache_key in self.cache:
                return self.cache[cache_key]
            
            logger.info(f"Fetching weather for coordinates {lat}, {lon}")
            
            url = f"{self.base_url}/weather"
            params = {"lat": lat, "lon": lon, "appid": self.api_key, "units": units}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self.cache[cache_key] = data
            
            return data
        
        except Exception as e:
            logger.error(f"Error fetching weather by coordinates: {e}")
            return None
    
    def parse_weather_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            return {
                "city": data.get("name", "Unknown"),
                "country": data.get("sys", {}).get("country", ""),
                "coordinates": {
                    "lat": data.get("coord", {}).get("lat"),
                    "lon": data.get("coord", {}).get("lon")
                },
                "temperature": {
                    "current": data.get("main", {}).get("temp"),
                    "feels_like": data.get("main", {}).get("feels_like"),
                    "min": data.get("main", {}).get("temp_min"),
                    "max": data.get("main", {}).get("temp_max")
                },
                "pressure": data.get("main", {}).get("pressure"),
                "humidity": data.get("main", {}).get("humidity"),
                "visibility": data.get("visibility"),
                "wind": {
                    "speed": data.get("wind", {}).get("speed"),
                    "direction": data.get("wind", {}).get("deg"),
                    "gust": data.get("wind", {}).get("gust")
                },
                "clouds": data.get("clouds", {}).get("all"),
                "weather": data.get("weather", [{}])[0].get("main"),
                "description": data.get("weather", [{}])[0].get("description"),
                "sunrise": data.get("sys", {}).get("sunrise"),
                "sunset": data.get("sys", {}).get("sunset"),
                "timezone": data.get("timezone"),
                "timestamp": datetime.fromtimestamp(data.get("dt", 0)).isoformat()
            }
        except Exception as e:
            logger.error(f"Error parsing weather data: {e}")
            return {}
    
    def clear_cache(self):
        self.cache.clear()
        logger.info("Weather cache cleared")
