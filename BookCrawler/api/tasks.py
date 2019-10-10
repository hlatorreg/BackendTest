from background_task import background
import requests
import datetime
from bs4 import BeautifulSoup
from api.models import Category, Book
from urllib.parse import urlparse

@background(schedule=3)
def crawl_bookstore():
    task_config    = load_config()
    url            = task_config['TARGET']['url']
    html_table_map = task_config['MAP']
    get_categories(url)
    get_books(url, html_table_map)

def get_categories(url):
    url_html   = requests.get(url)
    index_soup = BeautifulSoup(url_html.content, 'html.parser')
    categories = index_soup.select('[href*="catalogue/category/books/"]')
    for c in categories:
        name = c.getText().strip()
        name_route = c['href']
        cur_category = Category.objects.filter(name=name)
        if cur_category:
            print('Category already exists')
        else:
            new_category = Category(name=name, route_name=name_route)
            new_category.save()

def get_books(url, html_table_map):
    url_html        = requests.get(url)
    parsed_url      = urlparse(url)
    host            = parsed_url.hostname
    soup            = BeautifulSoup(url_html.content, 'html.parser')
    this_page_books = soup.select('article.product_pod')
    for book in this_page_books:
        book_model               = Book()
        book_model_title         = book.select_one('h3 > a')['title']
        book_model_thumbnail_url = book.select_one('a > img.thumbnail')['src']
        book_model_price         = book.select_one('div.product_price > p.price_color').getText()
        book_model_stock         = True if book.select_one('div.product_price > p.instock').getText().strip() == 'In stock' else False
        # missing category_id, upc 
        book_url       = 'http://'+host+'/'+book.select_one('div.image_container > a')['href']
        book_page      = requests.get(book_url)
        book_soup      = BeautifulSoup(book_page.content, 'html.parser')
        book_datatable = book_soup.select_one('article.product_page > table')
        book_data      = book_datatable.select('tr')
        for row in book_datatable.select('tr'):
            row_head = row.select_one('th').getText()
            row_value = row.select_one('td').getText()
            book_model_inner_data = [row_value for option in html_table_map if row_head == html_table_map[option]]

def load_config():
    import configparser
    config = configparser.ConfigParser()
    config.read('api/config.ini')
    config.sections()
    return config
    