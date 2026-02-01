import dotenv
import os
import csv
import time
import requests
import pandas as pd
from pytrends.request import TrendReq

# YouTube API Key (Replace with your own API key)
conf = dotenv.dotenv_values('../.env')
YOUTUBE_API_KEY = conf['API_KEY']
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/videos"


def get_trending_videos(region_code="US", max_results=50):
    """Fetch trending video titles and descriptions from YouTube using requests"""
    params = {
        "part": "snippet",
        "chart": "mostPopular",
        "regionCode": region_code,
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(YOUTUBE_API_URL, params=params)
    data = response.json()

    categories = {}
    keywords = []

    for item in data.get("items", []):
        title = item["snippet"]["title"]
        description = item["snippet"].get("description", "")
        category_id = item["snippet"].get("categoryId", "unknown")
        keywords.extend(title.split())  # Basic keyword extraction from title
        keywords.extend(description.split())

        if category_id in categories:
            categories[category_id] += 1
        else:
            categories[category_id] = 1

    top_category = max(categories, key=categories.get) if categories else "unknown"
    return list(set(keywords)), top_category  # Remove duplicates and return top category

def get_search_volume(keywords, country="US"):
    """Fetch average search volume for keywords using Google Trends"""
    pytrends = TrendReq()
    keyword_data = {}

    for keyword in keywords:
        try:
            pytrends.build_payload([keyword], cat=0, timeframe='now 7-d', geo=country, gprop='youtube')
            data = pytrends.interest_over_time()
            if not data.empty:
                avg_volume = data[keyword].mean()
                keyword_data[keyword] = avg_volume
        except Exception as e:
            print(f"Error fetching data for {keyword}: {e}")
        time.sleep(1)  # Avoid API rate limits

    return keyword_data

def save_to_csv(data, filename="trending_keywords.csv"):
    """Save keyword search volume data to CSV file"""
    df = pd.DataFrame(data.items(), columns=["Keyword", "Avg Search Volume"])
    df = df.sort_values(by="Avg Search Volume", ascending=False).head(10)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    trending_keywords, niche = get_trending_videos(region_code="US")
    search_volume_data = get_search_volume(trending_keywords, country="US")
    save_to_csv(search_volume_data, f"{niche}_trending_keywords.csv")
