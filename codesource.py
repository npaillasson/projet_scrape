import requests
import re
from bs4 import BeautifulSoup
from math import ceil

def page_url_extractor(specific_soup):
    result_list = []
    items_list = specific_soup.findAll("article")
    for item in items_list:
        link_page = item.find("a")
        link_page = str(link_page["href"])
        link_page = link_page.replace("../../../", BASE_BOOK_URL)
        result_list.append(link_page)
    return result_list

#working_url = "http://books.toscrape.com/catalogue/category/books/childrens_11/index.html"
working_url = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"

BASE_SECTION_URL = "http://books.toscrape.com/catalogue/category/books/" \
    # common part of section's links

RESULTS_NUMBER_EXTRACT_EXPRESSION = re.compile(r"\d+")

LINK_INDEX_EXTRACT_EXPRESSION = re.compile(r"index.html$")

BASE_BOOK_URL = "http://books.toscrape.com/catalogue/"

base_link_category = LINK_INDEX_EXTRACT_EXPRESSION.sub("", working_url)

section_requests = requests.get(working_url)


if section_requests.ok:

    section_soup = BeautifulSoup(section_requests.text, "html.parser")
    book_links = section_soup.findAll("h3")
    page_number = section_soup.findAll("form")
    page_number = int(RESULTS_NUMBER_EXTRACT_EXPRESSION.findall(page_number[0].get_text())[0]) \
        # extraction of number of books in the section (using regex)
    page_number = ceil(page_number/20)  # number of section's pages determination
    page_counter = 0  # for the while loop
    books_page_url_list = []

    while page_counter != page_number:
        if page_counter == 0:
            books_page_url_list.extend(page_url_extractor(section_soup))
        else:
            iter_link_category = "{}page-{}{}".format(base_link_category, (page_counter + 1),".html")
            iter_requests_category = requests.get(iter_link_category)
            iter_soup_category = BeautifulSoup(iter_requests_category.text, "html.parser")
            books_page_url_list.extend(page_url_extractor(iter_soup_category))

        page_counter += 1
    print(books_page_url_list)

        # list who contains all urls of different pages of the section
    #link_book_page_list = []  # list who contains section's books pages links

    #while page_counter =! page_number:
        #if page_counter == 0:
            #link_end = "index"
        #else:
            #link_end = f"page-{}".format(page_counter)

        #for book_link in book_links:





#collection of datas on book page

url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

AVAILABLE_EXTRACT_EXPRESSION = re.compile(r"\d+")  \
    # regex to extract the number of books available from the primary data

HEADERS = "product_page_url; universal_ product_code (upc); title; price_including_tax; " \
          "price_excluding_tax; number_available; product_description; category;" \
          " review_rating; image_url"  # column HEADERS

IMG_LINK = "http://books.toscrape.com/"

RATE_DICT = {"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"} \
    # dict to convert numbers in letter in a numeric value

response = requests.get(url)

if not response.ok:
    soup = BeautifulSoup(response.text, "html.parser")

    book_title = soup.find("h1")
    book_title = str(book_title.get_text())
    category = soup.findAll("li")
    category = str(category[2].get_text()).strip()
    product_description = soup.findAll("p")
    rate = product_description[2]["class"][1]
    rate = RATE_DICT[rate]
    product_description = str(product_description[3].get_text())
    img = soup.find("img")
    img = img["src"].replace("../../", IMG_LINK)
    information_table = soup.findAll("td")

    info_list = [url]  # list who contains all data about the book (sorted in order)

    for information_line in information_table:  \
            # loop who get data from the information tab and add them in the info_list
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
    info_list[5] = AVAILABLE_EXTRACT_EXPRESSION.findall(info_list[5])[0]
    # extraction of the number of books available
    info = ";".join(info_list)
    # convert info_list in str using ";" as separator before writing it in cvs file

    with open("myFile.csv", "w") as file:
        file.write(HEADERS)
        file.write("\n" + info)
