from time import sleep
from selenium.webdriver.common.by import By
from modules.base import Parser
import undetected_chromedriver as uc

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
                try:
                    next_button = self.driver.find_element(By.ID, 'pnnext')
                    next_button.click()
                    sleep(2)  # Adding a delay to wait for the next page to load
                except:
                    break
        self.write_to_file(all_text, self.data_path, 'search_results', 'txt')

    def _set_driver(self, proxy, headless):
        user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Chrome/125.0.6422.76 Safari/537.36"

        chrome_options = uc.ChromeOptions()
        chrome_options.headless = headless
        chrome_options.add_argument('--lang=en')
        chrome_options.add_argument(f"user-agent={user_agent}")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--remote-debugging-port=9222') 
        chrome_options.add_experimental_option("prefs", {"credentials_enable_service": False})

        proxy_options = {
            'proxy': {
                'http': proxy,
                'https': proxy,
                'no_proxy': 'localhost:127.0.0.1'
            }
        } if proxy else None

        driver = uc.Chrome(options=chrome_options, seleniumwire_options=proxy_options)
        sleep(2)  # Delay after creating the driver instance

        return driver

    def _get_page_text(self):
        results = self.driver.find_elements(By.CLASS_NAME, 'g')
        page_text = ''
        for result in results:
            page_text += result.text + '\n'
        return page_text