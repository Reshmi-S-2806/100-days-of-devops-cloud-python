# Day 5: Folder Backup Tool

A Python command-line tool that zips a folder into a timestamped backup, stores it in a destination folder, and automatically deletes backups older than a set number of days. Every run is recorded in a log file, and the script can be scheduled to run unattended.

## Features

- Creates timestamped zip backups (e.g. `test-data_2026-11-28_18-30-00.zip`)
- Retention policy: deletes backups older than N days (default 7)
- Logs every action to `backup.log` and the console
- Safety check: refuses to save backups inside the source folder
- Clear error messages and a non-zero exit code on failure
- No external libraries needed (Python standard library only)

## Tech Stack

- Python 3.10+
- Standard library: argparse, logging, pathlib, shutil, time, datetime

## Project Structure

```
day05-backup-tool/
├── backup.py          # The backup script
├── run_backup.bat     # Wrapper used by Windows Task Scheduler
├── test-data/         # Sample folder to back up
└── README.md
```

## Installation

```bash
git clone https://github.com/<your-username>/100-days-of-devops-cloud-python.git
cd 100-days-of-devops-cloud-python/day05-backup-tool
```

No `pip install` is required.

## Usage

```bash
python backup.py --source <folder-to-back-up> --dest <backup-folder> [--keep-days N]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--source` | Folder to back up (required) | - |
| `--dest` | Folder where backups are stored (required) | - |
| `--keep-days N` | Delete backups older than N days | 7 |

### Examples

Create a backup:

```bash
python backup.py --source test-data --dest backups
```

Keep backups for 30 days:

```bash
python backup.py --source test-data --dest backups --keep-days 30
```

### Sample output

```
2026-11-28 18:30:00,123 | INFO | Backup created: test-data_2026-11-28_18-30-00.zip (0.00 MB)
2026-11-28 18:30:00,125 | INFO | Deleted old backup: test-data_2026-11-17_09-00-00.zip
2026-11-28 18:30:00,126 | INFO | Cleanup done. Old backups deleted: 1
```

## Testing the Retention Policy

Instead of waiting 7 days, fake an old file date (PowerShell):

```powershell
python backup.py --source test-data --dest backups
$f = Get-ChildItem backups\*.zip | Select-Object -First 1
$f.LastWriteTime = (Get-Date).AddDays(-10)
python backup.py --source test-data --dest backups --keep-days 7
```

The log should show the old backup being deleted.

## Scheduling

**Windows (Task Scheduler)**

```powershell
schtasks /Create /SC DAILY /ST 18:00 /TN "Day5Backup" /TR "C:\path\to\run_backup.bat"
```

Remove it with:

```powershell
schtasks /Delete /TN "Day5Backup" /F
```

**Linux / macOS (cron)**

```
0 18 * * * /usr/bin/python3 /path/to/backup.py --source /path/to/data --dest /path/to/backups
```

## How It Works

```
backup.py --source test-data --dest backups
      │
      ├─ 1. Check the source exists and the destination is safe
      ├─ 2. Zip the source into