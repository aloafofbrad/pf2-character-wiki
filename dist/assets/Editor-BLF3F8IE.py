from config import DATA_KEY, INFO_KEY, INDENT
from Accessor import Accessor

# Base class for updating objects inside of a json array, inside of a file
class Editor(Accessor):
    """
    Args:
    filename     the json file to be used. Also sets this for the JsonReadWriter object
    key          the key to be updated in each file
    value        the default value for objects. Can be a str, int, float, None, dict, or list (anything that is valid JSON)
    infoKey      the key used to locate info inside each json object
    arrayKey     the key used to access the json array (e.g. "data")
    ascending    sets the sort to be ascending/descending. Ascending by default
    """
    def __init__(self, filename:str, key:str, value, infoKey:str=INFO_KEY, arrayKey:str=DATA_KEY, ascending:bool=True, dryRun:bool=False):
        super().__init__(filename=filename, keys=[], arrayKey=arrayKey, infoKey=infoKey)
        self.setKey(key)
        self.setValue(value)
        self.setAscending(ascending)
        self.setDryRun(dryRun)
    
    def setKey(self, key:str) -> None:
        self.key = key
    def getKey(self) -> str:
        return self.key
    def setKeys(self, keys:list) -> None:
        try:
            self.key = keys[0]
        except IndexError:
            pass
    def getKeys(self) -> list:
        return [self.getKey(),]
    
    def setValue(self, value) -> None:
        self.value = value
    def getValue(self):
        return self.value
    
    def setAscending(self, ascending:bool=True) -> None:
        self.ascending = ascending
    def getAscending(self) -> bool:
        return self.ascending
    
    def setDryRun(self, dryRun:bool=False) -> None:
        self.dryRun = dryRun
    def getDryRun(self) -> bool:
        return self.dryRun

    # Grabs the inner, unsorted array from the dict (json object)
    def extractArray(self) -> list:
        if self.readWriter.getRawData() == None:
            self.read()
        array = []
        try:
            array = self.readWriter.getRawData()[self.getArrayKey()]
        except KeyError as e:
            print(e)
        return array
    
    # Inserts the sorted array back into the dict (json object)
    def insertArray(self, data:list) -> None:
        # self.rawData[self.arrayKey] = data
        rawdata = self.readWriter.getRawData()
        rawdata[self.getArrayKey()] = data
        self.readWriter.setRawData(rawdata)

    # Prints output expected in a dry run
    def dryRunPrint(self, data) -> None:
        import json
        rawdata = dict()
        rawdata[self.getArrayKey()] = data
        print(json.dumps(rawdata, indent=INDENT))    
    
    def write(self) -> None:
        self.readWriter.write()
    
    """
    Update all JSON objects to have the same key:value pair for a field.
    A wrapper for Editor.__execute() which handles read/write logic before and after.
    More of an example of how to extend this base class than a function intended to be used.

    args
    value       The value to be written to the object
    start       Which index to start at
    stop        If -1, updates every object
    insideInfo  If true, update this field inside the info object
    allowNull   If true, allows the field to be given a None/null value
    """
    def doMainThing(self, value=None, start:int=0, stop:int=-1, insideInfo:bool=True, allowNull:bool=False):
        # Boilerplate read code for child classes
        data = self.extractArray()

        """This is where your custom code for child classes should go.
        It does not all have to be inside a function, but that makes
        the most sense for a parent class"""
        data = self.__execute(insideInfo, start, stop, data, value, allowNull)

        # Boilerplate write/dry run code for child classes
        if self.dryRun:
            self.dryRunPrint(data)
        else:
            self.insertArray(data)
            self.write()
        self.readWriter.clearRawData()
    
    # Meant to be called by doMainThing()
    def __execute(self, insideInfo, start, stop, data, value, allowNull):
        # Use the defined default value if none is given
        if value == None and not allowNull:
            value = self.value

        if stop == -1:
            stop = len(data)
            
        if insideInfo:
            for i in range(start, stop):
                data[i][self.infoKey][self.key] = value
        else:
            for i in range(start, stop):
                data[i][self.key] = value
        return data

def test():
    from config import CHARACTER_FILE
    editor = Editor(CHARACTER_FILE, key="deity", value="Superman", dryRun=True)
    editor.doMainThing(allowNull=False)

if __name__ == "__main__":
    test()