import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://www.sgx.com/securities/company-announcements?ANNC=ANNC30&page=1&pagesize=100"

# Headers to mimic a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.sgx.com',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}

# Create a session
session = requests.Session()

# Send a GET request to the page
response = session.get(url, headers=headers)

print(response.text)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <a> tags within the specified div
    div = soup.find('div', class_='sgx-content-table-scroll-container')
    if div:
        links = div.find_all('a', href=True, class_='website-link')

        # Extract and print links that start with 'https://links.sgx.com'
        for link in links:
            href = link['href']
            if href.startswith('https://links.sgx.com'):
                print(href)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
