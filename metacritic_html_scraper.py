from bs4 import BeautifulSoup
import requests

def html_scraper():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    url = input("Enter the Metacritic URL: ")
    page = requests.get(url, headers=headers)

    test = BeautifulSoup(page.text, 'html.parser')

    tag = test.find("div", class_="body product_reviews")
    asdf = tag.find_all("div", class_ = "review_content".split())

# Find number of pages of reviews
    try:
        page_nums = int(test.find("li", class_ = "page last_page").find("a", class_ = "page_num").string)
    except AttributeError:
        page_nums = 0

    p = 0

    for i in range(1,len(asdf)):
        p = p+1

    print(p)