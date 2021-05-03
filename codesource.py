#!env/bin/python3
# -*-coding:Utf-8 -*

import requests
import re
import os
from bs4 import BeautifulSoup
from math import ceil
from url_extraction_functions import book_page_url_extractor, category_url_extractor
import time
from thread_class import ScrapCategory

start = time.time()
print("The program is running, please wait a moment !")

# regex used to extract the number of books in one category and the number of items available
EXTRACT_NUMBER_EXPRESSION = re.compile(r"\d+")

# regex used to create the concerned category next page's url
# when category contains more than 20 books
URL_INDEX_EXTRACT_EXPRESSION = re.compile(r"index.html$")

ENCODE_ISSUES_DELETION_EXPRESSION = re.compile(r"[âÃ©]")

# common part of categories' url
BASE_CATEGORY_URL = "http://books.toscrape.com/catalogue/category/books/"

# Common part of books pages' url
BASE_BOOK_URL = "http://books.toscrape.com/catalogue/"

# home page url
TARGET_URL = "http://books.toscrape.com/"

# creation of results directory if it doesn't already exist
if not os.path.exists("results/"):
    os.mkdir("results")

main_request = requests.get(TARGET_URL)

# empty list used to stock all threads before their execution (1 thread per category)
book_process_list = []

if main_request.ok:

    main_soup = BeautifulSoup(main_request.text, "html.parser")
    # empty list used to stock all categories' url
    categories_url_list = []

    categories_url_list = category_url_extractor(main_soup, TARGET_URL)

for category_url in categories_url_list:

    # a query by category to extract the url of each book contained in it
    category_request = requests.get(category_url)

    if category_request.ok:
        category_soup = BeautifulSoup(category_request.text, "html.parser")
        category_name = category_soup.find("h1").get_text()
        number_of_pages = category_soup.findAll("form")
        # extraction of the amount of books in the category (using regex)
        number_of_pages = int(EXTRACT_NUMBER_EXPRESSION.findall(number_of_pages[0].get_text())[0])
        # determination of the number of pages in the category
        number_of_pages = ceil(number_of_pages/20)
        # counter used in the while loop
        page_counter = 0
        # empty list used to stock every books pages' url contained in one category
        books_page_url_list = []

        # loop used to get all books url in one category
        # this loop browse through all the pages of the category
        while page_counter != number_of_pages:
            if page_counter == 0:
                books_page_url_list.extend(book_page_url_extractor(category_soup, BASE_BOOK_URL))
            else:
                # if the category has more than 20 books
                # we need to change the url to go to the following page
                # (replace the end of the url "index.html" by "page-<number>.html")
                iter_url_category = "{}/page-{}.html".format(BASE_CATEGORY_URL, (page_counter + 1))
                # we make a new request on this new url
                iter_category_request = requests.get(iter_url_category)
                # and we also create a new "Beautifulsoup" object
                iter_category_soup = BeautifulSoup(iter_category_request.text, "html.parser")
                # we add each url in the books_page_url_list
                books_page_url_list.extend(
                    book_page_url_extractor(iter_category_soup, BASE_BOOK_URL))

            page_counter += 1

    # instance of every "ScrapCategory" object (this class is inherited from Thread.thread)
    # we use it to create all csv files and extract all data books for each category \
    # at the same time
    book_process_list.append(ScrapCategory(books_page_url_list, category_name,
                                           ENCODE_ISSUES_DELETION_EXPRESSION, TARGET_URL,
                                           EXTRACT_NUMBER_EXPRESSION))

# we start every threads contained in book_process_list
for process in book_process_list:
    process.start()

# we stop every threads contained in book_process_list
for process in book_process_list:
    process.join()

end = time.time()
print("Thanks for waiting ! your results are in the 'results' folder \nrunning time :",
      ceil(end - start), "s")
