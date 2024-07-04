import io
import json
import re
import pandas as pd
import requests
import pymupdf
from tqdm import tqdm

# STEP 1: Extract relevant labels from raw data
file_path = 'data.json'

# open the json file containing raw data
with open(file_path, 'r') as file:
    raw_data = json.load(file)

company_names = []
years = []
report_types = []
headquarters = []
relevant_keys = ['Issuer/Manager', 'Report Type', 'Period Ended']

# for each element of raw data, extract only the required labels
for data in raw_data:
    # extract company name
    company_names.append(data[relevant_keys[0]].lower())
    # extract year
    year = data[relevant_keys[2]][-4:]
    years.append(year if year.isdigit() else None)
    # extract report type
    report_types.append(data[relevant_keys[1]].lower())
    # extract headquarter information
    headquarters.append("singapore")


# STEP 2: Extract all PDF text and convert to string of data
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


pdf_texts = []

for link in tqdm(raw_data):
    try:
        pdf_link = link["PDF Link"]
        pdf_text = read_pdf_from_url(pdf_link)
        pdf_texts.append(pdf_text)
    except AssertionError:
        pdf_texts.append(None)
        print(f"{link['PDF Link']} did not work.")
    except Exception:
        print(f"Code stopped at {link['PDF Link']}.")
        pdf_texts.append(None)
        with open('backup.txt', 'w') as f:
            for line in pdf_texts:
                f.write(f"{line}\n")

with open('backup.txt', 'w') as f:
    for line in pdf_texts:
        f.write(f"{line}\n")

# some links have spaces in the URL leading to them not opening properly
faulty_links = [5988, 7666, 10370]

with open('backup.txt') as f:
    lines = f.readlines()

# remove faulty indices from labels
for f_link in faulty_links:
    company_names.pop(f_link)
    years.pop(f_link)
    report_types.pop(f_link)
    headquarters.pop(f_link)

print(len(company_names))
print(len(years))
print(len(report_types))

# STEP 3: Convert all above data into Pandas Dataframe
df = pd.DataFrame({
    'text': lines,
    'company_name': company_names,
    'year': years,
    'report_type': report_types,
    'headquarter': headquarters
})

# write the dataframe to json
df.to_csv('all_data.csv')


