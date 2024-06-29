# import time
# import requests
from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# import re
#
# # enable headless mode in Selenium
# options = Options()
# options.add_argument('--headless=new')
#
# driver = webdriver.Chrome(
#     options=options,
# )
#
# # PATH = "C:/Program Files (x86)/chromedriver.exe"
# cService = webdriver.ChromeService(executable_path=PATH)
# driver = webdriver.Chrome(service=cService)
#
# driver.get('https://www.sgx.com/securities/company-announcements?ANNC=ANNC30&page=1&pagesize=100')
#
# # sleep for 5 seconds to emulate human behaviour
# time.sleep(30)
#
# announcement_urls = []
# # href_elements = driver.find_elements(By.LINK_TEXT, "Annual Reports and Related Documents::")
# href_elements = driver.find_elements(By.CLASS_NAME, "sgx-content-table-scroll-container")
#
# for url in href_elements:
#     print(url.text)
#     print('----------------------------------')
#     # announcement_urls.append(url.get_attribute("href"))
#
# # announcement_urls = [x for x in announcement_urls if re.match(r'https://links.sgx.com', x)]
#
# # print(announcement_urls)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
import time

PATH = "C:/Program Files (x86)/chromedriver.exe"

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.56 Safari/537.36"
chrome_options.add_argument(f'user-agent={userAgent}')

# Set path to chromedriver as per your configuration
webdriver_service = Service(executable_path=PATH)

# Choose Chrome Browser
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# URL of the page to scrape
url = "https://www.sgx.com/securities/company-announcements?ANNC=ANNC30&page=1&pagesize=100"

# Open the URL
driver.get(url)

# Wait for the JavaScript to load and execute
time.sleep(20)  # You may need to adjust this sleep time based on your connection speed and the site's loading time

# Find all <a> tags within the specified div
div = driver.find_element(By.CLASS_NAME, 'sgx-content-table-scroll-container')
links = div.find_elements(By.CSS_SELECTOR, 'a.website-link')

final_links = []

# Extract and print links that start with 'https://links.sgx.com'
for link in links:
    href = link.get_attribute('href')
    if href.startswith('https://links.sgx.com'):
        print(href)
        final_links.append(href)

with open('links.txt', 'w') as file:
    for item in final_links:
        file.write(f"{item}\n")

# Close the browser
driver.quit()
