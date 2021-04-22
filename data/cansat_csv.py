import csv

class cansat_csv:
    def __init__(self, file_name = "", headers = [], data = []):
        self.file_name = file_name # File name
        self.headers = headers # This need to be a list

    def csv_header(file_name, headers):
        with open(self.file_name, 'w', newline='') as file:
        	write = csv.writer(file)
        	write.writerow(self.headers)

    def csv_writer(file_name, data):
        with open(self.filename, 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.data)
