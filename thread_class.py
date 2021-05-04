from threading import Thread
import re
import requests
import urllib.request
import os
from bs4 import BeautifulSoup


class ScrapCategory(Thread):
    """Thread used to get all books data in one category and create the correspondent csv file"""

    def __init__(self, url_list, category_name,
                 regex_encode_issue, target_url,
                 extract_number_expression):
        """Thread initialization"""

        Thread.__init__(self)
        # columns HEADERS"
        ScrapCategory.columns_headers = "product_page_url; universal_ product_code (upc);" \
                                        " title; price_including_tax; " \
                                        "price_excluding_tax; number_available;" \
                                        " product_description; category;" \
                                        " review_rating; image_url"
        # dict to convert numbers in letter in a numeric value
        ScrapCategory.rate_dict = {"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}
        ScrapCategory.regex_separator = re.compile(r";")
        ScrapCategory.regex_title_correction = re.compile(r"[/;]")
        self.regex_extract_number = extract_number_expression
        self.url_list = url_list
        self.category_name = category_name
        self.regex_encode_issue = regex_encode_issue
        self.target_url = target_url

    def run(self):
        """Code to execute during thread execution"""

        # creation of directory named after the category name if it doesn't already exist
        if not os.path.exists("results/{}/".format(self.category_name)):
            os.mkdir("results/{}".format(self.category_name))

        # creation of books_img directory if it doesn't already exist
        if not os.path.exists("results/{}/books_img/".format(self.category_name)):
            os.mkdir("results/{}/books_img".format(self.category_name))

        with open("results/{}/{}.csv".format(self.category_name, self.category_name), "w") as file:
            file.write(ScrapCategory.columns_headers)

            for book_page_url in self.url_list:

                # data extraction from books pages

                book_request = requests.get(book_page_url)

                if book_request.ok:
                    book_soup = BeautifulSoup(book_request.text, "html.parser")

                    book_title = book_soup.find("h1").get_text()
                    book_title = ScrapCategory.regex_title_correction.sub("_", book_title)
                    # We fix encode issues in the book title
                    book_title = self.regex_encode_issue.sub("", book_title)
                    rate_and_product_description = book_soup.findAll("p")
                    rate = rate_and_product_description[2]["class"][1]
                    rate = ScrapCategory.rate_dict[rate]
                    product_description = str(rate_and_product_description[3].get_text())
                    # replace ";" with ":" in the product description paragraph
                    product_description = ScrapCategory.regex_separator.sub(":", product_description)
                    # We fix all encode issues in the product description
                    product_description = self.regex_encode_issue.sub("", product_description)
                    img = book_soup.find("img")
                    img = img["src"].replace("../../", self.target_url)
                    information_table = book_soup.findAll("td")

                    # list which contains all data about the book (sorted in order)
                    info_list = [book_page_url]

                    # loop which gets data from the information tab and adds them in the info_list
                    for information_line in information_table:
                        information_line = information_line.get_text()
                        info_list.append(information_line)
                    # remove the field "Books"
                    del info_list[2]
                    # remove the field "tax"
                    del info_list[4]
                    info_list.insert(2, book_title)
                    info_list.insert(6, product_description)
                    info_list.insert(7, self.category_name)
                    info_list[8] = rate
                    info_list.append(img)

                    # fix the encoding issues on the price fields
                    info_list[3], info_list[4] = info_list[3][1:], info_list[4][1:]
                    # extraction of the number of books available
                    info_list[5] = self.regex_extract_number.findall(info_list[5])[0]
                    # convert info_list in str using ";" as separator before writing it in cvs file
                    info = ";".join(info_list)

                    file.write("\n" + info)

                    urllib.request.urlretrieve(img, "results/{}/books_img/{}.png".format(
                        self.category_name, book_title))
