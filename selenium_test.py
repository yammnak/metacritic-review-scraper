from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

url = 'https://www.metacritic.com/game/playstation-5/elden-ring/user-reviews'
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
driver.get(url)
driver.implicitly_wait(5)
button = driver.find_elements(By.XPATH, "//span/span[contains(.,'Expand')]")

for button in button:
    button.click()

html_page = BeautifulSoup(driver.page_source, 'html.parser')

main_review_body = html_page.find("div", class_="body product_reviews")
review_bodies = main_review_body.find_all("div", class_ = "review_content".split())

print(review_bodies[1])