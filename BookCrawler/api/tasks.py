from background_task import background
import requests
import datetime
from bs4 import BeautifulSoup
from crawler.models import Category, Book

@background(schedule=3)
def demo_task(message):
    get_categories()

def get_categories():
    url = 'http://books.toscrape.com/index.html'
    url_html = requests.get(url)
    soup = BeautifulSoup(url_html.content, 'html.parser')
    categories = soup.select('[href*="catalogue/category/books/"]')
    for c in categories:
        name = c.getText().strip()
        name_route = c['href']
        cur_category = Category.objects.filter(name=name)
        if cur_category:
            print('Category already exists')
        else:
            new_category = Category(name=name, route_name=name_route, extraction_date=datetime.datetime.now())
            new_category.save()
    return categories


    