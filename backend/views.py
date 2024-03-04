from django.shortcuts import render
from . import models
import requests
from django.utils import timezone
from googletrans import Translator

# Create your views here.
def index(request):
    # API Keys and URL
    api_key = '5e6965c822764b6d8e834ca5c7703e73'
    base_url = 'https://newsapi.org/v2/top-headlines'
    
    # Time checking
    current_time = timezone.now()
    stored_time = models.TimeCheck.objects.first()
    
    # Translator
    translator = Translator()
    
    # Check if it's a new day
    if current_time.date() != stored_time.time.date():
        stored_time.time = current_time
        stored_time.save()
        
        # Remove all articles from the database
        models.Article.objects.all().delete()
        
        print("LOG: FETCHING NEW ARTICLES")

        # Fetch from different countries
        for country in ['us', 'gb', 'ru', 'cn', 'jp', 'eg']:
            
            # What is being sent
            params = {
                'apiKey': api_key,
                'country': country,
                'pageSize': 10,
            }
            
            # The http request
            response = requests.get(base_url, params=params)

            # Success
            if response.status_code == 200:
                news_data = response.json()

                for article in news_data.get('articles', []):
                    # Parse all fields
                    source = article.get("source", {}).get('name', 'No source provided.')
                    author = article.get('author', 'No author provided.')
                    title = article.get('title', 'No title provided.')
                    description = article.get('description', 'No description provided.')
                    url = article.get('url', 'No url provided.')
                    urlToImage = article.get('urlToImage', 'No image provided.')
                    content = article.get('content', 'No content provided.')
                
                    # Translate content
                    try:
                        title = translator.translate(title).text
                    except Exception as e:
                        print("LOG:", str(e))
                    try:
                        description = translator.translate(description).text
                    except Exception as e:
                        print("LOG:", str(e))
                    try:
                        translator.translate(content).text
                    except Exception as e:
                        print("LOG:", str(e))
                
                    # Create an article and save to db
                    new_article = models.Article(
                        source = source,
                        author = author,
                        title = title,
                        description = description,
                        url = url,
                        urlToImage = urlToImage,
                        content = content,
                    )
                    new_article.save()
                
            # Failure 
            else:
                print('Failed to fetch news data from ' + country)

    articles = models.Article.objects.all()
    return render(request, "index.html", {"articles": articles})