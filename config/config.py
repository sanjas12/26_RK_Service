from pathlib import Path

# reallab
NAME_REALLAB = 'RK-Reallab'
BASE_DIR = Path(__file__).parent.parent.absolute()

LIST_DIR = Path(BASE_DIR, "database")
LIST_DIR.mkdir(parents=True, exist_ok=True)
RAW_FILE = Path(LIST_DIR, 'list.txt')
LIST_FILE = Path(LIST_DIR, 'list')

SERVER_DEFAULT = "192.168.0.1"
SERVER_HOST = "192.168.30.11"

ENCODING = 'UTF-8'