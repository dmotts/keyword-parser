import csv
import os


class Parser:
    def __init__(self, project_folder):
        project_path = os.path.join(os.path.abspath('projects'), project_folder)
        answer_path = os.path.join(project_path, 'answerthepublic')
        ktool_path = os.path.join(project_path, 'keywordtool')
        cookies_path = os.path.join(os.path.abspath('data'), 'cookies')

        self.project_path = self._makedir(project_path)
        self.answer_path = self._makedir(answer_path)
        self.ktool_path = self._makedir(ktool_path)
        self.cookies_path = self._makedir(cookies_path)

    @staticmethod
    def _makedir(path):
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    @staticmethod
    def write_to_file(data, file_path, filename, file_format='txt'):
        # Create a full path for the file by combining the directory path, filename, and file format
        filename = os.path.join(file_path, f'{filename}.{file_format}')

        try:
            # Check the file format and write data accordingly
            if file_format == 'txt':
                # Open a text file in append mode and write each line of data
                with open(filename, 'a', encoding='utf-8') as file:
                    for line in data:
                        file.write(f"{line}\n")
                        file.flush()
            elif file_format == 'csv':
                # Open a CSV file in append mode and use csv.writer to write rows of data
                with open(filename, 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(data)
                    file.flush()
            else:
                # Raise a ValueError for unsupported file formats
                raise ValueError("Unsupported file format. Please use 'txt' or 'csv'.")

            # Display a success message after writing data to the file
            print(f"The data has been successfully written to the file.\n")  # {filename}.
        except Exception as e:
            # Display an error message if an exception occurs during file writing
            print(f"An error occurred while writing data to the file: {e}")

