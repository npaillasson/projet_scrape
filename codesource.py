import requests
import re
from bs4 import BeautifulSoup

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

if response.ok:
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
    info = ";".join(info_list)
    # convert info_list in str using ";" as separator before writing it in cvs file

    with open("myFile.csv", "w") as file:
        file.write(HEADERS)
        file.write("\n" + info)
