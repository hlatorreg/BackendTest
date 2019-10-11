import datetime
from urllib.parse import urlparse

import requests
from background_task import background
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict

from api.models import Book, Category


@background(schedule=3)
def crawl_bookstore():
    task_config    = load_config()
    url            = task_config['TARGET']['url']
    html_table_map = task_config['MAP']
    crawl_categories(url)
    crawl_books(url, html_table_map)

def crawl_categories(url):
    url_html   = requests.get(url)
    index_soup = BeautifulSoup(url_html.content, 'html.parser')
    categories = index_soup.select('[href*="catalogue/category/books/"]')
    for c in categories:
        name = c.getText().strip()
        cur_category = Category.objects.filter(name=name)
        if cur_category:
            pass
        else:
            new_category = Category(name=name)
            new_category.save()

def crawl_books(url, html_table_map):
    counter = 1
    host = url
    while True:
        url_html        = requests.get(url)
        parsed_url      = urlparse(url)
        current_route   = host if 'catalogue' not in parsed_url.path else host + 'catalogue/'
        soup            = BeautifulSoup(url_html.content, 'html.parser')
        this_page_books = soup.select('article.product_pod')
        counter+=1
        for book in this_page_books:
            book_model_title         = book.select_one('h3 > a')['title']
            book_model_thumbnail_url = host+book.select_one('a > img.thumbnail')['src'].replace('../','')
            book_model_price         = book.select_one('div.product_price > p.price_color').getText()
            book_model_stock         = True if book.select_one('div.product_price > p.instock').getText().strip() == 'In stock' else False
            book_url                 = current_route+book.select_one('div.image_container > a')['href']
            book_page                = requests.get(book_url)
            book_soup                = BeautifulSoup(book_page.content, 'html.parser')
            book_datatable           = book_soup.select_one('article.product_page > table')
            book_data                = book_datatable.select('tr')
            book_model_description   = book_soup.select_one('div#product_description + p').getText() if book_soup.select_one('div#product_description + p') else ''
            book_model_category_name = book_soup.select_one('[href*="../category/books/"]').getText().strip()
            book_model_category_id   = get_model_category(book_model_category_name)
            for row in book_datatable.select('tr'):
                row_head  = row.select_one('th').getText()
                row_value = row.select_one('td').getText()
                book_data = [row_value for option in html_table_map if row_head == html_table_map[option]]
                if book_data:
                    book_model_upc = book_data[0]
                    break
            try:
                Book.objects.get(upc=book_model_upc)
            except ObjectDoesNotExist as exc:
                book_model = Book(
                    category_id         = book_model_category_id,
                    title               = book_model_title,
                    thumbnail_url       = book_model_thumbnail_url,
                    price               = book_model_price,
                    stock               = book_model_stock,
                    product_description = book_model_description,
                    upc                 = book_model_upc
                )
                book_model.save()
        next_button = soup.select_one('li.next > a')
        if next_button:
            url = current_route+next_button['href']
        else:
            break
    print('Crawling done!')

def load_config():
    import configparser
    config = configparser.ConfigParser()
    config.read('api/config.ini')
    config.sections()
    return config

def get_all_model_categories():
    return Category.objects.all().values()

def get_model_category(value):
    category = Category.objects.get(name=value)
    if category:
        return category
    else:
        return None

def get_model_book_by_id(search_value):
    try:
        return model_to_dict(Book.objects.get(id=search_value))
    except ObjectDoesNotExist as exc:
        return {"error": "ID not found."}

def get_model_book_by_upc(search_value):
    try:
        return model_to_dict(Book.objects.get(upc=search_value))
    except ObjectDoesNotExist as exc:
        return {"error": "UPC not found."}

def create_api_user(name, password):
    users = list(User.objects.all().values())
    if len(users) >= 10:
        return 'Max user count reached'
    elif User.objects.filter(username=name).exists():
        return 'User already exists'
    else:
        user = User.objects.create_user(username=name, password=password)
        user.save()
        return True

def is_authenticated(request):
    import json
    from django.contrib.auth import authenticate, login
    login_data = json.loads(request.body.decode('utf-8'))
    if 'username' not in login_data.keys() or 'password' not in login_data.keys():
        return False
    if User.objects.filter(username=login_data['username']).exists():
        return authenticate(request, username=login_data['username'], password=login_data['password'])
