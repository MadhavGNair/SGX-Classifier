from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import time

PATH = "C:/Program Files (x86)/chromedriver.exe"


class SGXScraper:
    def __init__(self, driver_path=PATH):
        self.chrome_options = Options()
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")  # Ensure GUI is off
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        # add a pre-defined header to mimic human user
        userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.56 Safari/537.36"
        self.chrome_options.add_argument(f'user-agent={userAgent}')
        webdriver_service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=webdriver_service, options=self.chrome_options)
        self.final_links = []
        self.company_info = []

    def scrape_announcement_links(self):
        for page in range(1, 115):
            print(page)
            # URL of the page to scrape
            url = f"https://www.sgx.com/securities/company-announcements?ANNC=ANNC30&page={page}&pagesize=100"

            # open the URL
            self.driver.get(url)

            # wait for the JavaScript to load and execute
            time.sleep(20)

            # find all <a> tags within the specified div
            div = self.driver.find_element(By.CLASS_NAME, 'sgx-content-table-scroll-container')
            links = div.find_elements(By.CSS_SELECTOR, 'a.website-link')

            # extract and print links that start with 'https://links.sgx.com'
            for link in links:
                href = link.get_attribute('href')
                if href.startswith('https://links.sgx.com'):
                    self.final_links.append(href)
        self.scrape_company_details()
        self.driver.quit()

    def scrape_company_details(self):
        for idx, url in enumerate(self.final_links):
            print('link no.: ', idx)
            # open the URL
            self.driver.get(url)

            # wait for the JavaScript to load and execute
            time.sleep(20)

            # get the html of the announcement page
            page_source = self.driver.page_source

            self.driver.quit()

            # extract required information from the html source
            soup = bs(page_source, 'html.parser')

            dd_elements = soup.find_all('dd')
            pdf_link = soup.find_all('a')
            pdf_link = 'https://links.sgx.com' + pdf_link[0].get('href')

            required_info = []

            for elem in dd_elements[0:12]:
                required_info.append(elem.text)

            required_info.append(pdf_link)
            self.company_info.append(required_info)
        self.write_list_to_file('company_info.txt', scraper.company_info)

    def write_list_to_file(self, file_name, list_to_write):
        with open(file_name, 'w') as file:
            for item in list_to_write:
                file.write(f"{item}\n")


scraper = SGXScraper(PATH)
scraper.scrape_announcement_links()

# # set path to chromedriver as per your configuration
# webdriver_service = Service(executable_path=PATH)
# driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
#
# final_links = []
# for page in range(1, 115):
#     # URL of the page to scrape
#     url = f"https://www.sgx.com/securities/company-announcements?ANNC=ANNC30&page={page}&pagesize=100"
#
#     # open the URL
#     driver.get(url)
#
#     # wait for the JavaScript to load and execute
#     time.sleep(20)
#
#     # find all <a> tags within the specified div
#     div = driver.find_element(By.CLASS_NAME, 'sgx-content-table-scroll-container')
#     links = div.find_elements(By.CSS_SELECTOR, 'a.website-link')
#
#     # extract and print links that start with 'https://links.sgx.com'
#     for link in links:
#         href = link.get_attribute('href')
#         if href.startswith('https://links.sgx.com'):
#             final_links.append(href)
#
# with open('links.txt', 'w') as file:
#     for item in final_links:
#         file.write(f"{item}\n")
#
#     # Close the browser
#     driver.quit()
