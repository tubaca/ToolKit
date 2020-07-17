# This Python file uses the following encoding: utf-8

import json
from os import path

class json_class:

    fileDir = path.dirname(path.realpath(__file__))

    def __init__(self):
        self.existing_data = {}

        with open(self.fileDir + '/data.json') as jsonFile:
            data = json.load(jsonFile)

        self.existing_data.update(data)

    def loadJSON(self):
        with open(self.fileDir + '/data.json') as jsonFile:
            data = json.load(jsonFile)
            return data

    def update_dict(self, new_data = {}):

        self.existing_data.update(new_data)

    def dumpJSON(self):

        json_object = json.dumps(self.existing_data, sort_keys = True, indent = 4)

        with open(self.fileDir + '/data.json', 'w') as jsonFile:
            jsonFile.write(json_object)
