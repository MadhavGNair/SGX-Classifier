from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import time

PATH = "C:/Program Files (x86)/chromedriver.exe"

# setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
# add a pre-defined header to mimic human user
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.56 Safari/537.36"
chrome_options.add_argument(f'user-agent={userAgent}')

# set path to chromedriver as per your configuration
webdriver_service = Service(executable_path=PATH)
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

inner_json = {'Issuer & Securities': {'Issuer/ Manager': '',
                                          'Securities': '',
                                          'Stapled Security': ''},
                  'Announcement Details': {'Announcement Title ': '',
                                           'Date &Time of Broadcast ': '',
                                           'Status ': '',
                                           'Report Type': '',
                                           'Announcement Reference': '',
                                           'Submitted By (Co./ Ind. Name)': '',
                                           'Designation': '',
                                           'Description (Please provide a detailed description of the event in the box below - Refer to the Online help for the format)': ''},
                  'Additional Details': {'Period Ended': ''}}

final_list = []

with open("links_store.txt") as file:
    for url in file:
        print(len(final_list))

        # open the URL
        driver.get(url)

        # wait for the JavaScript to load and execute
        time.sleep(3)

        # get the html of the announcement page
        page_source = driver.page_source

        # driver.quit()

        # extract required information from the html source
        soup = bs(page_source, 'html.parser')

        dd_elements = soup.find_all('dd')
        pdf_link = soup.find_all('a')
        pdf_link = 'https://links.sgx.com' + pdf_link[0].get('href')

        required_info = []

        for elem in dd_elements[0:12]:
            required_info.append(elem.text)

        required_info.append(pdf_link)
        final_list.append(required_info)


driver.quit()

with open("company_info.txt", 'w') as file:
    for item in final_list:
        file.write(f"{item}\n")


