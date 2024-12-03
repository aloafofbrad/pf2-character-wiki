from config import DATA_KEY, INFO_KEY, ID_KEY
from collections.abc import Callable
from Editor import Editor
import traceback

# Object that performs CRUD operations on key:value pairs ("fields") inside of a json array, inside of a file
class Updater(Editor):
    """
    Args:
    filename     the json file to be used. Also sets this for the JsonReadWriter object
    key          the key to be updated in each file
    value        the default value for objects. Can be a str, int, float, None, dict, or list (anything that is valid JSON)
    condition    the condition used to test whether to update a field. Can be any function that returns a bool.
                 Example use cases:
                     return true if the field's value is a longer than 10 characters when cast as a string.
                     return true if the field's value is a number between 2 and 8.
                 takes the value of the current field as the first argument. pass any other arguments needed to the arguments
                 parameter as a list. condition() is called by Updater.validate().
                 Finally, if you need all entries to be updated, (that is, not validated, but just updated), pass False to the
                 argument "validation".
    arguments    used as arguments for the condition function.
    infoKey      the key used to locate info inside each json object
    arrayKey     the key used to access the json array (e.g. "data")
    """
    def __init__(self, filename:str, key:str, value, validation:bool, condition:Callable=None, arguments:list=[], infoKey:str=INFO_KEY, arrayKey:str=DATA_KEY, dryRun:bool=False):
        super().__init__(filename=filename, key=key, value=value, infoKey=infoKey, arrayKey=arrayKey, dryRun=dryRun)
        self.validation = None
        self.condition = None
        self.setValidation(validation)
        self.setCondition(condition)
        self.setArguments(arguments)
    
    def dummyCondition(self, value):
        return True
    
    def setCondition(self, condition:Callable=None) -> None:
        self.condition = condition
        self.setValidation(self.validation)
    def getCondition(self) -> Callable:
        return self.condition
    
    def setArguments(self, arguments:list=[]) -> None:
        self.arguments = arguments
    def getArguments(self) -> list:
        return self.arguments
    
    def setValidation(self, validation:bool=True) -> None:
        self.validation = validation
        if self.condition == None:
            self.validation = False
    def getValidation(self) -> bool:
        return self.validation
    
    # Call self.condition() 
    def validate(self, value) -> bool:
        return True
        # if not self.validation or self.condition == None:
        #     return True
        # return self.condition(arg for arg in [value] + self.arguments)
        return self.condition(value)
    
    """
    Update all JSON objects to have the same field.
    A wrapper for __create(), __update(), and __delete() which handles read/write logic before and after calling those functions.
    Recommended usage for all fields: give Editor objects a non-None value object, then call create(), update(), or delete() with no arguments given.

    args
    func        The function to be executed (__create, __update, __delete)
    value       The value to be written to the object
    start       Which index to start at
    stop        If -1, updates every object
    insideInfo  If true, update this field inside the info object
    allowNull   If true, allows the field to be given a None/null value
    """
    def __manipulateFields(self, func:Callable, value=None, insideInfo:bool=True, allowNull:bool=False):
        # Boilerplate read code for child classes
        data = self.extractArray()

        # Use the defined default value if none is given
        if value == None and not allowNull:
            value = self.value

        """This is where your custom code for child classes should go.
        It does not all have to be inside a function, but that makes
        the most sense for a parent class"""
        try:
            # data = func(self, insideInfo, start, stop, data, value, allowNull)
            if func == Updater.__delete:
                data = func(self, insideInfo, data)
            else:
                data = func(self, insideInfo, data, value)
        except Exception as e:
            # print(e)
            print(traceback.format_exc(e))
            print(f"Could not run function {func}; no data will be written")
        else:
            # Boilerplate write/dry run code for child classes
            if self.dryRun:
                self.dryRunPrint(data)
            else:
                self.insertArray(data)
                self.write()
        finally:
            self.readWriter.clearRawData()

    # Do not call this, call create()
    # def __create(self, insideInfo, start, stop, data, value, allowNull):
    def __create(self, insideInfo, data, value):
        if insideInfo:
            for i in range(0, len(data)):
                data[i][self.infoKey][self.key] = value
        else:
            for i in range(0, len(data)):
                data[i][self.key] = value
        return data
    
    # Do not call this, call update()
    # def __update(self, insideInfo, start, stop, data, value):
    def __update(self, insideInfo, data, value):
        if insideInfo:
            for i in range(0, len(data)):
                curr = data[i][self.infoKey][self.key]
                if self.validate(curr):
                    data[i][self.infoKey][self.key] = value
        else:
            for i in range(0, len(data)):
                curr = data[i][self.key]
                if self.validate(curr):
                    data[i][self.key] = value
        return data

    # Do not call this, call delete()
    # def __delete(self, insideInfo, start, stop, data, value):
    def __delete(self, insideInfo, data):
        try:
            if insideInfo:
                for i in range(0, len(data)):
                    data[i][self.infoKey].pop(self.key)
            else:
                for i in range(0, len(data)):
                    data[i].pop(self.key)
        except Exception as e:
            print(f"Could not delete key {e} at index {i}")
        return data

    def create(self, value=None, insideInfo:bool=True, allowNull:bool=False):
        self.__manipulateFields(Updater.__create, value, insideInfo, allowNull)

    def update(self, value=None, insideInfo:bool=True, allowNull:bool=False):
        self.__manipulateFields(Updater.__update, value, insideInfo, allowNull)

    def delete(self, insideInfo:bool=True, allowNull:bool=False):
        self.__manipulateFields(Updater.__delete, value=None, insideInfo=insideInfo, allowNull=allowNull)

    # Returns the largest ID found in the array, or -999 if none was found.
    def getLargestID(self) -> int:
        result = -999
        data = self.extractArray()

        for entry in data:
            try:
                currID = entry[ID_KEY]
            except KeyError as e:
                print(e)
            else:
                if currID > result:
                    result = 0+currID
        return result
    
    """
    Creates one or more new entries in the data.
    Args:
    numEntries      The number of new entries to be created.
    templateIndex   Uses the entry at this index as a template for new entries.
                    By default, uses the entry at index 0
    """
    def newEntry(self, numEntries:int=1, templateIndex:int=0):
        # Boilerplate read code for child classes
        data = self.extractArray()

        # Get the largest ID, to use in the next Entry
        next_id = 1 + self.getLargestID()
        created = 0

        # Get the template
        try:
            template = data[templateIndex]
        except IndexError as e:
            print(e)
        else:
            # Create the new entries
            while created < numEntries:
                try:
                    curr = dict()
                    for key in template.keys():
                        if type(template[key]) is dict:
                            curr[key] = template[key].copy()
                        else:
                            curr[key] = template[key]
                    curr[ID_KEY] = next_id
                    curr[INFO_KEY][ID_KEY] = next_id
                    # curr[INFO_KEY][ID_KEY] = curr[ID_KEY]
                except Exception as e:
                    print("Failed to create new entry")
                    print(e)
                else:
                    next_id += 1
                    data.append(curr)
                finally:
                    # This is in the finally block to prevent infinite loops
                    created += 1

        # Boilerplate write/dry run code for child classes
        if self.dryRun:
            self.dryRunPrint(data)
        else:
            self.insertArray(data)
            self.write()
        self.readWriter.clearRawData()

    """
    Transplant data from one field into a new one.
    
    source      The key(s) from which the data will be sourced
    dest        The key(s) to which the data will be transplanted
    insideInfo  If true, adds INFO_KEY to the start of the list

    While source and dest were originally intended to be used as lists
    of keys for dictionaries, getNestedValue() and setNestedValue() also
    support the use of lists. To read/write all values in a list stored
    in a dictionary, pass a 0 for the key. For example, if myDict looks
    like this: myDict = {'one':{'two':['some strings', 'that i want']}}
    Then source or dest should look like this: ['one', 'two', 0]
    The 0 will force all values in the list to be returned or written to,
    depending on the function you call.
    """
    def transplantField(self, source:list=[], dest:list=[], insideInfo:bool=True):
        # Boilerplate read code for child classes
        data = self.extractArray()

        if insideInfo:
            source = [INFO_KEY] + source
            dest = [INFO_KEY] + dest

        for i in range(0, len(data)):
            try:
                # Get the value to transplant
                transplantData = self.getNestedValue(source, data[i])
                # Transplant the value
                self.setNestedValue(transplantData, dest, data[i])
            except Exception as e:
                print(f"transplantField: Error during transplant {e}")
                print(f"\tdata: {transplantData}")
                print(f"\tindex: {i}")
                print()

        # Boilerplate write/dry run code for child classes
        if self.dryRun:
            self.dryRunPrint(data)
        else:
            self.insertArray(data)
            self.write()
        self.readWriter.clearRawData()

    # def transplantField(self, source:str, dest:str):
    #     self.transplantField([source,], [dest,])

    """
    Recursively access values in a dictionary.
    keys        The keys to be accessed. Used like a queue.
    target      The dictionary to retrieve a value from.

    Since this uses keys as a queue, if you have some value x stored in
    myDictionary['one']['two']['three'], your function call should look 
    like: getNestedValue(['one','two','three'], myDictionary)
    """
    def getNestedValue(self, keys:list, target):
        try:
            # Base case
            if len(keys) == 1:
                # print(f"getNestedValue: Found nested value {target[keys[0]]}")
                if type(keys[0]) == int:
                    return target
                return target[keys[0]]
            # Recursive case
            return self.getNestedValue(keys[1:], target[keys[0]])
        except KeyError as e:
            print(f"getNestedValue: Could not find key {e} from object \"{target}\"")
        return None
    
    def setNestedValue(self, value, keys:list, target):
        try:
            # Base case
            if len(keys) == 1:
                if type(value) == list and type(keys[0]) == int:
                    for i in range(0, len(value)):
                        target[keys[i]] = value[i]
                else:
                    target[keys[0]] = value
                # print(f"setNestedValue: wrote {value} to {target}")
                return target
            # Recursive case
            return self.setNestedValue(value, keys[1:], target[keys[0]])
        except KeyError as e:
            print(f"setNestedValue: Could not find key {e} from object \"{target}\"")
        return None

