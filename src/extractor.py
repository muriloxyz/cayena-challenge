import math

import pandas as pd
import requests as re
from bs4 import BeautifulSoup 

STAGING_PATH = "/home/akko/cayena-challenge/.staged.csv"

BASE_URL = "https://books.toscrape.com/"
CATALOGUE_PATH = "catalogue/" 
PAGINATION_PATH = "catalogue/page-{}.html"
BOOK_CLASS = "product_pod"

FIELD_SCHEMA = [
    'title',
    'rating',
    'category',
    'upc',
    'product_type',
    'price_notax',
    'price_tax',
    'tax_value',
    'n_available',
    'n_reviews'
]

class Extractor():

    def __init__(self, base_url=BASE_URL, catalogue_path=CATALOGUE_PATH, pagination_path=PAGINATION_PATH):
        self.base_url = base_url
        self.catalogue_path = catalogue_path
        self.pagination_path = pagination_path
        self.__set_metainfo()

    def scrape_books(self, csv_stage=True):
        book_list = []

        for page_num in range(1, self.n_pages + 1):
            page = re.get(self.base_url + self.pagination_path.format(page_num))
            books = BeautifulSoup(page.text, "html.parser").find_all("article", class_=BOOK_CLASS)
            for book in books:
                book_path = self.catalogue_path + book.find("h3").find("a").attrs['href']
                book_list.append(self.scrape_bookpage(book_path))
    
        df = pd.DataFrame(book_list, columns=FIELD_SCHEMA)
        
        if csv_stage:
            df.to_csv(STAGING_PATH)
        else:
            return df

    def scrape_bookpage(self, url_path):
        page = re.get(self.base_url + url_path)
        soup = BeautifulSoup(page.content, "html.parser")
        category = soup.find_all("li")[2].text # 3rd one is the category
        title = soup.find("h1").text
        rating = soup.find("p", class_="star-rating").attrs['class'][1]
        td_results = list(map(lambda x: x.text, soup.find_all("td")))
        return (
            title,              # Book title
            rating,             # Star rating
            category,           # Book category
            td_results[0],      # UPC
            td_results[1],      # Product type
            td_results[2],      # Price (no tax)
            td_results[3],      # Price (w/ tax)
            td_results[4],      # Tax
            td_results[5],      # Availability
            td_results[6],      # Number os reviews
        )  

    def __set_metainfo(self):
        soup = self.__get_page(self.pagination_path.format("1"))
        results = soup.find_all("strong")
        self.page_size = int(results[2].text) - int(results[1].text) + 1
        self.n_elems = int(results[0].text)
        self.n_pages = math.ceil(self.n_elems / self.page_size)

    def __get_page(self, url_path):
        url = self.base_url + url_path
        page = re.get(url)
        return BeautifulSoup(page.content, "html.parser")

