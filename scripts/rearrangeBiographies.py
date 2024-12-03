from config import CHARACTER_FILE, DATA_KEY, INFO_KEY
from Updater import Updater
from Printer import Printer

def main():
    # newBioTemplate = dict()
    newBioTemplate = [{
        "author":{
            "name":"",
            "id":None,
            "date":"",
            "addendum":""
        },
        "text":[
            "?"
        ]
    },]

    characterUpdater = Updater(CHARACTER_FILE, key="contents", validation=False, value=newBioTemplate, condition=None, arguments=[], dryRun=False)
    characterUpdater.create()
    characterUpdater.transplantField(["biography", 0], ["contents", 0, "text"])
    characterUpdater.setKey("biography")
    characterUpdater.delete()

if __name__ == "__main__":
    main()