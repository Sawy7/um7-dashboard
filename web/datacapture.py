import datetime
import os
import csv

class DataCapture:
    capture_directory = "captures/"

    @staticmethod
    def create_capture_directory():
        if not os.path.exists(DataCapture.capture_directory):
            os.makedirs(DataCapture.capture_directory)

    def __init__(self):
        formatted_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.path = f"um7capture_{formatted_datetime}.csv"
        print(self.path)
        self.open_file()

    def open_file(self):
        full_path = DataCapture.capture_directory + self.path
        self.file = open(full_path, "w")
        self.writer = csv.writer(self.file)

    def close_file(self):
        self.file.close()

    async def write(self, data):
        self.writer.writerow(data)

    def __del__(self):
        print("datacapture object destroyed")
        self.close_file()
