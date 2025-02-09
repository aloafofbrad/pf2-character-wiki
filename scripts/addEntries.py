"""
"""

from config import CHARACTER_FILE, JOURNAL_FILE, SETTINGS_FILE
from Updater import Updater

def main():
    characterUpdater = Updater(CHARACTER_FILE, key="", validation=False, value=None, condition=None, arguments=[], dryRun=False)

    journalUpdater = Updater(JOURNAL_FILE, key="", validation=False, value=None, condition=None, arguments=[], dryRun=False)

    settingUpdater = Updater(SETTINGS_FILE, key="", validation=True, value=None, condition=None, arguments=[], dryRun=False)

    updaters = [characterUpdater, journalUpdater, settingUpdater]
    newEntries = [0,0,0]
    """
    characters
    1. the gorgon
    2. the thing in the chest

    journals
    1. grandpa & grandson
    2. treasure of the mysterious underground temple

    settings
    1. the mysterious underground temple
    2. bunahver
    20250209
    """
    for i in range(0, len(updaters)):
        updaters[i].newEntry(newEntries[i])

if __name__ == "__main__":
    main()