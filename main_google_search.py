import logging
from modules.google_search import GoogleSearch

def setup_logging():
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

def extract_google_pages(keywords, project_folder, max_pages, proxy=None, headless=False):
    try:
        google_search = GoogleSearch(project_folder, proxy=proxy, headless=headless)
        google_search.extract_search_pages(keywords, max_pages)
    except Exception as e:
        logging.error(f"An error occurred during extraction: {e}")

if __name__ == '__main__':
    setup_logging()

    project_name = "example_project"

    keywords = []
    while True:
        keyword = input("Enter a search term (or type 'done' to finish): ").strip()
        if keyword.lower() == 'done':
            break
        if keyword:
            keywords.append(keyword)

    if not keywords:
        logging.info("No keywords entered. Exiting.")
        exit()

    try:
        max_pages = int(input("Enter the maximum number of pages to scrape: ").strip())
    except ValueError:
        logging.error("Invalid input for maximum number of pages. Exiting.")
        exit()

    proxy = None
    headless = True
    extract_google_pages(keywords, project_name, max_pages, proxy, headless)