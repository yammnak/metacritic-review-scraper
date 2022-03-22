from distutils.util import get_platform
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Cleans reviews by getting rid of the html elements within the reviews and the leading/trailing whitespace
def clean_reviews(review):
    review = str(review)
    review = review.replace("<span class=\"blurb blurb_expanded\">", "")
    review = review.replace("<span>", "")
    review = review.replace("</span>", "")
    review = review.replace("<br/>", "")
    review = review.strip()
    return(review)

# Finds all platforms that a game is on and returns and array containing the platforms
def get_platforms(html_page):
    initial_platform = html_page.find("span", class_ = "platform")
    ip = initial_platform.find("a").string
    try:
        platforms = html_page.find("li", class_ = "product_platforms")
        platforms = platforms.find("span", class_ = "data")
        platforms = platforms.find_all("a")
        platforms.append(ip)
        i = 0
        for s in platforms:
            s = s.string
            s = s.strip()
            s = s.replace(" ","-")
            s = s.lower()
            platforms[i] = s
            i = i+1

    except AttributeError:
        ip = ip.string
        ip = ip.strip()
        platforms = [ip]
    
    return(platforms)

# Scrapes all reviews on a single html page
def single_page_html_scraper(url, data, platform):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)
    driver.get(url)
    driver.implicitly_wait(3)
    button = driver.find_elements(By.XPATH, "//span/span[contains(.,'Expand')]")

    for button in button:
        try:
            button.click()
        except Exception:
            pass

    html_page = BeautifulSoup(driver.page_source, 'html.parser')

    try:
        main_review_body = html_page.find("div", class_="body product_reviews")
        name = html_page.find("div", class_ = "product_title")
        name = str(name.find("h1").string)
        review_bodies = main_review_body.find_all("div", class_ = "review_content".split())
    except AttributeError:
        review_bodies = []

    for review in review_bodies:
        date = review.find("div", class_ = "date").string
        score = review.find("div", class_ = "metascore_w").string
        written_review = review.find("span", class_ = "blurb blurb_expanded")
        if written_review is None:
            written_review = review.find("div", class_ = "review_body").find("span")
        written_review = clean_reviews(written_review)
        total_thumbs_ups = review.find("span", class_ = "total_ups").string
        total_thumbs = review.find("span", class_ = "total_thumbs").string
        data.append([date, name, platform, score, written_review, total_thumbs_ups, total_thumbs])
    driver.quit()

# Scrapes every review for the game on every platform
def html_scraper(base_url, data, platform):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    page = requests.get(base_url, headers=headers)
    html_page = BeautifulSoup(page.text, 'html.parser')

    try:
        page_nums = int(html_page.find("li", class_ = "page last_page").find("a", class_ = "page_num").string)
    except AttributeError:
        page_nums = 0

    if page_nums != 0:
        for pages in range(0,page_nums):
            url = base_url + "?page=" + str(pages)
            single_page_html_scraper(url, data, platform)
    else:
        single_page_html_scraper(base_url, data, platform)


def all_platform_scraper():
    data = []
    base_url = input("Enter the Metacritic URL: ")
    file_name = input("Input file name: ")

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    page = requests.get(base_url, headers=headers)
    html_page = BeautifulSoup(page.text, 'html.parser')
    platforms = get_platforms(html_page)
    name = html_page.find("div", class_ = "product_title")
    name = name.find("h1").string

    for platform in platforms:
        url = "https://www.metacritic.com/game/" + str(platform).lower().strip().replace(" ", "-").replace(":", "") + "/" + str(name).lower().strip().replace(" ", "-").replace(":", "") + "/user-reviews"
        print(url)
        html_scraper(url, data, platform)

    df = pd.DataFrame(data, columns=['date', 'game', 'platform', 'metacritic_score', 'review', 'thumbs_ups', 'total_thumbs'])
    df.to_csv(file_name +  ".csv", index = False)