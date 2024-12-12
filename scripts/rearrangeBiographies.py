"""
Script to replace the "biographies" object (a list of strings) with a 
list of objects called "contents". End result should look like:
{
  "id":-1,
  "info":{
    ...
    "contents":[
      "author":{
        "name":"",
        "id":null,
        "date":"",
        "addendum":""
      },
      "text":[
        "some strings that",
        "people want to read"
      ]
    ],
    ...
  }
}

Ran successfully on 12/2/2024
"""

from config import CHARACTER_FILE, SETTINGS_FILE, DATA_KEY, INFO_KEY
from Updater import Updater
from Printer import Printer

def main():
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

    settingUpdater = Updater(SETTINGS_FILE, key="contents", validation=False, value=newBioTemplate, condition=None, arguments=[], dryRun=False)
    settingUpdater.create()
    settingUpdater.setKey("history")
    settingUpdater.delete()

if __name__ == "__main__":
    main()