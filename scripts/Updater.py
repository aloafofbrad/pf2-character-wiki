from config import DATA_KEY, INFO_KEY
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
        if self.readWriter.getRawData() == None:
            self.read()
        data = self.extractArray()

        # Use the defined default value if none is given
        if value == None and not allowNull:
            value = self.value

        """This is where your custom code for child classes should go.
        It does not all have to be inside a function, but that makes
        the most sense for a parent class"""
        try:
            # data = func(self, insideInfo, start, stop, data, value, allowNull)
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
        # if stop == -1:
        #     stop = len(data)
            
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
    def __delete(self, insideInfo, data, value):
        # if stop == -1:
        #     stop = len(data)
        try:
            if insideInfo:
                for i in range(0, len(data)):
                    curr = data[i][self.infoKey][self.key]
                    if self.validate(curr):
                        data[i][self.infoKey].pop(self.key)
            else:
                for i in range(0, len(data)):
                    curr = data[i][self.key]
                    if self.validate(curr):
                        data[i].pop(self.key)
        # In case somehow data[i] or data[i][self.infoKey] isn't a dict,
        # causing pop() to fail
        except Exception as e:
            print(e)
        return data

    # def create(self, value=None, start:int=0, stop:int=-1, insideInfo:bool=True, allowNull:bool=False):
    #     self.__manipulateFields(Updater.__create, value, start, stop, insideInfo, allowNull)
    def create(self, value=None, insideInfo:bool=True, allowNull:bool=False):
        self.__manipulateFields(Updater.__create, value, insideInfo, allowNull)

    # def update(self, value=None, start:int=0, stop:int=-1, insideInfo:bool=True, allowNull:bool=False):
    #     self.__manipulateFields(Updater.__update, value, start, stop, insideInfo, allowNull)
    def update(self, value=None, insideInfo:bool=True, allowNull:bool=False):
        self.__manipulateFields(Updater.__update, value, insideInfo, allowNull)

    # def delete(self, start:int=0, stop:int=-1, insideInfo:bool=True, allowNull:bool=False):
    #     self.__manipulateFields(Updater.__delete, start, stop, insideInfo, allowNull)
    def delete(self, insideInfo:bool=True, allowNull:bool=False):
        self.__manipulateFields(Updater.__delete, insideInfo, allowNull)

def test():
    from config import CHARACTER_FILE
    # fieldUpdater = Updater(CHARACTER_FILE, key="deity", value="Superman", validation=False, condition=None, arguments=[], dryRun=True)
    def dietyIsBlank(deity):
        return deity in ["", "?"]
    fieldUpdater = Updater(CHARACTER_FILE, key="deity", value=None, validation=True, condition=dietyIsBlank, dryRun=True)
    fieldUpdater.update()
    fieldUpdater.setCondition(None)
    fieldUpdater.setValidation(False)
    fieldUpdater.setKey("faveSuperHero")
    fieldUpdater.setValue("Batman")
    fieldUpdater.create()
    fieldUpdater.delete()

if __name__ == "__main__":
    test()