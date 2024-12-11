"""
"""

from config import CHARACTER_FILE, JOURNAL_FILE, SETTINGS_FILE
from Updater import Updater

def main():
    characterUpdater = Updater(CHARACTER_FILE, key="", validation=False, value=None, condition=None, arguments=[], dryRun=False)

    journalUpdater = Updater(JOURNAL_FILE, key="", validation=False, value=None, condition=None, arguments=[], dryRun=False)

    settingUpdater = Updater(SETTINGS_FILE, key="", validation=True, value=None, condition=None, arguments=[], dryRun=False)

    updaters = [journalUpdater]
    newEntries = 1
    for updater in updaters:
        updater.newEntry(1, 0)

if __name__ == "__main__":
    main()