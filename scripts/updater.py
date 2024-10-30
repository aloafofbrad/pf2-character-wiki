from config import DATA_KEY, INFO_KEY
import json
from jsonreadwriter import JsonReadWriter

# Object that updates objects inside of a json array, inside of a file
class Updater:
    """
    Args:
    filename     the json file to be used. Also sets this for the JsonReadWriter object
    key          the key to be updated in each file
    value        the default value for objects. Can be a str, int, float, None, dict, or list (anything that is valid JSON)
    infoKey      the key used to locate info inside each json object
    arrayKey     the key used to access the json array (e.g. "data")
    ascending    sets the sort to be ascending/descending. Ascending by default
    """
    def __init__(self, filename:str, key:str, value, infoKey:str=INFO_KEY, arrayKey:str=DATA_KEY, ascending:bool=True):
        self.setFilename(filename)
        self.setKey(key)
        self.setValue(value)
        self.setInfoKey(infoKey)
        self.setArrayKey(arrayKey)
        self.setAscending(ascending)
        self.readWriter = JsonReadWriter(filename)

    def setFilename(self, filename:str) -> None:
        self.__filename = filename
    def getFilename(self) -> str:
        return self.__filename
    
    def setKey(self, key:str) -> None:
        self.__key = key
    def getKey(self) -> str:
        return self.__key
    
    def setValue(self, value) -> None:
        self.__value = value
    def getValue(self):
        return self.__value
    
    def setInfoKey(self, key:str) -> None:
        self.__infoKey = key
    def getInfoKey(self) -> str:
        return self.__infoKey
    
    def setArrayKey(self, key:str) -> None:
        self.__arrayKey = key
    def getArrayKey(self) -> str:
        return self.__arrayKey
    
    
    def setAscending(self, ascending:bool=True) -> None:
        self.__ascending = ascending
    def getAscending(self) -> bool:
        return self.__ascending

    # Grabs the inner, unsorted array from the dict (json object)
    def __extractArray(self, data:dict) -> list:
        array = []
        try:
            # array = data[self.__arrayKey]
            array = self.readWriter.getRawData()[self.getArrayKey()]
        except KeyError as e:
            print(e)
        return array
    
    # Inserts the sorted array back into the dict (json object)
    def __insertArray(self, data:list) -> None:
        # self.__rawData[self.__arrayKey] = data
        rawdata = self.readWriter.getRawData()
        rawdata[self.getArrayKey()] = data
        self.readWriter.setRawData(rawdata)
    
    """
    Update all JSON objects to have the same field.
    Recommended usage: give Updater objects a non-None value object, then call
    updateJSONObject with no arguments given.

    args
    value       The value to be written to the object
    start       Which index to start at
    stop        If -1, updates every object
    insideInfo  If true, update this field inside the info object
    allowNull   If true, allows the field to be given a None/null value
    """
    def updateJSONObjects(self, value=None, start:int=0, stop:int=-1, insideInfo:bool=True, allowNull:bool=False):
        # Use the defined default value if none is given
        if value == None and not allowNull:
            value = self.__value

        if stop == -1:
            stop = len(data)
        
        if self.readWriter.getRawData() == None:
            self.__read()
        data = self.__extractArray(self.readWriter.getRawData())

        if insideInfo:
            for i in range(start, stop):
                data[i][self.__infoKey][self.__key] = value
        else:
            for i in range(start, stop):
                data[i][self.__key] = value

        self.__insertArray(data)
        self.__write()
        self.readWriter.clearRawData()
    
    def __write(self) -> None:
        self.readWriter.write()

    def __read(self) -> None:
        self.readWriter.read()

def driver():
    from config import CHARACTER_FILE
    updater = Updater(CHARACTER_FILE, key="deity", value="")
    updater.updateJSONObjects()

if __name__ == "__main__":
    driver()