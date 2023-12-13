from pathlib import Path

# reallab
NAME_REALLAB = 'RK-Reallab'
BASE_DIR = Path(__file__).parent.parent.absolute()

LIST_DIR = Path(BASE_DIR, "database")
LIST_DIR.mkdir(parents=True, exist_ok=True)
LIST_FILE = Path(LIST_DIR, 'list')