from config import DATA_KEY, INFO_KEY
import json
from jsonreadwriter import JsonReadWriter

# Simple class that skims the characters file and outputs basic data on each character
class Reader:
    def __init__(self, filename:str, keys:list=[], arrayKey:str=DATA_KEY, infoKey:str=INFO_KEY):
        self.setFilename(filename)
        self.setKeys(keys)
        self.setArrayKey(arrayKey)
        self.setInfoKey(infoKey)
        self.readWriter = JsonReadWriter(filename)
    
    def setFilename(self, filename:str) -> None:
        self.__filename = filename
    def getFilename(self) -> str:
        return self.__filename
    
    def setArrayKey(self, key:str) -> None:
        self.__arrayKey = key
    def getArrayKey(self) -> str:
        return self.__arrayKey
    
    def setInfoKey(self, key:str) -> None:
        self.__infoKey = key
    def getInfoKey(self) -> str:
        return self.__infoKey
    
    def setKeys(self, keys:list) -> None:
        self.__keys = keys
    def getKeys(self) -> list:
        return self.__keys
    
    # Opens the JSON file and reads the data
    def __read(self) -> None:
        if self.readWriter.getRawData() == None:
            self.readWriter.read()
    
    # Prints an object associated with a key
    # Like print(target[key]) but fancy
    """
    Args:
    target      the dictionary to print from
    key         the key to use for target
    printKey    If True, prints the key before the value.
    """
    def __printKeyValue(self, target:dict, key:str, printKey:bool=True) -> None:
        try:
            keyPrintValue = ""
            if printKey:
                keyPrintValue = f"{key}\t"
            objectType = type(target[key])
            if objectType in [int, float, str, None]:
                print(f"""{keyPrintValue}{target[key]}""")
            elif objectType in [list, dict]:
                print(f"""{keyPrintValue}{target[key]}""")         
        except KeyError as e:
            print(e)
    
    # Prints an object that resides in a JSON object
    # Can be a dictionary, array, etc. Type agnostic
    def __printObject(self, object) -> None:
        try:
            print(f"""{object}""")
        except Exception as e:
            print(e)

    # Prints objects assigned to given keys
    """
    Output should resemble:

    ID  Name
    0   Somebody
    1   Somebody Else
    ...

    """
    def printObjects(self, printKey:bool=True) -> None:
        self.__read()
        data = self.readWriter.getRawData()[self.__arrayKey]
        for obj in data:
            try: # Expected to raise KeyError if obj doesn't have an "info" key
                for key in self.__keys:
                    self.__printKeyValue(obj[self.__infoKey], key, printKey)
                print()
            except KeyError as e:
                pass
        print()


def main():
    from config import CHARACTER_FILE
    reader = Reader(CHARACTER_FILE)
    reader.setKeys(["id", "name"])
    reader.printObjects()

if __name__ == "__main__":
    main()