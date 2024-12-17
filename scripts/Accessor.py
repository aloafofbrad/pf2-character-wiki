from config import DATA_KEY, INFO_KEY
from jsonreadwriter import JsonReadWriter

# Base class that reads the characters file
class Accessor:
    """
    Args:
    filename     the json file to be used. Also sets this for the JsonReadWriter object
    key          keys to be printed
    filters    values to filter output by. Sort of like piping this into grep, but without having to use grep
    arrayKey     the key used to access the json array (e.g. "data")
    infoKey      the key used to locate info inside each json object
    """
    def __init__(self, filename:str, keys:list=[], arrayKey:str=DATA_KEY, infoKey:str=INFO_KEY):
        self.setArrayKey(arrayKey)
        self.setFilename(filename)
        self.setInfoKey(infoKey)
        self.setKeys(keys)
        self.filters = {}
        self.readWriter = JsonReadWriter(filename)
    
    def setArrayKey(self, key:str) -> None:
        self.arrayKey = key
    def getArrayKey(self) -> str:
        return self.arrayKey

    def setFilename(self, filename:str) -> None:
        self.filename = filename
        try:
            self.readWriter.setFilename(self.filename)
        except AttributeError:
            pass
    def getFilename(self) -> str:
        return self.filename
    
    def setInfoKey(self, key:str) -> None:
        self.infoKey = key
    def getInfoKey(self) -> str:
        return self.infoKey
    
    def setKeys(self, keys:list) -> None:
        self.keys = keys
    def getKeys(self) -> list:
        return self.keys
    
    def addFilter(self, filter:str, values:list) -> None:
        self.filters[filter] = [str(value) for value in values]
        """
        The filter given is a key that corresponds to a key in character information.
        The values given are valid values that that key can have.
        For example, if filter="name" and values=["Alice","Bob"], then only characters
        with the names "Alice" and "Bob" should be printed.
        """
    
    def getFilters(self) -> list:
        return self.filters
    
    def hasFilters(self) -> bool:
        return len(self.filters.keys()) > 0
    
    def resetFilters(self) -> None:
        self.filters = {}
    
    # Opens the JSON file and reads the data
    def read(self) -> None:
        if self.readWriter.getRawData() == None:
            self.readWriter.read()
    
    def getData(self):
        return self.readWriter.getRawData()
    
    def doMainThing(self):
        self.read()

def test():
    from config import CHARACTER_FILE
    accessor = Accessor(CHARACTER_FILE)
    accessor.doMainThing()
    data = accessor.getData()
    print(data)

if __name__ == "__main__":
    # import sys
    # main(sys.argv[1:])
    test()