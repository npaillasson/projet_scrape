import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

response = requests.get(url)

productInformations = "product_page_url, universal_ product_code (upc), title, price_including_tax, " \
                      "price_excluding_tax, number_available, product_description, category, review_rating, image_url\n"

if response.ok:
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup:
        print(tag)
            
    tds = soup.findAll("td")
    with open("myFile.csv", "w") as file:
        file.write(productInformations)
        for td in tds:
            td=str(td)

            file.write(str(td)+",")
