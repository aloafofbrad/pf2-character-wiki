"""
"""

from config import CHARACTER_FILE
from Updater import Updater

def main():
    characterUpdater = Updater(CHARACTER_FILE, key="", validation=False, value=None, condition=None, arguments=[], dryRun=False)

    template = [{"id":-1, "category":"."},]
    characterUpdater.setKey("seeAlso")
    characterUpdater.setValue(template)
    characterUpdater.create()

if __name__ == "__main__":
    main()