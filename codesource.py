#!env/bin/python3
# -*-coding:Utf-8 -*

import requests
import re
import os
from bs4 import BeautifulSoup
from math import ceil
from functions import *
import time

depart = time.time()

if not os.path.exists("results/"):  # creation of results directory if it doesn't already exist
    os.mkdir("results")

EXTRACT_NUMBER_EXPRESSION = re.compile(r"\d+")\
    # regex used to extract the number of books in one category and the number of items available

URL_INDEX_EXTRACT_EXPRESSION = re.compile(r"index.html$")\
    # regex used to create the concerned category next page's url
# when category contains more than 20 books


WRONG_SEPARATORS_DELETION_EXPRESSION = re.compile(r";")

ENCODE_ISSUES_DELETION_EXPRESSION = re.compile(r"[âÃ©]")

BASE_CATEGORY_URL = "http://books.toscrape.com/catalogue/category/books/" \
    # common part of category's links

BASE_BOOK_URL = "http://books.toscrape.com/catalogue/"

RATE_DICT = {"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"} \
    # dict to convert numbers in letter in a numeric value

HEADERS = "product_page_url; universal_ product_code (upc); title; price_including_tax; " \
          "price_excluding_tax; number_available; product_description; category;" \
          " review_rating; image_url"  # columns HEADERS

TARGET_URL = "http://books.toscrape.com/"

main_request = requests.get(TARGET_URL)

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

            with open("results/{}.csv".format(category_name), "w") as file:
                file.write(HEADERS)

                for book_page_url in books_page_url_list:

                    # data extraction from books pages

                    book_request = requests.get(book_page_url)

                    if book_request.ok:
                        book_soup = BeautifulSoup(book_request.text, "html.parser")

                        book_title = book_soup.find("h1").get_text()
                        category = book_soup.findAll("li")
                        category = str(category[2].get_text()).strip()
                        rate_and_product_description = book_soup.findAll("p")
                        rate = rate_and_product_description[2]["class"][1]
                        rate = RATE_DICT[rate]
                        product_description = str(rate_and_product_description[3].get_text())
                        product_description = WRONG_SEPARATORS_DELETION_EXPRESSION.sub(":", product_description)\
                            # replace ";" with ":" in the product description paragraph
                        product_description = ENCODE_ISSUES_DELETION_EXPRESSION.sub("", product_description)
                        img = book_soup.find("img")
                        img = img["src"].replace("../../", TARGET_URL)
                        information_table = book_soup.findAll("td")

                        info_list = [book_page_url]\
                            # list who contains all data about the book (sorted in order)

                        for information_line in information_table:  \
                                # loop who gets data from the information tab and add them in the info_list
                            information_line = str(information_line.get_text())
                            info_list.append(information_line)
                        del info_list[2]  # remove the field "Books"
                        del info_list[4]  # remove the field "tax"
                        info_list.insert(2, book_title)
                        info_list.insert(6, product_description)
                        info_list.insert(7, category)
                        info_list[8] = rate
                        info_list.append(img)

                        info_list[3], info_list[4] = info_list[3][1:], info_list[4][1:]
                        # fix the encoding issue on the price fields
                        info_list[5] = EXTRACT_NUMBER_EXPRESSION.findall(info_list[5])[0]
                        # extraction of the number of books available
                        info = ";".join(info_list)
                        # convert info_list in str using ";" as separator before writing it in cvs file

                        file.write("\n" + info)
arrive = time.time()
print(arrive-depart)