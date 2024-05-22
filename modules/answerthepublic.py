import os
import pickle
from time import sleep
from bs4 import BeautifulSoup
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules.base import Parser
import undetected_chromedriver as uc

class Answer(Parser):
    URL = 'https://answerthepublic.com/'
    LOGIN_URL = 'https://answerthepublic.com/users/sign_in'

    def __init__(self, project_folder, email, password, proxy=None, headless=False):
        super().__init__(project_folder)
        self.email = email
        self.password = password
        self.cookies_file_path = os.path.join(self.cookies_path, f'answer_{self.email}.pkl')
        self.driver = self._set_driver(proxy, headless)
        sleep(2)  # Delay after initializing the driver

    @staticmethod
    def __cookies_file_exists(cookies_filename):
        return os.path.exists(cookies_filename)

    @staticmethod
    def _set_driver(proxy, headless):
        # Automatically download and install the correct version of ChromeDriver
        chromedriver_autoinstaller.install()

        # Creating a ChromeOptions object for configuring Chrome browser options
        chrome_options = uc.ChromeOptions()
        # Setting headless mode based on the 'headless' parameter
        chrome_options.headless = headless
        # Adding an argument to set the browser language to English
        chrome_options.add_argument('--lang=en')
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
            sleep(1)  # Delay after element is located
            return element
        except TimeoutException:
            raise NoSuchElementException(f"Element not found: {by}={value}")

    def _wait_for_element_clickable(self, by, value, timeout=15):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            sleep(1)  # Delay after element is clickable
            return element
        except TimeoutException:
            raise NoSuchElementException(f"Element not found: {by}={value}")

    def _wait_for_element_invisible(self, by, value, timeout=15):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element((by, value))
            )
            sleep(1)  # Delay after element becomes invisible
        except TimeoutException:
            print("Element did not disappear within the specified timeout")

    def __handle_modal_popup(self):
        try:
            dismiss_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-multiple-session-modal-target='btnSubmit']"))
            )
            dismiss_button.click()
            sleep(1)  # Delay after clicking the dismiss button
            print("Dismissed the popup.")
        except TimeoutException:
            print("No dismiss button found or it didn't appear within 10 seconds.")
    
    def __set_source(self, mode):
        # Find the search labels container element using its class name "search__labels"
        search_labels_div = self.driver.find_element(By.CLASS_NAME, "search__labels")

        # Initialize the 'element' variable to None before the condition
        element = None

        # Check the value of 'mode' to determine the source (YouTube or Bing)
        if mode == 'youtube':
            # If mode is 'youtube', find the corresponding label element for YouTube
            element = search_labels_div.find_element(By.CSS_SELECTOR, '[for="provider_youtube"]')
        elif mode == 'bing':
            # If mode is 'bing', find the corresponding label element for Bing
            element = search_labels_div.find_element(By.CSS_SELECTOR, '[for="provider_bing"]')

        # Check if 'element' was initialized before attempting to click
        if element is not None:
            # Click the found element
            element.click()
            sleep(1)  # Delay after setting the source
        else:
            # Handle the situation when the element was not found
            print(f"Element for mode '{mode}' not found.")

    def __set_country(self, country):
        # Locate the dropdown element by its ID ("region").
        dropdown = Select(self.driver.find_element(By.ID, "region"))

        # Select the option in the dropdown with the visible text matching the provided country name.
        # The .title() method is used to capitalize the first letter of each word in the country name.
        dropdown.select_by_visible_text(country.title())
        sleep(1)  # Delay after setting the country

    def __set_language(self, lang):
        # Locate the dropdown element by its ID ("lang").
        dropdown = Select(self.driver.find_element(By.ID, "lang"))

        # Select the option in the dropdown with the visible text matching the provided language.
        # The .title() method is used to capitalize the first letter of each word in the language name.
        dropdown.select_by_visible_text(lang.title())
        sleep(1)  # Delay after setting the language

    def __input_keyword(self, key):
        # Locate the input element by its ID ("report_keyword").
        element = self.driver.find_element(By.ID, "report_keyword")

        # Input the provided keyword into the found input element.
        element.send_keys(key)
        sleep(5)  # Delay after inputting the keyword

    def __click_search_button(self):
        # Locate the search button element by its class name ("search__submit").
        element = self._wait_for_element_clickable(By.CLASS_NAME, "search__submit")
        
        # Simulate a click on the found search button element.
        element.click()
        sleep(1)  # Delay after clicking the search button

    def login(self):
        # Check if cookies file exists
        if (False): # self.__cookies_file_exists(self.cookies_file_path):
            print('Cookies found. Logging into the account...')

            # Load cookies from the existing file
            with open(self.cookies_file_path, "rb") as cookies_file:
                cookies = pickle.load(cookies_file)

            # Navigate to the login URL and add cookies to the current session
            self.driver.get(self.LOGIN_URL)
            for cookie in cookies:
                self.driver.add_cookie(cookie)

            # Refresh the page after adding cookies
            self.driver.get(self.LOGIN_URL)
            sleep(2)  # Delay after logging in with cookies
        else:
            try:
                # Navigate to the login URL
                self.driver.get(self.LOGIN_URL)
                sleep(2)  # Delay after navigating to login URL

                # Find and fill in the email input field
                input_email = self._wait_for_element_located(By.ID, 'user_email')
                input_email.send_keys(self.email)
                sleep(1)  # Delay after inputting email

                # Find and fill in the password input field
                input_password = self._wait_for_element_located(By.ID, 'user_password')
                input_password.send_keys(self.password)
                sleep(1)  # Delay after inputting password

                # Find and click the login button
                login_button = self.driver.find_element(By.CLASS_NAME, 'btn-login')
                login_button.click()
                sleep(1)  # Delay after clicking the login button

                # Wait for the login button to become invisible (indicating successful login)
                self._wait_for_element_invisible(By.CLASS_NAME, 'btn-login')

                # Get the current session cookies and save them to a file
            #    cookies = self.driver.get_cookies()
             #   with open(self.cookies_file_path, "wb") as cookies_file:
                    # pickle.dump(cookies, cookies_file)
                
            except Exception as e:
                # Raise an exception in case of a login error
                raise Exception("Login error: \n", e)

        

    @staticmethod
    def __parse_keywords(mode, soup):
        # Find the section tag corresponding to the specified mode (e.g., 'questions')
        section_tag = soup.find('section', {'data-source-name': mode})

        # Find all unordered lists with class 'modifier-list' within the section
        ul_lists = section_tag.find_all('ul', class_='modifier-list')

        # Initialize an empty list to store the extracted text
        text_list = []

        # Iterate over each unordered list
        for ul_list in ul_lists:
            # Find all div tags with class 'modifier-suggestion' within the list
            divs = ul_list.find_all('div', class_='modifier-suggestion')

            # Extract text from each div and add it to the text_list
            text_list.extend([div.get_text(strip=True) for div in divs])

        # Return the list of extracted text for the specified keyword type (mode)
        return text_list
        
    def parse(self, keyword, source='google', country='united states', language='english', file_format='txt', timeout=20):
        # Navigate to the URL
        self.driver.get(self.URL)

        # Handle the modal popup if it exists
        self.__handle_modal_popup()


        # Set the search source if different from the default (Google)
        if not source.lower() == 'google':
            self.__set_source(source)

        # Set the search country if different from the default (United States)
        if not country.lower() == 'united states':
            self.__set_country(country)

        # Set the search language if different from the default (English)
        if not language.lower() == 'english':
            self.__set_language(language)

        # Input the specified keyword into the search bar
        self.__input_keyword(keyword)

        # Click the search button
        self.__click_search_button()

        # Display a message while waiting for the keywords to load
        print('Waiting for the keywords to load...')

        # Pause execution for the specified timeout duration
        sleep(timeout)

        # Refresh the page after the initial wait
        self.driver.refresh()

        # Pause execution for an additional timeout duration
        sleep(timeout)

        # Extract the page source and create a BeautifulSoup object for parsing
        page_content = self.driver.page_source
        soup = BeautifulSoup(page_content, 'lxml')

        # Create a directory for storing the parsed data
        file_path = os.path.join(self.answer_path, keyword, source)
        self._makedir(file_path)

        # Define different types of keywords to parse
        keyword_types = [
            'questions',
            'prepositions',
            'comparisons',
            'alphabeticals',
            'related'
        ]

        # Initialize an empty list for all keywords
        all_keywords = []

        # Iterate over each type of keyword
        for key in keyword_types:
            # Parse keywords for the current type
            keywords = self.__parse_keywords(key, soup)
            print(f'Parsed {key} keywords: {len(keywords)}')

            # Write parsed keywords to a file in the specified format
            self.write_to_file(keywords, file_path, key, file_format)

            # Update the list of all keywords
            all_keywords += keywords

        # Display the total number of parsed keywords
        print(f'Total keywords: {len(all_keywords)}')

        # Write all parsed keywords to a file
        self.write_to_file(all_keywords, file_path, 'all_keywords', file_format)
















