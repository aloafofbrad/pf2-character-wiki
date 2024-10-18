import json

# Object that reads and writes JSON files. Holds the data from them in memory so that it can be used by other objects
class JsonReadWriter:
    def __init__(self, filename:str):
        self.setFilename(filename)
        self.setRawData(None)
        
    def setFilename(self, filename) -> None:
        self.__filename = filename
    def getFilename(self) -> str:
        return self.__filename
    
    def setRawData(self, rawData) -> None:
        self.__rawData = rawData
    def getRawData(self):
        return self.__rawData
    def clearRawData(self) -> None:
        self.setRawData(None)

    def write(self) -> None:
        json_data = json.dumps(self.__rawData, indent=4)
        try:
            with open(self.__filename, "w") as outfile:
                outfile.write(json_data)
        except FileNotFoundError as e:
            print(e)

    def read(self) -> None:
        rawData = None
        try:
            with open(self.__filename, "r") as infile:
                rawData = json.load(infile)
        except FileNotFoundError as e:
            print(e)
            rawData = None
        if rawData != None:
            self.setRawData(rawData)