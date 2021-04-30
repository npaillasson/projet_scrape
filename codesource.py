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

depart = time.time()

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

book_process_list = []

if main_request.ok:

    main_soup = BeautifulSoup(main_request.text, "html.parser")
    category_url_list = []
    category_url_extraction = main_soup.find("aside")
    category_url_extraction = category_url_extraction.findAll("ul")
    category_url_extraction = category_url_extraction[1]
    category_url_extraction = category_url_extraction.findAll("li")
    for category_name in category_url_extraction:
        category_url = category_name.find("a")
        category_url = category_url["href"]
        category_url = '{}{}'.format(TARGET_URL, category_url)
        category_url_list.append(category_url)

for category_url in category_url_list:

    base_link_category = URL_INDEX_EXTRACT_EXPRESSION.sub("", category_url)

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

        while page_counter != page_number:
            if page_counter == 0:
                books_page_url_list.extend(book_page_url_extractor(category_soup, BASE_BOOK_URL))
            else:
                iter_link_category = "{}/page-{}.html".format(BASE_CATEGORY_URL, (page_counter + 1))
                iter_category_request = requests.get(iter_link_category)
                iter_category_soup = BeautifulSoup(iter_category_request.text, "html.parser")
                books_page_url_list.extend(book_page_url_extractor(iter_category_soup, BASE_BOOK_URL))

            page_counter += 1

    book_process_list.append\
        (ScrapCategory(books_page_url_list, category_name, ENCODE_ISSUES_DELETION_EXPRESSION, TARGET_URL, EXTRACT_NUMBER_EXPRESSION))

for process in book_process_list:
    process.start()

for process in book_process_list:
    process.join()


arrive = time.time()
print(arrive-depart)