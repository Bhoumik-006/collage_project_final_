# API Integration Guide for StudentConnect Project

This document describes the APIs integrated into the StudentConnect college event management system and the additional Personal Information Dashboard features.

## 🎯 Project Overview

**StudentConnect** is a Django-based college event management system enhanced with real-time API integrations for weather, news, and inspirational content.

## 🔧 APIs Integrated

### 1. OpenWeather API 🌤️
- **Purpose**: Real-time weather information for event planning
- **Provider**: OpenWeatherMap
- **Endpoint**: `http://api.openweathermap.org/data/2.5/weather`
- **Installation**: No additional packages required (uses `requests`)
- **Integration Location**: `api_handler.py`
- **Data Provided**: 
  - Current temperature for event locations
  - Weather conditions for outdoor events
  - Humidity and wind information
  - Weather-based event recommendations
- **Authentication**: Requires free API key
- **Rate Limit**: 1,000 calls/day (free tier), 60 calls/minute
- **Use Case**: 
  - Help event organizers plan outdoor activities
  - Display weather conditions on event pages
  - Send weather alerts for upcoming events

### 2. News API 📰
- **Purpose**: Campus news and educational content integration
- **Provider**: NewsAPI.org
- **Endpoint**: `https://newsapi.org/v2/everything`
- **Installation**: No additional packages required (uses `requests`)
- **Integration Location**: `api_handler.py`
- **Data Provided**:
  - Educational news and updates
  - Technology and innovation articles
  - Campus-related news feeds
  - Event-relevant news content
- **Authentication**: Requires free API key
- **Rate Limit**: 1,000 requests/day (free tier)
- **Use Case**: 
  - Display relevant news on student dashboard
  - Educational content for academic events
  - Current affairs for debate competitions
  - Technology news for tech events

### 3. Quotable API 💭
- **Purpose**: Daily motivation and educational quotes
- **Provider**: Quotable (Open Source)
- **Endpoint**: `https://api.quotable.io/random`
- **Installation**: No additional packages required (uses `requests`)
- **Integration Location**: `api_handler.py`
- **Data Provided**:
  - Inspirational quotes for students
  - Educational and motivational content
  - Famous quotes by category
  - Author information and biographies
- **Authentication**: No API key required (completely free)
- **Rate Limit**: No restrictions (public API)
- **Use Case**: 
  - Daily inspiration on student dashboard
  - Motivational content for events
  - Educational quotes for academic events
  - Wellness and mental health support

## 🚀 Installation & Setup

### 1. Install Required Packages
```bash
# Core API requirements (already in Django requirements.txt)
pip install requests>=2.31.0
pip install python-dotenv>=1.0.0

# Or install from requirements.txt
pip install -r requirements.txt
```

### 2. Environment Configuration

Create or update your `.env` file in the Django project root:

```bash
# Django Settings
SECRET_KEY=your_django_secret_key
DEBUG=True

# Database Configuration  
DATABASE_URL=your_database_url

# API Keys for External Services
WEATHER_API_KEY=your_openweather_api_key_here
NEWS_API_KEY=your_news_api_key_here

# Email Configuration (if using)
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_email_password
```

### 3. API Key Setup

