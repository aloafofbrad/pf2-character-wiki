"""
"""

from config import CHARACTER_FILE, JOURNAL_FILE, SETTINGS_FILE
from Updater import Updater

def main():
    characterUpdater = Updater(CHARACTER_FILE, key="", validation=False, value=None, condition=None, arguments=[], dryRun=False)

    journalUpdater = Updater(JOURNAL_FILE, key="", validation=False, value=None, condition=None, arguments=[], dryRun=False)

    settingUpdater = Updater(SETTINGS_FILE, key="", validation=False, value=None, condition=None, arguments=[], dryRun=False)

    fields = {"deities":[]}
    updaters = [settingUpdater]
    for updater in updaters:
        for key in fields.keys():
            updater.setKey(key)
            updater.setValue(fields[key])
            updater.create()

if __name__ == "__main__":
    main()