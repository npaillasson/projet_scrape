def book_page_url_extractor(specific_soup, base_url):
    """Function which returns a list which contains all books url of the category page"""

    result_list = []
    items_list = specific_soup.findAll("article")
    for item in items_list:
        page_url = item.find("a")
        page_url = str(page_url["href"])
        page_url = page_url.replace("../../../", base_url)
        result_list.append(page_url)
    return result_list


def category_url_extractor(specific_soup, base_url):
    """Function which returns a list which contains all categories url"""

    result_list = []
    # categories url extraction from home page
    categories_list = specific_soup.find("aside")
    categories_list = categories_list.findAll("ul")
    categories_list = categories_list[1]
    # keep just the categories url
    categories_list = categories_list.findAll("li")
    # loop to extract all categories url and add them in result_list
    for category_name in categories_list:
        category_url = category_name.find("a")
        category_url = category_url["href"]
        # creation of categories' url
        category_url = base_url + category_url
        result_list.append(category_url)
    return result_list
