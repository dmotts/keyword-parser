import csv
import os
import logging

class Parser:
    def __init__(self, project_folder):
        project_path = os.path.join(os.path.abspath('projects'), project_folder)
        data_path = os.path.join(project_path, 'data')
        cookies_path = os.path.join(os.path.abspath('data'), 'cookies')

        self.project_path = self._makedir(project_path)
        self.data_path = self._makedir(data_path)
        self.cookies_path = self._makedir(cookies_path)

    @staticmethod
    def _makedir(path):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            return path
        except OSError as e:
            logging.error(f"Error creating directory {path}: {e}")
            raise

    @staticmethod
    def write_to_file(data, file_path, filename, file_format='txt'):
        filename = os.path.join(file_path, f'{filename}.{file_format}')

        try:
            if file_format == 'txt':
                with open(filename, 'a', encoding='utf-8') as file:
                    for line in data:
                        file.write(f"{line}\n")
                        file.flush()
            elif file_format == 'csv':
                with open(filename, 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(data)
                    file.flush()
            else:
                raise ValueError("Unsupported file format. Please use 'txt' or 'csv'.")

            logging.info(f"The data has been successfully written to the file.")
        except Exception as e:
            logging.error(f"An error occurred while writing data to the file: {e}")
            raise

    @staticmethod
    def write_to_doc(data, file_path, filename):
        try:
            from docx import Document
            filename = os.path.join(file_path, f'{filename}.docx')
            doc = Document()
            doc.add_paragraph(data)
            doc.save(filename)
            logging.info(f"The data has been successfully written to {filename}.")
        except ImportError as e:
            logging.error("Error: python-docx module is not installed. Install it using 'pip install python-docx'.")
            raise
        except Exception as e:
            logging.error(f"An error occurred while writing to the DOC file: {e}")
            raise