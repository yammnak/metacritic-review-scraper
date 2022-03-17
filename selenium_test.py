from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

url = 'https://www.metacritic.com/game/playstation-5/elden-ring/user-reviews'
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
driver.get(url)
driver.implicitly_wait(1)
expand_button = driver.find_element(By.CLASS_NAME, "toggle_expand_collapse toggle_expand")
expand_button.click()