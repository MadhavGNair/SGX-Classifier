# SGX-Classifier
 An LLM model that can classify company report PDFs from SGX. 

The files present are explained below,

Python:
- SGX_scraper.py - the API based scraper
- SGX_scraper_selenium.py - the initial selenium based scraper (incomplete)
- process_dataframe.py - for testing and modifying all_data.csv
- generate_training_data.py - Extracts relevant training data from raw data
- pdf_classifier.ipynb - the PDF classifier model

JSON:
- data.json - raw data
- training.json - the training data extracted from data.json

TXT:
- links_store.txt - copy of all 11303 links where raw data was collected from (back-up)