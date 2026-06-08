# Weather Dashboard README

## 🌤️ Weather Dashboard

A production-ready real-time weather dashboard that fetches data from OpenWeatherMap API, stores historical records, manages favorites, and provides a beautiful web interface.

### ✨ Features

✅ **Real-time Weather Data**
- Current conditions for any city
- Temperature, humidity, pressure, wind speed
- Weather descriptions and conditions
- Sunrise/sunset times, visibility, cloud coverage

✅ **Weather Forecasts**
- 5-day, 3-hour interval forecasts
- Temperature trends and predictions

✅ **Favorites Management**
- Save favorite cities
- Quick access to frequently checked locations
- Persistent storage

✅ **Weather History**
- Historical data tracking
- Temperature trend analysis

✅ **Alerts System**
- Custom weather alerts
- Temperature, wind, and humidity thresholds

✅ **Smart Caching**
- 5-minute TTL for API calls
- Reduced API usage and faster responses

✅ **Beautiful Web Interface**
- Responsive design
- Real-time search
- Error handling

### 📦 Installation

#### Option 1: Direct Python Setup

1. **Get API Key**
   ```bash
   # Visit https://openweathermap.org/api
   # Sign up for free API key
   ```

2. **Configure Environment**
   ```bash
   cp weather_dashboard/.env.example .env
   # Edit .env and add your OPENWEATHER_API_KEY
   ```

3. **Install Dependencies**
   ```bash
   pip install -r weather_dashboard/requirements.txt
   ```

4. **Run Dashboard**
   ```bash
   python run_weather_dashboard.py
   ```

5. **Access**
   - Open http://localhost:8000 in your browser

#### Option 2: Docker

```bash
# Configure
cp weather_dashboard/.env.example .env
# Edit .env with your API key

# Run with Docker Compose
docker-compose -f weather_dashboard/docker-compose.yml up
```

### 🚀 API Endpoints

**Weather Data:**
- `GET /api/weather/<city>` - Current weather for a city
- `GET /api/forecast/<city>` - 5-day forecast
- `GET /api/coordinates/<city>` - City coordinates
- `GET /api/status` - Dashboard status

**Favorites:**
- `GET /api/favorites` - List all favorites
- `POST /api/favorites` - Add favorite city
- `DELETE /api/favorites/<city>` - Remove favorite

**Alerts:**
- `GET /api/alerts` - List alerts
- `POST /api/alerts` - Create alert

### 📚 Usage Examples

```python
from weather_dashboard.api_client import WeatherAPIClient

# Create client
client = WeatherAPIClient()

# Get current weather
weather = client.get_current_weather("London", units="metric")
parsed = client.parse_weather_data(weather)
print(parsed)

# Get forecast
forecast = client.get_forecast("Paris", count=5)

# Get coordinates
coords = client.get_coordinates("New York")
```

### ⚙️ Configuration

Edit `.env` file:

```env
OPENWEATHER_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///weather_dashboard.db
CACHE_TTL=300
DEBUG=False
ENABLE_FORECASTS=True
ENABLE_ALERTS=True
ENABLE_HISTORY=True
```

### 🛠️ Development

```bash
# Run in debug mode
DEBUG=True python run_weather_dashboard.py

# View logs
tail -f logs/weather_dashboard.log

# Run examples
python weather_dashboard/examples.py
```

### 📊 Database Models

- **WeatherRecord** - Historical weather data
- **Alert** - Weather alerts
- **Favorite** - Favorite cities

### 🐳 Docker

```bash
docker build -t weather-dashboard weather_dashboard/
docker run -p 8000:8000 weather-dashboard
```

### 📝 License

MIT
