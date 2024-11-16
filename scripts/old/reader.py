from config import DATA_KEY, INFO_KEY
import json
from jsonreadwriter import JsonReadWriter

# Class that skims the characters file and outputs basic data on each character
class Reader:
    """
    Args:
    filename     the json file to be used. Also sets this for the JsonReadWriter object
    key          keys to be printed
    __filters    values to filter output by. Sort of like piping this into grep, but without having to use grep
    arrayKey     the key used to access the json array (e.g. "data")
    infoKey      the key used to locate info inside each json object
    """
    def __init__(self, filename:str, keys:list=[], arrayKey:str=DATA_KEY, infoKey:str=INFO_KEY):
        self.setFilename(filename)
        self.setKeys(keys)
        self.setArrayKey(arrayKey)
        self.setInfoKey(infoKey)
        self.__filters = {}
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
    
    def resetFilters(self) -> None:
        self.__filters = {}

    def addFilter(self, filter:str, values:list) -> None:
        self.__filters[filter] = [str(value) for value in values]
        """
        The filter given is a key that corresponds to a key in character information.
        The values given are valid values that that key can have.
        For example, if filter="name" and values=["Alice","Bob"], then only characters
        with the names "Alice" and "Bob" should be printed.
        """
    
    def hasFilters(self) -> bool:
        return len(self.__filters.keys()) > 0
    
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

    Returns True if printing was successful
    """
    def __printKeyValue(self, target:dict, key:str, printKey:bool=False) -> bool:
        result = False
        try:
            keyPrintValue = ""
            endPrintValue = "\t"
            if printKey:
                keyPrintValue = f"{key}\t"
                endPrintValue = "\n"
            objectType = type(target[key])
            if objectType in [int, float, str, None]:
                print(f"""{keyPrintValue}{target[key]}""",end=endPrintValue)
                result = True
            elif objectType in [list, dict]:
                print(f"""{keyPrintValue}{target[key]}""",end=endPrintValue)
                result = True
        except KeyError:
            pass
        return result
    
    """# Prints an object that resides in a JSON object
    # Can be a dictionary, array, etc. Type agnostic
    def __printObject(self, object) -> None:
        try:
            print(f"{object}")
        except Exception as e:
            pass"""
    
    def __printHeader(self) -> None:
        for key in self.__keys:
            print(key, end="\t")
        print()

    # Prints all key value pairs within a JSON object.
    def printJSONObject(self, object:dict, printKey:bool=False) -> None:
        """
        printed Determines whether to print \n for the next object.
        It's set to True if there has been one key:value pair printed from this object.
        That is, if self.__printKeyValue has returned True at least once.
        """
        printed = False
        try:
            for key in self.__keys:
                printed = self.__printKeyValue(object[self.__infoKey], key, printKey)
        except KeyError as e:
            pass
        if printed: # then print \n so the next object starts on a newline
            print()

    """
    Print objects assigned to given keys
    Output should resemble:

    ID  Name
    0   Somebody
    1   Somebody Else
    ...

    """
    def printObjects(self, printKey:bool=False) -> None:
        self.__read()
        data = self.readWriter.getRawData()[self.__arrayKey]
        self.__printHeader()

        # If the user didn't give filters, just print each obj in data
        if not self.hasFilters():
            for obj in data:
                self.printJSONObject(obj, printKey)

        elif self.hasFilters():
            # If the user did give filters, get valid keys from those filters
            validKeys = [key for key in self.__filters.keys()]
            for obj in data:
                for vk in validKeys:
                    try:
                        """Check if the object's value of that key is in the filter's list of
                        values for that key. In other words, check that this object matches
                        at least one of the desired values to be found"""
                        objectValue = obj[self.__infoKey][vk]
                        objectValue = str(objectValue)
                        objectValue = objectValue.lower()

                        """This second cast of v for v in self.__filters[vk] to srting would
                        normally be unecessary, but certain IDEs (VS Code) may not catch that
                        v is already a string. This second cast is done purely to suppress
                        warnings/errors."""
                        filterValues = [v for v in self.__filters[vk]]
                        filterValues = [str(fv) for fv in filterValues]
                        filterValues = [fv.lower() for fv in filterValues]

                        """If objectValue is present in filterValues, the object can be printed.
                        This doesn't mean that all values in filterValues are present in the object,
                        just that at least one is."""
                        if objectValue in filterValues:
                            self.printJSONObject(obj, printKey)
                    except KeyError as e:
                        pass
                    except Exception as e: # In case casting objectValue as str goes wrong
                        pass

# Finds values in arguments, given a list of flags.
def findValues(args:list, flags:list) -> list:
    result = []
    i = 0
    while i < len(args):
        try:
            curr = args[i]
        except IndexError:
            return result
            # Shouldn't happen, maybe remove the try block.
        
        if curr in flags:
            i += 1
            try:
                values = [word for word in args[i].split(",")]
            except Exception as e:
                print(e)
                values = []
            finally:
                result = result + values
                i += 1
        else:
            i += 1
    return result

"""Parses the arguments and returns a dict of flags and the arguments passed with them
ids     character IDs used to filter by ID.
names   character names used to filter by name.
keys    keys to be printed (name, ancestry, background, class, etc)

args:
args    the arguments passed to the program
"""
def parse(args) -> dict:
    result = {
        "ids":None,
        "names":None,
        "keys":None,
        }
    if "--ids" in args or "-i" in args:
        result["ids"] = findValues(args, flags=["--ids", "-i"])
    if "--names" in args or "-n" in args:
        result["names"] = findValues(args, flags=["--names", "-n"])
    if "--keys" in args or "-k" in args:
        result["keys"] = findValues(args, flags=["--keys", "-k"])
    return result

def test():
    from config import CHARACTER_FILE
    reader = Reader(CHARACTER_FILE)
    reader.setKeys(["id", "name"])
    reader.printObjects()

"""
Expected syntax for running this program:

python3 reader.py --keys id,name,ancestry,class,background
python3 reader.py -k id,name
python3 reader.py -k "id,name"

Expected output should display all keys given that exist in each character's JSON object
"""
def main(argv):
    from config import CHARACTER_FILE
    reader = Reader(CHARACTER_FILE)
    args = parse(argv)
    if args["ids"] != None:
        reader.addFilter("id", args["ids"])
    if args["names"] != None:
        reader.addFilter("name", args["names"])
    if args["keys"] != None:
        reader.setKeys(args["keys"])
    reader.printObjects()

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])