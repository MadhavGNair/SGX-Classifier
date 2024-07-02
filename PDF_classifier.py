import io
import json
import re
import pymupdf
import requests
import pandas as pd

# import the training dataframe
df = pd.read_csv('training_data.csv')
df = df.drop(columns=['Unnamed: 0'])
df['year'] = pd.to_numeric(df['year'], errors='coerce').astype(pd.Int64Dtype())

faulty_links = [5988, 7666, 10370]
for f_link in faulty_links:
    print(df.loc[[f_link]])