def test():
    from config import CHARACTER_FILE
    # Example 1: update all characters to have Superman as a deity
    # Then add a favorite superhero for them: Batman
    # Then delete the deity fields
    # fieldUpdater = Updater(CHARACTER_FILE, key="deity", value="Superman", validation=False, condition=None, arguments=[], dryRun=True)
    # def dietyIsBlank(deity):
    #     return deity in ["", "?"]
    # fieldUpdater = Updater(CHARACTER_FILE, key="deity", value=None, validation=True, condition=dietyIsBlank, dryRun=True)
    # fieldUpdater.update("Superman")
    # fieldUpdater.setCondition(None)
    # fieldUpdater.setValidation(False)
    # fieldUpdater.setKey("faveSuperHero")
    # fieldUpdater.setValue("Batman")
    # fieldUpdater.create()
    # fieldUpdater.delete()
    # 
    # Example 2: add 3 new characters and name them
    # def matchesID(id:int):
    #     # return id == test
    #     pass
    # fieldUpdater = Updater(CHARACTER_FILE, key="name", value=None, validation=True, condition=matchesID, dryRun=False)
    # start = fieldUpdater.getLargestID()
    # print(f"Largest ID: {start}")
    # newNames = ["Brain Villagers", "Mayor Brana Kotwicz", "Furnhod"]
    # fieldUpdater.newEntry(3)
    # i = 0
    # for j in range(start, start+3):
    #     def matchesID(id:int):
    #         return id == j
    #     fieldUpdater.setCondition(matchesID)
    #     fieldUpdater.update(newNames[i])
    #     i += 1    

if __name__ == "__main__":
    test()