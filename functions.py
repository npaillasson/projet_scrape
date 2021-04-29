def book_page_url_extractor(specific_soup, BASE_BOOK_URL):
    """Function who returns a list who contains all books links of the page"""
    result_list = []
    items_list = specific_soup.findAll("article")
    for item in items_list:
        link_page = item.find("a")
        link_page = str(link_page["href"])
        link_page = link_page.replace("../../../", BASE_BOOK_URL)
        result_list.append(link_page)
    return result_list