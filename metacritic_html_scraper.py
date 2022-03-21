from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def single_page_html_scraper(url, data):
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
    driver.get(url)
    driver.implicitly_wait(1)
    button = driver.find_elements(By.XPATH, "//span/span[contains(.,'Expand')]")

    for button in button:
        button.click()

    html_page = BeautifulSoup(driver.page_source, 'html.parser')

    main_review_body = html_page.find("div", class_="body product_reviews")
    name = html_page.find("div", class_ = "product_title")
    name = str(name.find("h1").string)
    review_bodies = main_review_body.find_all("div", class_ = "review_content".split())

    for review in review_bodies:
        date = review.find("div", class_ = "date").string
        score = review.find("div", class_ = "metascore_w").string
        written_review = review.find("span", class_ = "blurb blurb_expanded")
        if written_review is None:
            written_review = review.find("div", class_ = "review_body").find("span")
        total_thumbs_ups = review.find("span", class_ = "total_ups").string
        total_thumbs = review.find("span", class_ = "total_thumbs").string
        data.append([name, date, score, written_review, total_thumbs_ups, total_thumbs])
    driver.quit()

def html_scraper():
    data = []

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    base_url = input("Enter the Metacritic URL: ")
    file_name = input("Input file name: ")
    page = requests.get(base_url, headers=headers)
    html_page = BeautifulSoup(page.text, 'html.parser')

    try:
        page_nums = int(html_page.find("li", class_ = "page last_page").find("a", class_ = "page_num").string)
    except AttributeError:
        page_nums = 0

    if page_nums != 0:
        for pages in range(0,page_nums):
            url = base_url + "?page=" + str(pages)
            single_page_html_scraper(url, data)
    else:
        single_page_html_scraper(base_url, data)

    df = pd.DataFrame(data, columns=['game', 'date', 'metacritic_score', 'review', 'thumbs_ups', 'total_thumbs'])
    df.to_csv(file_name +  ".csv")