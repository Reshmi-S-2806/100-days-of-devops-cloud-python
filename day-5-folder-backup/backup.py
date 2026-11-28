import argparse
import logging
import shutil
import time
from datetime import datetime
from pathlib import Path


def setup_logging(dest: Path):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(dest / "backup.log"),
            logging.StreamHandler(),
        ],
    )


def create_backup(source: Path, dest: Path) -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    archive_base = dest / f"{source.name}_{timestamp}"
    archive_path = shutil.make_archive(str(archive_base), "zip", root_dir=source)
    return Path(archive_path)


def delete_old_backups(dest: Path, prefix: str, keep_days: int) -> int:
    cutoff = time.time() - keep_days * 24 * 60 * 60
    deleted = 0
    for file in dest.glob(f"{prefix}_*.zip"):
        if file.stat().st_mtime < cutoff:
            file.unlink()
            logging.info(f"Deleted old backup: {file.name}")
            deleted += 1
    return deleted


def main():
    parser = argparse.ArgumentParser(description="Simple folder backup tool")
    parser.add_argument("--source", required=True, help="Folder to back up")
    parser.add_argument("--dest", required=True, help="Folder to store backups")
    parser.add_argument("--keep-days", type=int, default=7,
                        help="Delete backups older than this many days (default 7)")
    args = parser.parse_args()

    source = Path(args.source).resolve()
    dest = Path(args.dest).resolve()

    if not source.is_dir():
        raise SystemExit(f"Source folder not found: {source}")

    # Safety: backing up a folder into itself would make the zip grow forever
    if dest == source or source in dest.parents:
        raise SystemExit("Destination must be outside the source folder.")

    dest.mkdir(parents=True, exist_ok=True)
    setup_logging(dest)

    try:
        backup_file = create_backup(source, dest)
        size_mb = backup_file.stat().st_size / 1024**2
        logging.info(f"Backup created: {backup_file.name} ({size_mb:.2f} MB)")
    except Exception as e:
        logging.error(f"Backup failed: {e}")
        raise SystemExit(1)

    deleted = delete_old_backups(dest, source.name, args.keep_days)
    logging.info(f"Cleanup done. Old backups deleted: {deleted}")


if __name__ == "__main__":
    main()