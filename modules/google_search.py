import os
import logging
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from modules.base import Parser

class GoogleSearch(Parser):
    URL = 'https://www.google.com/'

    def __init__(self, project_folder, proxy=None, headless=False):
        super().__init__(project_folder)
        self.driver = self._set_driver(proxy, headless)
        sleep(2)

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
        
    def _wait_for_element_located(self, by, value, timeout=15):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            sleep(1)
            return element
        except Exception as e:
            logging.error(f"Element not found: {by}={value}, error: {e}")
            raise

    def extract_search_pages(self, keywords, max_pages):
        try:
            for keyword in keywords:
                self.driver.get(self.URL)
                search_box = self._wait_for_element_located(By.NAME, 'q')
                search_box.send_keys(keyword)
                search_box.send_keys(Keys.RETURN)

                page_text = []
                for page in range(max_pages):
                    sleep(2)
                    page_content = self.driver.page_source
                    soup = BeautifulSoup(page_content, 'html.parser')
                    results = soup.find_all('div', class_='g')
                    for result in results:
                        page_text.append(result.get_text(separator=' ', strip=True))

                    next_button = self.driver.find_elements(By.ID, 'pnnext')
                    if next_button:
                        next_button[0].click()
                    else:
                        break

                self.write_to_doc("\n\n".join(page_text), self.data_path, f'{keyword}_results')

        except Exception as e:
            logging.error(f"An error occurred while extracting search pages: {e}")
            raise
        finally:
            self.driver.quit()