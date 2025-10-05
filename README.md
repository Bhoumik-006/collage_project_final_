# Personal Information Dashboard

A comprehensive Python application that provides real-time weather information, latest news updates, and daily inspirational quotes through a unified API interface.

## 🌟 Features

- **Real-time Weather Data**: Get current weather conditions for any city
- **Latest News Updates**: Stay informed with the most recent news articles  
- **Daily Inspiration**: Receive motivational quotes to start your day
- **Simple API Interface**: Easy-to-use methods for all data retrieval

## 🔧 APIs Integrated

### 1. OpenWeather API 🌤️
- **Purpose**: Real-time weather information for any city worldwide
- **Provider**: OpenWeatherMap
- **Endpoint**: `http://api.openweathermap.org/data/2.5/weather`
- **Installation**: No additional packages required (uses `requests`)
- **Data Provided**: 
  - Current temperature (Celsius/Fahrenheit)
  - Weather conditions (sunny, cloudy, rainy, etc.)
  - Humidity and atmospheric pressure
  - Wind speed and direction
  - Visibility and cloud coverage
- **Authentication**: Requires free API key
- **Rate Limit**: 1,000 calls/day (free tier), 60 calls/minute
- **Use Case**: Display current weather for user's location or any specified city

### 2. News API 📰
- **Purpose**: Access to current news articles and headlines
- **Provider**: NewsAPI.org
- **Endpoint**: `https://newsapi.org/v2/everything`
- **Installation**: No additional packages required (uses `requests`)
- **Data Provided**:
  - Latest news articles with titles and descriptions
  - Article URLs for full content
  - Publication dates and source information
  - Author details and article images
  - Customizable by topic, source, or keyword
- **Authentication**: Requires free API key
- **Rate Limit**: 1,000 requests/day (free tier)
- **Use Case**: Keep users informed with personalized news feeds and trending topics

### 3. Quotable API 💭
- **Purpose**: Daily inspiration and motivational content
- **Provider**: Quotable (Open Source)
- **Endpoint**: `https://api.quotable.io/random`
- **Installation**: No additional packages required (uses `requests`)
- **Data Provided**:
  - Random inspirational and motivational quotes
  - Author information and biographical details
  - Quote categories and tags
  - Length-based quote filtering
- **Authentication**: No API key required (completely free)
- **Rate Limit**: No restrictions (public API)
- **Use Case**: Provide daily motivation, inspiration for productivity apps, or educational content

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

## 🔑 API Installation & Setup

### Required Python Packages
```bash
# Install all required packages
pip install -r requirements.txt

# Or install individually:
pip install requests>=2.31.0
pip install python-dotenv>=1.0.0
```

### OpenWeather API Setup 🌤️
1. **Sign Up**: Visit [OpenWeatherMap](https://openweathermap.org/api)
2. **Create Account**: Register for a free account
3. **Generate API Key**: 
   - Go to "API Keys" section in your account
   - Copy your default API key
4. **Add to Environment**: 
   ```bash
   WEATHER_API_KEY=your_actual_api_key_here
   ```
5. **Verify Setup**: Test with a simple API call
6. **Free Tier Limits**: 1,000 calls/day, 60 calls/minute

### News API Setup 📰
1. **Sign Up**: Visit [NewsAPI.org](https://newsapi.org/)
2. **Register Account**: Create free developer account
3. **Get API Key**: 
   - Access your dashboard
   - Copy your API key from the account page
4. **Add to Environment**:
   ```bash
   NEWS_API_KEY=your_news_api_key_here
   ```
5. **Verify Setup**: Test with a sample news request
6. **Free Tier Limits**: 1,000 requests/day

### Quotable API Setup 💭
- **No Setup Required**: Completely free public API
- **No Registration**: No account or API key needed
- **No Rate Limits**: Unlimited usage
- **Ready to Use**: Works immediately with requests library

## 💻 Usage & Implementation

### Quick Start Example

```python
from api_handler import APIHandler

# Initialize the API handler
api = APIHandler()

# 🌤️ Weather API Usage
weather_data = api.get_weather("New York")
if weather_data:
    temp = weather_data['main']['temp']
    condition = weather_data['weather'][0]['description']
    humidity = weather_data['main']['humidity']
    print(f"🌡️ Temperature: {temp}°C")
    print(f"☁️ Condition: {condition.title()}")
    print(f"💧 Humidity: {humidity}%")

# 📰 News API Usage
news_data = api.get_news("technology", limit=5)
if news_data and 'articles' in news_data:
    print("\n📰 Latest Tech News:")
    for i, article in enumerate(news_data['articles'][:3], 1):
        print(f"{i}. {article['title']}")
        print(f"   Source: {article['source']['name']}")
        print(f"   URL: {article['url']}")

# 💭 Quote API Usage
quote_data = api.get_random_quote()
if quote_data:
    print(f"\n💭 Daily Inspiration:")
    print(f"'{quote_data['content']}'")
    print(f"— {quote_data['author']}")
```

### Advanced Usage Examples

```python
# Custom weather for multiple cities
cities = ["London", "Tokyo", "Sydney"]
for city in cities:
    weather = api.get_weather(city)
    if weather:
        temp = weather['main']['temp']
        print(f"{city}: {temp}°C")

# Specific news topics
topics = ["python", "artificial intelligence", "climate change"]
for topic in topics:
    news = api.get_news(topic, limit=2)
    if news:
        print(f"\nNews about {topic.title()}:")
        for article in news['articles']:
            print(f"- {article['title']}")

# Multiple inspirational quotes
for i in range(3):
    quote = api.get_random_quote()
    if quote:
        print(f"{i+1}. \"{quote['content']}\" - {quote['author']}")
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