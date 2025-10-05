# Personal Information Dashboard

A comprehensive Python application that provides real-time weather information, latest news updates, and daily inspirational quotes through a unified API interface.

## 🌟 Features

- **Real-time Weather Data**: Get current weather conditions for any city
- **Latest News Updates**: Stay informed with the most recent news articles  
- **Daily Inspiration**: Receive motivational quotes to start your day
- **Simple API Interface**: Easy-to-use methods for all data retrieval

## 🔧 APIs Integrated

### 1. OpenWeather API
- **Purpose**: Real-time weather information
- **Endpoint**: `http://api.openweathermap.org/data/2.5/weather`
- **Data Provided**: Temperature, weather conditions, humidity, wind speed
- **Authentication**: Requires API key

### 2. News API
- **Purpose**: Current news and updates
- **Endpoint**: `https://newsapi.org/v2/everything`  
- **Data Provided**: Latest articles with titles, descriptions, and sources
- **Authentication**: Requires API key

### 3. Quotable API
- **Purpose**: Inspirational quotes
- **Endpoint**: `https://api.quotable.io/random`
- **Data Provided**: Random quotes with author information
- **Authentication**: No API key required (free public API)

## 📋 Prerequisites

- Python 3.7+
- API keys for Weather and News APIs

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd personal-information-dashboard
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```bash
   # API Keys (replace with your actual keys)
   WEATHER_API_KEY=your_openweather_api_key_here
   NEWS_API_KEY=your_news_api_key_here
   ```

## 🔑 API Key Setup

### OpenWeather API
1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Generate your API key
4. Add it to your `.env` file as `WEATHER_API_KEY`

### News API
1. Visit [NewsAPI](https://newsapi.org/)
2. Register for a free account
3. Get your API key
4. Add it to your `.env` file as `NEWS_API_KEY`

## 💻 Usage

### Basic Implementation

```python
from api_handler import APIHandler

# Initialize the API handler
api = APIHandler()

# Get weather data
weather_data = api.get_weather("New York")
if weather_data:
    print(f"Temperature: {weather_data['main']['temp']}°C")
    print(f"Condition: {weather_data['weather'][0]['description']}")

# Get latest news
news_data = api.get_news("technology", limit=5)
if news_data:
    for article in news_data['articles']:
        print(f"Title: {article['title']}")
        print(f"Source: {article['source']['name']}")

# Get random quote
quote_data = api.get_random_quote()
if quote_data:
    print(f"Quote: {quote_data['content']}")
    print(f"Author: {quote_data['author']}")
```

### API Methods

#### `get_weather(city="London")`
- **Parameters**: `city` (string, optional) - City name for weather data
- **Returns**: JSON object with weather information
- **Example**:
  ```python
  weather = api.get_weather("Paris")
  ```

#### `get_news(query="technology", limit=5)`
- **Parameters**: 
  - `query` (string, optional) - News topic or keyword
  - `limit` (int, optional) - Number of articles to retrieve
- **Returns**: JSON object with news articles
- **Example**:
  ```python
  news = api.get_news("sports", limit=10)
  ```

#### `get_random_quote()`
- **Parameters**: None
- **Returns**: JSON object with random quote and author
- **Example**:
  ```python
  quote = api.get_random_quote()
  ```

## 📁 Project Structure

```
├── api_handler.py          # Main API integration class
├── requirements.txt        # Project dependencies
├── .env                   # Environment variables (not tracked)
├── .gitignore            # Git ignore file
└── README.md             # Project documentation
```

## 🛠️ Error Handling

All API methods include comprehensive error handling:
- Network timeout protection (5-second timeout)
- HTTP status code validation
- Exception catching with descriptive error messages
- Graceful degradation (returns `None` on failure)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

## 🔗 API Documentation

- [OpenWeather API Documentation](https://openweathermap.org/api)
- [News API Documentation](https://newsapi.org/docs)
- [Quotable API Documentation](https://github.com/lukePeavey/quotable)

## ⚠️ Rate Limits

- **OpenWeather API**: 1000 calls/day (free tier)
- **News API**: 1000 requests/day (free tier)
- **Quotable API**: No rate limits (public API)

## 📞 Support

If you encounter any issues or have questions, please open an issue in this repository.