from threading import Thread
import re
import requests
from bs4 import BeautifulSoup


class ScrapCategory(Thread):
    """Thread used to get all books data in one category and create the correspondent csv file"""

    def __init__(self, url_list, category_name, regex_encode_issue, target_url, extract_number_expression):
        """Thread initialization"""

        Thread.__init__(self)
        ScrapCategory.columns_headers = "product_page_url; universal_ product_code (upc);" \
                                        " title; price_including_tax; " \
                                        "price_excluding_tax; number_available;" \
                                        " product_description; category;" \
                                        " review_rating; image_url"  # columns HEADERS"
        ScrapCategory.rate_dict = {"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}\
            # dict to convert numbers in letter in a numeric value
        ScrapCategory.regex_separator = re.compile(r";")
        self.regex_extract_number = extract_number_expression
        self.url_list = url_list
        self.category_name = category_name
        self.regex_encode_issue = regex_encode_issue
        self.target_url = target_url

    def run(self):
        """Code to execute during thread execution"""

        with open("results/{}.csv".format(self.category_name), "w") as file:
            file.write(ScrapCategory.columns_headers)

            for book_page_url in self.url_list:

                # data extraction from books pages

                book_request = requests.get(book_page_url)

                if book_request.ok:
                    book_soup = BeautifulSoup(book_request.text, "html.parser")

                    book_title = book_soup.find("h1").get_text()
                    category = book_soup.findAll("li")
                    category = str(category[2].get_text()).strip()
                    rate_and_product_description = book_soup.findAll("p")
                    rate = rate_and_product_description[2]["class"][1]
                    rate = ScrapCategory.rate_dict[rate]
                    product_description = str(rate_and_product_description[3].get_text())
                    product_description = ScrapCategory.regex_separator.sub(":", product_description) \
                        # replace ";" with ":" in the product description paragraph
                    product_description = self.regex_encode_issue.sub("", product_description)
                    img = book_soup.find("img")
                    img = img["src"].replace("../../", self.target_url)
                    information_table = book_soup.findAll("td")

                    info_list = [book_page_url] \
                        # list which contains all data about the book (sorted in order)

                    for information_line in information_table: \
                            # loop which gets data from the information tab and adds them in the info_list
                        information_line = information_line.get_text()
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
                    info_list[5] = self.regex_extract_number.findall(info_list[5])[0]
                    # extraction of the number of books available
                    info = ";".join(info_list)
                    # convert info_list in str using ";" as separator before writing it in cvs file

                    file.write("\n" + info)
