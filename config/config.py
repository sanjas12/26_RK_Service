from pathlib import Path

# reallab
NAME_REALLAB = 'RK-Reallab'
BASE_DIR = Path(__file__).parent.parent.absolute()

LIST_DIR = Path(BASE_DIR, "database")
LIST_DIR.mkdir(parents=True, exist_ok=True)
LIST_FILE = Path(LIST_DIR, 'list.txt')

DEFAULT_IP = "192.168.0.1"
SERVER_HOST = "192.168.0.1"
LOCAL_HOST = "localhost"
LOCAL_IP = "127.0.0.1"
SERVER_PORT = '502'
MODULE_NAME = 'Reallab'
TIME_TO_CONNECT = 0.5           # sec


ENCODING = 'UTF-8'