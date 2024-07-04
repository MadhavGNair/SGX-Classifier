import re
import pandas as pd


def remove_unmatch(data_frame):
    for i in range(len(data_frame)):
        info = data_frame['text'][i]
        company_name = data_frame['company_name'][i]
        if company_name not in info:
            # remove all instances (around 1904) where text does not match ground truth (happens when first 5 pages
            # are just tables)
            data_frame = data_frame.drop([i])
    data_frame = data_frame.reset_index(drop=True)
    return data_frame


def preprocess_company_name(data_frame):
    for i in range(len(data_frame)):
        text = data_frame['company_name'][i]
        text = re.sub(r'\s+', ' ', text)
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', '', text)
        text = text.replace("  ", " ")
        data_frame.loc[i, 'company_name'] = text

    # filter out irrelevant report types
    relevant_types = ['annual report', 'sustainability report', 'disclosure statement', 'interim report',
                      'quarterly report', 'information statement', 'summary report', 'new']
    df_filtered = data_frame[data_frame['report_type'].isin(relevant_types)]
    df_filtered = df_filtered.reset_index(drop=True)
    return df_filtered


def load_dataframe(filename):
    # import the training dataframe
    dframe = pd.read_csv(filename)
    dframe = dframe.drop(columns=['Unnamed: 0'])
    # remove index 11 because the PDF is a bunch of tables and no text
    dframe = dframe.drop([11])
    # convert year to int
    dframe['year'] = pd.to_numeric(dframe['year'], errors='coerce').astype(pd.Int64Dtype())
    dframe = dframe.reset_index(drop=True)
    # normalize company name
    dframe = preprocess_company_name(dframe)
    dframe = remove_unmatch(dframe)
    return dframe


df = load_dataframe('all_data.csv')
df.to_csv('final_data.csv')


