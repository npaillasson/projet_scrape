# projet_scrape

***

This project is entirely coded in python 3.

project realized in the framework of a training on [OpenClassrooms](https://openclassrooms.com/fr/).
This project aims to monitor the prices of an online book store (http://books.toscrape.com/). This store is fictitious and dedicated to the learning of scraping.

**the use of the script requires an internet connection**

## Table of contents
1. [General information](#general-info)
2. [Technologies](#technologies)
3. [Installation](#installation)

***

## General Info

This project works by targeting [the home page's url](http://books.toscrape.com/) of the site. 
it browses all the different categories of books and extracts the following information from the page of each book for each category:


* product_page_url
* universal_ product_code (upc)
* title
* price_including_tax
* price_excluding_tax
* number_available
* product_description
* category
* review_rating
* image_url


Finally, the script generates a .csv file containing the information retrieved for each book in a given category. All results files are named after the category to which the books belong. the results files are placed in a directory named "results". If the directory does not exist, it is automatically created by the script at the root of the project.

###what is contains on this repository?

####python files
* **codesource.py** : the main source code of the application
* **function.py** : the file who contains one function
* **thread_class.py** : the file who contains one class inheriting from 'Tread.threading'

####others
* **requierements.txt** (used to install required packages)
* **README.md** (the file you are reading now)

***

## Technologies

This project use the next packages:


* [beautifulsoup4](https://pypi.org/project/beautifulsoup4/): version 4.9.3
* [requests](https://pypi.org/project/requests/): version 2.25.1


And their dependencies:

* [certifi](https://pypi.org/project/certifi/): version 2020.12.5
* [chardet](https://pypi.org/project/chardet/): version 4.0.0
* [idna](https://pypi.org/project/idna/): version 2.10
* [soupsieve](https://pypi.org/project/soupsieve/): version 2.2.1
* [urllib3](https://pypi.org/project/urllib3/): version 1.26.4

This project also use the modules **'re'**, **'Thread'**, **'os'** and **'math'**.

###

## Installation

To get this project on your computer you can clone it:
```
$ git clone https://github.com/npaillasson/projet_scrape.git
```
To create your virtual environment you can use:
```
$python3 -m venv env
```
Then activate your new virtual environment:
```
$source env/bin/activate
```
Then install the required packages using the file 'requirements.txt':
```
$pip install requirements.txt
```

To execute the script simply use:
```
$python3 codesource.py
```
Or, alternatively:
```
$./codesource.py
```
