from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def html_scraper():
    data = []

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    """     url = input("Enter the Metacritic URL: ") """
    url = 'https://www.metacritic.com/game/playstation-5/elden-ring/user-reviews'
    page_request = requests.get(url, headers=headers)

    html_page = BeautifulSoup(page_request.text, 'html.parser')

    main_review_body = html_page.find("div", class_="body product_reviews")
    review_bodies = main_review_body.find_all("div", class_ = "review_content".split())

    # Find number of pages of reviews
    try:
        page_nums = int(html_page.find("li", class_ = "page last_page").find("a", class_ = "page_num").string)
    except AttributeError:
        page_nums = 0

    for review in review_bodies:
        date = review.find("div", class_ = "date").string
        score = review.find("div", class_ = "metascore_w").string
        try:
            written_review = review.find("span", class_ = "blurb blurb_expanded").string
        except AttributeError:
            written_review = review.find("span", class_ = "blurb blurb_expanded")
            if written_review is None:
                written_review = review.find("div", class_ = "review_body").find("span")
        total_thumbs_ups = review.find("span", class_ = "total_ups").string
        total_thumbs = review.find("span", class_ = "total_thumbs").string
        data.append(['elden-ring', date, score, written_review, total_thumbs_ups, total_thumbs])

    df = pd.DataFrame(data, columns=['game', 'date', 'metacritic_score', 'review', 'thumbs_ups', 'total_thumbs'])
    df.to_csv("output.csv")

    print(review_bodies[1])