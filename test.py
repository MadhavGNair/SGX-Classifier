import io
import re
import pandas as pd
import json
import pymupdf
import requests
from collections import Counter

file_path = 'data.json'

# open the json file containing raw data
with open(file_path, 'r') as file:
    raw_data = json.load(file)


def count_report_types(data):
    # Extract all 'Report Type' values
    report_types = [item['Report Type'] for item in data if 'Report Type' in item]

    # Count the frequency of each report type
    report_type_counts = Counter(report_types)

    return report_type_counts


def read_pdf_from_url(pdf_url):
    response = requests.get(pdf_url)
    with pymupdf.open(stream=io.BytesIO(response.content), filetype="pdf") as doc:
        text = ""
        for page_num in range(min(5, len(doc))):
            page = doc[page_num]
            text += page.get_text()
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = [line for line in text.split('\n') if line != ' ']
    text = preprocess_text(" ".join(text))
    return text


def preprocess_text(text):
    # remove excess whitespace
    text = re.sub(r'\s+', ' ', text)
    # normalize case
    text = text.lower()
    # remove special characters (modify as needed)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = text.replace("  ", " ")
    return text.strip()


# faulty_links = [4671, 4673, 4674, 4675, 4678, 5988, 6244, 7666, 10370]
# try:
#     link = raw_data[4671]
#     pdf_link = link["PDF Link"]
#     pdf_text = read_pdf_from_url(pdf_link)
#     # pdf_texts.append(pdf_text)
# except AssertionError:
#     print("PDF Link Not Found")

# counts = {'Annual Report': 7317, 'Sustainability Report': 2153, 'Disclosure Statement': 405, 'Interim Report': 286,
#           'Quarterly Report': 74, 'Information Statement': 45, 'Summary Report': 23, 'New': 20}
#
# keys = list(counts.keys())
# print([key.lower() for key in keys])

# counts = count_report_types(raw_data)
# print(counts)
#
for item in raw_data:
    if item['Report Type'] == 'SG150409OTHROIM5':
        print(item)

