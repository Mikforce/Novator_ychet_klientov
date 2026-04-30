from __future__ import annotations

import shutil
import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "nov" / "db.sqlite3"
BACKUP_DIR = PROJECT_ROOT / "backups" / "db"


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database file not found: {DB_PATH}")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup_path = BACKUP_DIR / "latest.sqlite3"
    temp_backup_path = BACKUP_DIR / "latest.sqlite3.tmp"

    source = sqlite3.connect(DB_PATH)
    try:
        target = sqlite3.connect(temp_backup_path)
        try:
            source.backup(target)
        finally:
            target.close()
    finally:
        source.close()

    try:
        if backup_path.exists() or backup_path.is_symlink():
            backup_path.unlink()
        shutil.move(temp_backup_path, backup_path)
    except OSError:
        pass
    finally:
        if temp_backup_path.exists():
            temp_backup_path.unlink(missing_ok=True)

    for old_backup in BACKUP_DIR.glob("db_*.sqlite3"):
        old_backup.unlink(missing_ok=True)

    print(f"Database backup created: {backup_path}")


if __name__ == "__main__":
    main()
