import math
from multiprocessing import Process, Manager

import pandas as pd
import requests as re
from bs4 import BeautifulSoup 

STAGING_PATH = "/home/akko/cayena-challenge/.staged.csv"

N_THREADS = 4

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
        """
        Searches the entire base site for all available books,
        returning all desired info of each book per line in a
        Pandas Dataframe, or saving it to a csv_file if csv_staged
        is set to True.
        """
        print("Scrapping all books from {} with {} threads... This might take a while.".format(self.base_url, N_THREADS))

        manager = Manager()
        book_list = manager.list()
        pool = []

        start = 1
        for i in range(N_THREADS):
            end = min(start + (self.n_pages//N_THREADS), self.n_pages)
            pool.append(Process(target=self.__scrap_worker, args=(book_list, start, end)))
            pool[i].start()
            start = end + 1

        for i in range(N_THREADS):
            pool[i].join()
        
        book_list = list(book_list)

        df = pd.DataFrame(book_list, columns=FIELD_SCHEMA)
        
        if csv_stage:
            df.to_csv(STAGING_PATH, sep=';', index=None)
        else:
            return df

    def scrape_bookpage(self, url_path):
        """
        Given the url path for a page of the base_site,
        scrapes all useful info and returns it on a list.
        """

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


    def __scrap_worker(self, list, start, end, *args):

        for page_num in range(start, end+1):
            page = re.get(self.base_url + self.pagination_path.format(page_num))
            books = BeautifulSoup(page.text, "html.parser").find_all("article", class_=BOOK_CLASS)
            for book in books:
                book_path = self.catalogue_path + book.find("h3").find("a").attrs['href']
                list.append(self.scrape_bookpage(book_path))


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

