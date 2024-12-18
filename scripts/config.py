DATA_DIR = "src/data"
BACKUP_EXT = "bak"
def BACKUP_FILE_PATH(file): return file + "." + BACKUP_EXT
ANCESTRY_FILE = f"{DATA_DIR}/ancestries.json"
BACKGROUND_FILE = f"{DATA_DIR}/backgrounds.json"
CHARACTER_FILE = f"{DATA_DIR}/characters.json"
JOURNAL_FILE = f"{DATA_DIR}/journals.json"
SETTINGS_FILE = f"{DATA_DIR}/settings.json"
DATA_KEY = "data"
INFO_KEY = "info"
ID_KEY = "id"
INDENT = 2