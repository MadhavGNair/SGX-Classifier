import requests
from bs4 import BeautifulSoup as bs
import json
from tqdm import tqdm


def save_data(data_json, filename='data.json'):
    with open(filename, 'w') as fl:
        json.dump(data_json, fl, indent=4)
    print(f"Data saved to {filename}")


final_json = []

for page in tqdm(range(0, 46), desc="Page Loop", unit="Iteration"):
    url = f"https://api.sgx.com/announcements/v1.1/?periodstart=20040630_160000&periodend=20240701_155959&cat=ANNC&sub=ANNC30&pagestart={page}&pagesize=250"

    payload = {}
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorizationtoken': 'token here',
        'dnt': '1',
        'origin': 'https://www.sgx.com',
        'priority': 'u=1, i',
        'referer': 'https://www.sgx.com/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }

    # make an API call for the response
    response = requests.request("GET", url, headers=headers, data=payload)

    # get the JSON formatted data
    data = response.json()

    # in case API auth token resets mid-loop, save data up until now to prevent rerunning the entire code
    if 'data' not in data:
        with open('data.json', 'w') as f:
            json.dump(final_json, f, indent=4)
        print(f"ERROR OCCURRED AT PAGE {page}. Continue from {page}.")

    # for each URL in the JSON extract the HTML of the page
    for i in tqdm(range(len(data['data'])), desc="Link Loop", leave=False):
        if data['data'][i]['title'] == "Annual Reports and Related Documents::":
            local_url = data['data'][i]['url']
            local_headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'max-age=0',
                'cookie': '_gid=GA1.2.1756413844.1719667447; _hjSessionUser_1541925=eyJpZCI6ImUwZjFhNjQyLTZjNjItNTM2NS04MzUwLTY3ZmNkMGM4ZmIwZiIsImNyZWF0ZWQiOjE3MTk2Njc0NDY3NjYsImV4aXN0aW5nIjp0cnVlfQ==; ASP.NET_SessionId=smellvsx2yrvhpyxuhjq0k3x; _ga_126SHVWK0D=GS1.1.1719758018.10.1.1719758021.0.0.0; _ga=GA1.1.2094149841.1719663700; _hjSession_1541925=eyJpZCI6IjJlNWQ5OGU2LThlMTAtNDI0OC1hOWIwLWNiNzY0M2Y3YjRlZCIsImMiOjE3MTk3NTgwMjE4OTcsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowfQ==; RT="z=1&dm=sgx.com&si=0c167c8d-b813-434e-96d0-0877acc2b6da&ss=ly1niren&sl=1&tt=5rx&bcn=%2F%2F02179919.akstat.io%2F&ld=zooa"; __eoi=ID=b9759191c34a9d7f:T=1719663704:RT=1719759985:S=AA-AfjYuNdPk_8w7GQPQSIZr8zeX',
                'dnt': '1',
                'priority': 'u=0, i',
                'referer': 'https://www.sgx.com/',
                'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-site',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
            }

            local_response = requests.request("GET", local_url, headers=local_headers, data=payload)
            local_data = local_response.text

            # use BeautifulSoup to extract the relevant information
            soup = bs(local_data, 'html.parser')

            # all relevant elements are stored within the <dd> tag
            dd_elements = soup.find_all('dd')
            # link to pdf is further enclosed in an <a> tag
            pdf_link = soup.find_all('a')
            pdf_link = 'https://links.sgx.com' + pdf_link[0].get('href')

            required_info = []

            for elem in dd_elements[0:12]:
                required_info.append(elem.text)

            required_info.append(pdf_link)

            inner_json = {'Issuer/Manager': '', 'Securities': '', 'Stapled Security': '', 'Announcement Title': '',
                          'Date & Time of Broadcast': '', 'Status': '', 'Report Type': '', 'Announcement Reference': '',
                          'Submitted By (Co./ Ind. Name)': '', 'Designation': '',
                          'Description': '',
                          'Period Ended': '', 'PDF Link': ''}

            for idx, key in enumerate(inner_json.keys()):
                inner_json[key] = required_info[idx]

            final_json.append(inner_json)


with open('data.json', 'w') as f:
    json.dump(final_json, f, indent=4)
