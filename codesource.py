#!env/bin/python3
# -*-coding:Utf-8 -*

import requests
import re
import os
from bs4 import BeautifulSoup
from math import ceil
from functions import *
import time
from thread_class import ScrapCategory

start = time.time()

if not os.path.exists("results/"):  # creation of results directory if it doesn't already exist
    os.mkdir("results")

EXTRACT_NUMBER_EXPRESSION = re.compile(r"\d+")\
    # regex used to extract the number of books in one category and the number of items available

URL_INDEX_EXTRACT_EXPRESSION = re.compile(r"index.html$")\
    # regex used to create the concerned category next page's url
# when category contains more than 20 books

ENCODE_ISSUES_DELETION_EXPRESSION = re.compile(r"[âÃ©]")

BASE_CATEGORY_URL = "http://books.toscrape.com/catalogue/category/books/" \
    # common part of category's links

BASE_BOOK_URL = "http://books.toscrape.com/catalogue/"

TARGET_URL = "http://books.toscrape.com/"

main_request = requests.get(TARGET_URL)

book_process_list = []  # empty list used to stock all threads before their execution

if main_request.ok:

    main_soup = BeautifulSoup(main_request.text, "html.parser")
    category_urls_list = list()  # empty list used to stock all categories' urls

    category_urls_list = (category_url_extractor(main_soup, TARGET_URL))

fin_etape_1 = time.time()
print("etape 1", fin_etape_1 - depart)

for category_url in category_urls_list:

    category_request = requests.get(category_url)

    if category_request.ok:
        category_soup = BeautifulSoup(category_request.text, "html.parser")
        category_name = category_soup.find("h1").get_text()
        page_number = category_soup.findAll("form")
        page_number = int(EXTRACT_NUMBER_EXPRESSION.findall(page_number[0].get_text())[0]) \
            # extraction of the amount of books in the category (using regex)
        page_number = ceil(page_number/20)  # determination of the number of pages in the category
        page_counter = 0  # counter used in the while loop
        books_page_url_list = []

        while page_counter != page_number:  # loop used to get all books url in one category
            if page_counter == 0:
                books_page_url_list.extend(book_page_url_extractor(category_soup, BASE_BOOK_URL))
            else:  # if the category has more than 20 books
                # we need to change the url to go to the following page
                iter_link_category = "{}/page-{}.html".format(BASE_CATEGORY_URL, (page_counter + 1))
                # we make a new request on this new url and we also create a new Beautifulsoup object
                iter_category_request = requests.get(iter_link_category)
                iter_category_soup = BeautifulSoup(iter_category_request.text, "html.parser")
                books_page_url_list.extend(
                    book_page_url_extractor(iter_category_soup, BASE_BOOK_URL))

            page_counter += 1

    # instance of every ScrapCategory object (this class is inherited from Thread.thread)
    # we use it to create all csv files and extract all data books for each category \
    # at the same time
    book_process_list.append(ScrapCategory(books_page_url_list, category_name,
                                           ENCODE_ISSUES_DELETION_EXPRESSION, TARGET_URL,
                                           EXTRACT_NUMBER_EXPRESSION))

for process in book_process_list:  # we start every threads contained in book_process_list
    process.start()

for process in book_process_list:  # we stop every threads contained in book_process_list
    process.join()

end = time.time()
print(end - start)
