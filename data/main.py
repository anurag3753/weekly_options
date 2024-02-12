# main.py

import sys
from web_scraping import scrape_nse_data
from data_processing import DataProcessor


# Convert sys.argv into a dictionary-like object
argv_dict = dict(enumerate(sys.argv))


# Define constants
symbol = argv_dict.get(1, "NIFTY")  # Get the value of the first argument
url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
webdriver_path = "C:\\Users\\Hp\\Downloads\\Compressed\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
download_directory = "D:\\trading\\weekly_options\\data"
output_file = f"D:\\trading\\weekly_options\\data\\output_{symbol.lower()}.json"
csv_file_path = f"output_{symbol.lower()}.csv"

# Scrape data from NSE website and save to JSON file
scrape_nse_data(url, webdriver_path, download_directory, output_file)

# Process JSON data and write relevant information to CSV file
processor = DataProcessor(output_file)
processor.process_json_data()
processor.calculate_pcr()
processor.determine_option_signal()
processor.write_to_csv(csv_file_path)
