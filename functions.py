def book_page_url_extractor(specific_soup, base_url):
    """Function which returns a list which contains all books url of the category page"""

    result_list = []
    items_list = specific_soup.findAll("article")
    for item in items_list:
        link_page = item.find("a")
        link_page = str(link_page["href"])
        link_page = link_page.replace("../../../", base_url)
        result_list.append(link_page)
    return result_list

def category_url_extractor(specific_soup, base_url):
    """Function which returns a list which contains all categories url"""

    result_category_list =[]
    category_list = specific_soup.find("aside")  # categories url extraction from home page
    category_list = category_list.findAll("ul")
    category_list = category_list[1]
    category_list = category_list.findAll("li")  # keep just the categories url
    # loop to extract all categories url and add them in category_urls_list
    for category_name in category_list:
        category_url = category_name.find("a")
        category_url = category_url["href"]
        category_url = '{}{}'.format(base_url, category_url)  # creation of categories' url
        result_category_list.append(category_url)
    return result_category_list
