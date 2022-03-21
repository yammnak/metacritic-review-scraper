from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
base_url = "https://www.metacritic.com/game/pc/psychonauts-2/user-reviews"
page = requests.get(base_url, headers=headers)
html_page = BeautifulSoup(page.text, 'html.parser')

name = html_page.find("div", class_ = "product_title")
name = name.find("h1").string
print(name)