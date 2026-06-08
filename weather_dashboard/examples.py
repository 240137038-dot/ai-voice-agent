# Weather Dashboard - Usage Examples

from weather_dashboard.api_client import WeatherAPIClient
from weather_dashboard.database import DatabaseManager
import json

def example_1_current_weather():
    """Example 1: Fetch current weather"""
    print("=" * 50)
    print("Example 1: Current Weather")
    print("=" * 50)
    
    client = WeatherAPIClient()
    weather = client.get_current_weather("New York")
    
    if weather:
        parsed = client.parse_weather_data(weather)
        print(json.dumps(parsed, indent=2))

def example_2_forecast():
    """Example 2: Get forecast"""
    print("\n" + "=" * 50)
    print("Example 2: Weather Forecast")
    print("=" * 50)
    
    client = WeatherAPIClient()
    forecast = client.get_forecast("London", count=5)
    
    if forecast:
        print(f"Forecast for {forecast['city']['name']}:")
        for item in forecast['list'][:5]:
            print(f"  - {item['dt_txt']}: {item['main']['temp']}°C - {item['weather'][0]['main']}")

def example_3_database():
    """Example 3: Save and retrieve weather history"""
    print("\n" + "=" * 50)
    print("Example 3: Weather History")
    print("=" * 50)
    
    client = WeatherAPIClient()
    db = DatabaseManager()
    
    weather = client.get_current_weather("Tokyo")
    if weather:
        parsed = client.parse_weather_data(weather)
        db.save_weather_record(parsed)
        print(f"Saved weather for {parsed['city']}")
        
        history = db.get_weather_history("Tokyo", limit=5)
        print(f"\nWeather History for Tokyo ({len(history)} records):")
        for record in history:
            print(f"  - {record.timestamp}: {record.temperature}°C, {record.weather}")

def example_4_favorites():
    """Example 4: Manage favorite cities"""
    print("\n" + "=" * 50)
    print("Example 4: Favorite Cities")
    print("=" * 50)
    
    db = DatabaseManager()
    
    cities = [("New York", "US"), ("London", "GB"), ("Tokyo", "JP"), ("Paris", "FR")]
    
    for city, country in cities:
        db.add_favorite(city, country)
        print(f"Added {city}, {country} to favorites")
    
    favorites = db.get_favorites()
    print(f"\nTotal favorites: {len(favorites)}")
    for fav in favorites:
        print(f"  - {fav.city}, {fav.country}")

def example_5_alerts():
    """Example 5: Create weather alerts"""
    print("\n" + "=" * 50)
    print("Example 5: Weather Alerts")
    print("=" * 50)
    
    db = DatabaseManager()
    
    alerts_config = [
        ("New York", "temperature", "exceeds", 35),
        ("New York", "wind_speed", "exceeds", 50),
        ("London", "humidity", "below", 30),
        ("Tokyo", "temperature", "below", 0),
    ]
    
    for city, alert_type, condition, threshold in alerts_config:
        db.create_alert(city, alert_type, condition, threshold)
        print(f"Created alert: {city} - {alert_type} {condition} {threshold}")
    
    alerts = db.get_alerts("New York")
    print(f"\nAlerts for New York: {len(alerts)}")
    for alert in alerts:
        print(f"  - {alert.alert_type}: {alert.condition} {alert.threshold}")

def example_6_coordinates():
    """Example 6: Get city coordinates"""
    print("\n" + "=" * 50)
    print("Example 6: City Coordinates")
    print("=" * 50)
    
    client = WeatherAPIClient()
    cities = ["New York", "Sydney", "Dubai", "Berlin"]
    
    for city in cities:
        coords = client.get_coordinates(city)
        if coords:
            print(f"{city}: Latitude {coords['lat']:.2f}, Longitude {coords['lon']:.2f}")

if __name__ == "__main__":
    try:
        example_1_current_weather()
        example_2_forecast()
        example_3_database()
        example_4_favorites()
        example_5_alerts()
        example_6_coordinates()
        
        print("\n" + "=" * 50)
        print("All examples completed!")
        print("=" * 50)
    
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
