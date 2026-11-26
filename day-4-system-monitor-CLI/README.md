# Day 4: System Monitor CLI

A command-line tool written in Python that reports CPU, memory and disk usage plus the top processes by memory, and raises alerts when usage crosses a threshold. It can print JSON, append metrics to a CSV file, and run continuously in watch mode.

## Features

- CPU, memory and disk usage in one report
- Top N processes by memory usage
- Configurable alert thresholds
- JSON output for use with other tools
- CSV logging for later analysis (Excel, Grafana, pandas)
- Watch mode to repeat the check every N seconds
- Works on Windows, Linux and macOS

## Tech Stack

- Python 3.10+
- [psutil](https://pypi.org/project/psutil/)
- Standard library: argparse, csv, json

## Project Structure

```
day04-system-monitor/
├── monitor.py          # The CLI tool
├── requirements.txt    # Python dependencies
└── README.md
```

## Installation

```bash
git clone https://github.com/<your-username>/100-days-of-devops-cloud-python.git
cd 100-days-of-devops-cloud-python/day04-system-monitor

python -m venv venv
```

Activate the virtual environment:

```bash
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python monitor.py [options]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--cpu N` | CPU alert threshold (%) | 80 |
| `--mem N` | Memory alert threshold (%) | 80 |
| `--disk N` | Disk alert threshold (%) | 90 |
| `--top N` | Number of top processes to show | 5 |
| `--json` | Print metrics as JSON | off |
| `--csv FILE` | Append metrics to a CSV file | off |
| `--watch SECONDS` | Repeat every N seconds (Ctrl+C to stop) | off |

### Examples

Single report:

```bash
python monitor.py
```

Trigger alerts with low thresholds:

```bash
python monitor.py --cpu 10 --mem 30
```

JSON output:

```bash
python monitor.py --json
```

Log to CSV every 5 seconds:

```bash
python monitor.py --watch 5 --csv metrics.csv
```

### Sample output

```
=== System Report | 2026-11-26 18:45:02 ===
CPU:    12.4%
Memory: 63.1% (10.1/16.0 GB)
Disk:   54.2% (210.5 GB free)

Top processes by memory:
    4321  chrome.exe                4.2%
    1234  Code.exe                  3.1%
     987  python.exe                1.8%

All good.
```

## How It Works

1. `collect_metrics()` reads CPU, memory and disk values using psutil.
2. `top_processes()` lists running processes and sorts them by memory use.
3. `check_alerts()` compares each metric against its threshold.
4. The result is printed as a report or JSON, and optionally appended to a CSV.
5. In watch mode, the loop sleeps for N seconds and repeats.

## What I Learned

- Collecting system metrics with psutil
- Building CLI tools with argparse
- Threshold-based alerting, the core idea behind monitoring tools
- Exporting data as JSON and CSV
- Writing a polling loop with graceful exit on Ctrl+C

## Ideas for Improvement

- Send alerts to a Discord or Slack webhook
- Add network I/O statistics
- Add a `--duration` flag with average CPU and memory at the end
- Package it in a Docker container

## Next Steps

- Day 5: Backup automation script with Bash/Python and scheduled jobs