#### OpenWeather API Setup 🌤️
1. **Sign Up**: Visit [OpenWeatherMap](https://openweathermap.org/api)
2. **Create Account**: Register for a free account
3. **Generate API Key**: 
   - Go to "API Keys" section in your account
   - Copy your default API key
4. **Add to Django Settings**: Add `WEATHER_API_KEY` to your `.env` file
5. **Free Tier Limits**: 1,000 calls/day, 60 calls/minute

#### News API Setup 📰
1. **Sign Up**: Visit [NewsAPI.org](https://newsapi.org/)
2. **Register Account**: Create free developer account
3. **Get API Key**: Copy API key from your dashboard
4. **Add to Django Settings**: Add `NEWS_API_KEY` to your `.env` file
5. **Free Tier Limits**: 1,000 requests/day

#### Quotable API Setup 💭
- **No Setup Required**: Completely free public API
- **No Authentication**: Ready to use immediately

## 💻 Django Integration Examples

### 1. View Integration

```python
# views.py
from django.shortcuts import render
from .api_handler import APIHandler

def dashboard(request):
    api = APIHandler()
    
    # Get weather for college location
    weather_data = api.get_weather("Mumbai")  # Replace with your city
    
    # Get educational news
    news_data = api.get_news("education technology", limit=3)
    
    # Get daily inspiration
    quote_data = api.get_random_quote()
    
    context = {
        'weather': weather_data,
        'news': news_data,
        'quote': quote_data,
        # ... other context data
    }
    
    return render(request, 'dashboard.html', context)
```

### 2. Template Usage

```html
<!-- dashboard.html -->
<div class="api-widgets">
    <!-- Weather Widget -->
    {% if weather %}
    <div class="weather-widget">
        <h3>🌤️ Campus Weather</h3>
        <p>Temperature: {{ weather.main.temp }}°C</p>
        <p>Condition: {{ weather.weather.0.description|title }}</p>
        <p>Humidity: {{ weather.main.humidity }}%</p>
    </div>
    {% endif %}

    <!-- News Widget -->
    {% if news.articles %}
    <div class="news-widget">
        <h3>📰 Educational News</h3>
        {% for article in news.articles|slice:":3" %}
        <div class="news-item">
            <h4>{{ article.title }}</h4>
            <p>{{ article.description }}</p>
            <a href="{{ article.url }}" target="_blank">Read More</a>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <!-- Quote Widget -->
    {% if quote %}
    <div class="quote-widget">
        <h3>💭 Daily Inspiration</h3>
        <blockquote>
            "{{ quote.content }}"
            <cite>— {{ quote.author }}</cite>
        </blockquote>
    </div>
    {% endif %}
</div>
```

### 3. Event-Specific API Usage

```python
# Event planning with weather integration
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    api = APIHandler()
    
    # Get weather for event location and date
    if event.location and event.is_outdoor:
        weather_data = api.get_weather(event.location)
        
        # Weather recommendations
        weather_recommendation = None
        if weather_data:
            temp = weather_data['main']['temp']
            condition = weather_data['weather'][0]['main'].lower()
            
            if 'rain' in condition:
                weather_recommendation = "⚠️ Rain expected. Consider indoor backup."
            elif temp < 15:
                weather_recommendation = "🧥 Cool weather. Suggest warm clothing."
            elif temp > 30:
                weather_recommendation = "☀️ Hot weather. Ensure hydration stations."
    
    # Get relevant news for academic events
    relevant_news = None
    if event.category in ['academic', 'technology', 'research']:
        relevant_news = api.get_news(f"{event.category} {event.title}", limit=2)
    
    context = {
        'event': event,
        'weather': weather_data,
        'weather_recommendation': weather_recommendation,
        'relevant_news': relevant_news,
    }
    
    return render(request, 'event_detail.html', context)
```

## 🛠️ Error Handling & Best Practices

### 1. API Error Handling

```python
# Enhanced api_handler.py with Django logging
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class APIHandler:
    def get_weather_with_fallback(self, city="Mumbai"):
        try:
            weather_data = self.get_weather(city)
            if weather_data:
                return weather_data
            else:
                logger.warning(f"Weather API returned no data for {city}")
                return self.get_fallback_weather()
        except Exception as e:
            logger.error(f"Weather API error: {e}")
            return self.get_fallback_weather()
    
    def get_fallback_weather(self):
        return {
            'main': {'temp': 25, 'humidity': 60},
            'weather': [{'description': 'Data unavailable'}]
        }
```

### 2. Caching for Performance

```python
# utils.py - Django cache integration
from django.core.cache import cache
from .api_handler import APIHandler

def get_cached_weather(city, timeout=1800):  # 30 minutes cache
    cache_key = f"weather_{city}"
    weather_data = cache.get(cache_key)
    
    if not weather_data:
        api = APIHandler()
        weather_data = api.get_weather(city)
        if weather_data:
            cache.set(cache_key, weather_data, timeout)
    
    return weather_data
```

## 📊 StudentConnect + API Integration Benefits

### For Students:
- 🌤️ **Weather-aware event planning**: Know weather conditions before outdoor events
- 📰 **Educational content**: Stay updated with relevant academic news
- 💭 **Daily motivation**: Inspirational quotes for academic success
- 📅 **Smart event recommendations**: Weather-based event suggestions

### For Event Organizers:
- 🌦️ **Weather alerts**: Automatic weather warnings for outdoor events  
- 📰 **Content integration**: Relevant news for academic events
- 📊 **Data-driven decisions**: Weather data for event planning
- 🎯 **Enhanced engagement**: Rich content for event pages

### For Administrators:
- 📈 **Analytics integration**: Weather and news data for insights
- ⚠️ **Risk management**: Weather-based event risk assessment
- 📊 **Content management**: Automated news and quote updates
- 🔧 **System enhancement**: Rich API data for better user experience

## 🔗 Related Files in StudentConnect Project

- `api_handler.py` - Main API integration class
- `views.py` - Django views using API data
- `templates/` - HTML templates with API widgets
- `requirements.txt` - Package dependencies
- `.env` - Environment configuration
- `settings.py` - Django settings with API configurations

## 📞 Support & Documentation

- **OpenWeather API**: [Documentation](https://openweathermap.org/api)
- **News API**: [Documentation](https://newsapi.org/docs)
- **Quotable API**: [Documentation](https://github.com/lukePeavey/quotable)
- **Django Integration**: See project's main README.md

## ⚠️ Rate Limits & Usage Guidelines

- **OpenWeather API**: 1,000 calls/day (free tier)
- **News API**: 1,000 requests/day (free tier)  
- **Quotable API**: No rate limits
- **Recommendation**: Implement caching to minimize API calls
- **Best Practice**: Use error handling and fallback data for reliability