import datetime
import os
import csv
from rsl_comm_py.um7_broadcast_packets import UM7AllProcPacket, UM7GPSPacket

class DataCapture:
    capture_directory = "captures/"

    @staticmethod
    def create_capture_directory():
        if not os.path.exists(DataCapture.capture_directory):
            os.makedirs(DataCapture.capture_directory)

    @staticmethod
    def list_captures(current_capture):
        directory_list = os.listdir(DataCapture.capture_directory)
        directory_list.sort(reverse=True)
        if current_capture is not None:
            directory_list.remove(current_capture.path)
        return directory_list

    @staticmethod
    def get_file_path(file_name):
        return os.path.join(DataCapture.capture_directory, file_name)

    def __init__(self):
        formatted_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.path = f"um7capture_{formatted_datetime}.csv"
        self.latest_data = {}
        self.packet_types = ["UM7GPSPacket", "UM7AllProcPacket"]
        self.open_file()

    def open_file(self):
        full_path = DataCapture.capture_directory + self.path
        self.file = open(full_path, "w")
        fieldnames = ["time"] + list(UM7GPSPacket.__annotations__.keys()) + list(UM7AllProcPacket.__annotations__.keys()) + ["packet_type"]
        self.writer = csv.DictWriter(self.file, fieldnames)
        self.writer.writeheader()

    def close_file(self):
        self.file.close()

    async def write(self, data):
        if data["packet_type"] in self.packet_types:
            self.latest_data.update(data)

        self.latest_data["time"] = datetime.datetime.now().timestamp()
        self.writer.writerow(self.latest_data)

    def __del__(self):
        self.close_file()
