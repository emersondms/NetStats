import json

class JsonReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def __load_data(self, mode):
        file = open(self.file_path, mode)
        data = json.load(file)
        file.close()
        return data

    def get_prop_value(self, prop):
        data = self.__load_data("r")
        return data[prop]

    def set_prop_value(self, prop, value):
        data = self.__load_data("r")
        data[prop] = value
        file = open(self.file_path, "w")
        json.dump(data, file)
        file.close()