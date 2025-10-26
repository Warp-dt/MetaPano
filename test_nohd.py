import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import requests as req
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import tempfile

from dotenv import load_dotenv
import os

load_dotenv()
HEADER_NAME = os.getenv('HEADER_NAME')
HEADER_VALUE = os.getenv('HEADER_VALUE')

user_data_dir = tempfile.mkdtemp(prefix="selenium_chrome_3")
options = Options()
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
# options.add_argument("--headless=new")
service = Service("/usr/bin/chromedriver")  # ou /usr/local/bin/chromedriver
driver = webdriver.Chrome(service=service, options=options)

url="https://www.dofusbook.net/api/stuffs/dofus/public/9797636"


if __name__ == "__main__":
    # driver.get("https://ifconfig.me")
    # print(driver.page_source)
    driver.get(url)
    try:
        pre_text = driver.find_element("tag name", "pre").text
        data = json.loads(pre_text)
        print(data)
    except Exception as e:
        print(e)
        print(driver.page_source)
