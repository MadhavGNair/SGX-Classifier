import io
import re
import pandas as pd
import json
import pymupdf
import requests

file_path = 'data.json'

# open the json file containing raw data
with open(file_path, 'r') as file:
    raw_data = json.load(file)


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


faulty_links = [4671, 4673, 4674, 4675, 4678, 5988, 6244, 7666, 10370]
try:
    link = raw_data[4671]
    pdf_link = link["PDF Link"]
    pdf_text = read_pdf_from_url(pdf_link)
    # pdf_texts.append(pdf_text)
except AssertionError:
    print("PDF Link Not Found")
