import os
import pickle
from warnings import PendingDeprecationWarning
from time import sleep
from bs4 import BeautifulSoup
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# import chromedriver_autoinstaller
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules.base import Parser
import undetected_chromedriver as uc
from docx import Document

class Parser:
    def __init__(self, project_folder):
        project_path = os.path.join(os.path.abspath('projects'), project_folder)
        self.project_path = self._makedir(project_path)
        self.data_path = os.path.join(project_path, 'data')
        self._makedir(self.data_path)

    @staticmethod
    def _makedir(path):
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    @staticmethod
    def write_to_doc(data, file_path, filename):
        doc = Document()
        doc.add_paragraph(data)
        doc.save(os.path.join(file_path, f'{filename}.docx'))

class GoogleSearch(Parser):
    def __init__(self, project_folder, proxy=None, headless=True):
        super().__init__(project_folder)
        self.driver = self._set_driver(proxy, headless)

    def save_search_results(self, keywords, max_pages):
        all_text = ''
        for keyword in keywords:
            self.driver.get(f'https://www.google.com/search?q={keyword}')
            for page in range(max_pages):
                all_text += self._get_page_text()
                next_button = self.driver.find_element(By.ID, 'pnnext')
                if next_button:
                    next_button.click()
                    sleep(2)  # Adding a delay to wait for the next page to load
                else:
                    break
        self.write_to_doc(all_text, self.data_path, 'search_results')

    @staticmethod
    def _set_driver(proxy, headless):
        # Automatically download and install the correct version of ChromeDriver
        # chromedriver_autoinstaller.install()

        # Define custom user agent
        user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Chrome/125.0.6422.76 Safari/537.36"

        # Creating a ChromeOptions object for configuring Chrome browser options
        chrome_options = uc.ChromeOptions()
        # Setting headless mode based on the 'headless' parameter
        chrome_options.headless = headless
        # Adding an argument to set the browser language to English
        chrome_options.add_argument('--lang=en')

        chrome_options.add_argument(f"user-agent={user_agent}")

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--remote-debugging-port=9222') 
        chrome_options.add_experimental_option("prefs", {"credentials_enable_service": False})

        # Configuring proxy settings if a proxy is provided
        if proxy is not None:
            proxy_options = {
                'proxy': {
                    'http': proxy,
                    'https': proxy,
                    'no_proxy': 'localhost:127.0.0.1'
                }
            }
        else:
            proxy_options = None

        # Creating a Chrome driver instance with configured options and proxy settings
        driver = uc.Chrome(options=chrome_options, seleniumwire_options=proxy_options)
        sleep(2)  # Delay after creating the driver instance

        return driver

    def _get_page_text(self):
        results = self.driver.find_elements(By.CLASS_NAME, 'g')
        page_text = ''
        for result in results:
            page_text += result.text + '\n'
        return page_text
