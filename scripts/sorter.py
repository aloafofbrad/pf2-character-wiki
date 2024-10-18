import json
from jsonreadwriter import JsonReadWriter

# Object that sorts a json array inside of a file
class Sorter:
    def __init__(self, filename:str, key:str, ascending:bool=True):
        self.setFilename(filename)
        self.setKey(key)
        self.setAscending(ascending)
        self.__arrayKey = "data"
        # self.__setRawData(None)
        self.readWriter = JsonReadWriter(filename)

    def setFilename(self, filename) -> None:
        self.__filename = filename
    def getFilename(self) -> str:
        return self.__filename
    
    def setKey(self, key:str) -> None:
        self.__key = key
    def getKey(self) -> str:
        return self.__key
    
    def setAscending(self, ascending:bool=True) -> None:
        self.__ascending = ascending
    def getAscending(self) -> bool:
        return self.__ascending
    
    # def __setRawData(self, rawData) -> None:
    #     self.__rawData = rawData
    # def __clearRawData(self) -> None:
    #     self.__setRawData(None)

    # Grabs the inner, unsorted array from the dict (json object)
    def __extractArray(self, data:dict) -> list:
        array = []
        try:
            # array = data[self.__arrayKey]
            array = self.readWriter.getRawData()[self.__arrayKey]
        except KeyError as e:
            print(e)
        return array
    
    # Inserts the sorted array back into the dict (json object)
    def __insertArray(self, data:list) -> None:
        # self.__rawData[self.__arrayKey] = data
        rawdata = self.readWriter.getRawData()
        rawdata[self.__arrayKey] = data
        self.readWriter.setRawData(rawdata)
    
    def sort(self):
        if self.readWriter.getRawData() == None:
            self.__read()
        data = self.__extractArray(self.readWriter.getRawData())
        if len(data) > 1:
            data.sort(key=lambda x: x[self.__key],reverse=(not self.__ascending))
            self.__insertArray(data)
            self.__write()
        self.readWriter.clearRawData()
    
    def __write(self) -> None:
        # json_data = json.dumps(self.__rawData, indent=4)
        # with open(self.__filename, "w") as outfile:
        #     outfile.write(json_data)
        self.readWriter.write()

    def __read(self) -> None:
        # rawData = None
        # with open(self.__filename, "r") as infile:
        #     rawData = json.load(infile)
        # if rawData != None:
        #     self.__setRawData(rawData)
        self.readWriter.read()

        # \/ Test/debug code \/
        # data = rawData["data"]
        # for dict in data:
        #     curr = dict["info"]
        #     print(f"""{curr["id"]}\t{curr["name"]}""")
        # /\ Test/debug code /\

def driver():
    import config
    sorter = Sorter(config.CHARACTER_FILE, key="id")
    # sorter.__read()
    sorter.sort()

if __name__ == "__main__":
    driver()