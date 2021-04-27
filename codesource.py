import requests
import re
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

AVAILABLE_EXTRACT_EXPRESSION = re.compile(r"\d+")  \
    # regex to extract the number of books available from the primary data

HEADERS = "product_page_url; universal_ product_code (upc); title; price_including_tax; " \
          "price_excluding_tax; number_available; product_description; category; review_rating; image_url" \
    # column HEADERS

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
    tds = soup.findAll("td")

    infos_list = [url]  # list who contains all data about the book (sorted in order)

    for td in tds:  # loop who get data from the information tab and add them in the infos_list
        td = str(td.get_text())
        infos_list.append(td)
    del infos_list[2]  # remove the field "Books"
    del infos_list[4]  # remove the field "tax"
    infos_list.insert(2, book_title)
    infos_list.insert(6, product_description)
    infos_list.insert(7, category)
    infos_list[8] = rate
    infos_list.append(img)
    
    infos_list[3], infos_list[4] = infos_list[3][1:], infos_list[4][1:]  # fix the encoding issue on the price fields
    infos_list[5] = AVAILABLE_EXTRACT_EXPRESSION.findall(infos_list[5])[0]
    infos = ";".join(infos_list)  # convert infos_list in str using ";" as separator before writing it in cvs file

    with open("myFile.csv", "w") as file:
        file.write(HEADERS)
        file.write("\n" + infos)
