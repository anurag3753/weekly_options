# web_scraping.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_nse_data(url, webdriver_path, download_directory, output_file):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': download_directory,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True
    })

    service = Service(executable_path=webdriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'pre'))
        )
        json_data = element.text

        with open(output_file, 'w') as f:
            f.write(json_data)
        print(f"JSON data saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    driver.quit()
