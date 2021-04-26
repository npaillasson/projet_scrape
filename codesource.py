import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

productInformations = "product_page_url; universal_ product_code (upc); title; price_including_tax; " \
                      "price_excluding_tax; number_available; product_description; category; review_rating; image_url" #en-têtes des colonnes

img_link="http://books.toscrape.com/"

rate_dict={"One" : "1", "Two" : "2", "Three" : "3", "Four" : "4", "Five" : "5"} #dictionnaire qui permet de convertir la note extraite du site en chiffre

response = requests.get(url)

if response.ok:
    soup = BeautifulSoup(response.text, "html.parser")

    bookTitle = soup.find("h1")
    bookTitle = str(bookTitle.get_text())
    category = soup.findAll("li")
    category = str(category[2].get_text()).strip()
    productDescription = soup.findAll("p")
    rate = productDescription[2]["class"][1]
    rate=rate_dict[rate]
    productDescription = str(productDescription[3].get_text())
    img = soup.find("img")
    img = img["src"].replace("../../",img_link)
    tds = soup.findAll("td")

    infosList = [url] #liste qui contiendra dans l'ordre toutes les données des différentes colonnes

    for td in tds: #boucle qui permet de récupérer les données du tableau d'information du produit et de les ajouter dans infosList
        td=str(td.get_text())
        infosList.append(td)
    del infosList[2] #suppression de la donnée "Books"
    del infosList[4] #suppression de la donnée "montant de la taxe"
    infosList.insert(2,bookTitle)
    infosList.insert(6,productDescription)
    infosList.insert(7,category)
    infosList[8] = rate
    infosList.append(img)
    infosList[3], infosList[4]= infosList[3][1:], infosList[4][1:] #correction provisoire au problème d'encodage sur le prix
    infos = ";".join(infosList) #conversion d'infosList de "list" à "str" avec ";" comme séparateur avant écriture dans fichier csv

    with open("myFile.csv", "w") as file:
        file.write(productInformations)
        file.write("\n" + infos)
