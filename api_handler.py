import requests
import os
from dotenv import load_dotenv

load_dotenv()

class APIHandler:
    def __init__(self):
        self.weather_api_key = os.getenv('WEATHER_API_KEY')
        self.news_api_key = os.getenv('NEWS_API_KEY')
    
    def get_weather(self, city="London"):
        """Fetch weather data from OpenWeatherMap API"""
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': city,
                'appid': self.weather_api_key,
                'units': 'metric'
            }
            response = requests.get(url, params=params, timeout=5)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Weather API error: {e}")
            return None
    
    def get_news(self, query="technology", limit=5):
        """Fetch news from NewsAPI"""
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': query,
                'apiKey': self.news_api_key,
                'pageSize': limit,
                'sortBy': 'publishedAt'
            }
            response = requests.get(url, params=params, timeout=5)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"News API error: {e}")
            return None
    
    def get_random_quote(self):
        """Fetch random quote from free API"""
        try:
            url = "https://api.quotable.io/random"
            response = requests.get(url, timeout=5)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Quote API error: {e}")
            return None
