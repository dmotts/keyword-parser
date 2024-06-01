from modules.google_search import GoogleSearch

if __name__ == '__main__':
    try:
        keywords = []
        while True:
            search_term = input("Enter the search term for a keyword (press Enter to finish): ")
            if not search_term:
                break
            keywords.append(search_term)

        max_pages = int(input("Enter the number of pages to search: "))

        # Determine project name based on keywords before the first quotation mark
        project_name = ""
        for keyword in keywords:
            if '"' in keyword:
                project_name = " ".join(keyword.split('"')[0].split())
                break
        if not project_name:
            project_name = " ".join(keywords)

        google_search = GoogleSearch(project_name)
        google_search.save_search_results(keywords, max_pages)
    except ValueError:
        print("Please enter a valid number for the number of pages.")
    except Exception as e:
        print(f"An error occurred: {e}")