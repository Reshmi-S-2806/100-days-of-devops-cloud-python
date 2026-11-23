Website Health Monitor

A lightweight Python script that checks the availability and response latency of a list of websites, prints live results to the console, and appends timestamped records to a log file.

Features

Reads target URLs from a plain text sites.txt file (ignoring blank lines).

Sends HTTP GET requests with a 5 second timeout per site.

Classifies responses into three statuses:

UP — HTTP 200 OK

WARN — Any non-200 HTTP status code (301, 403, 404, 500)

DOWN — Connection failure, DNS error, or timeout

Measures round-trip response latency in milliseconds (ms).

Appends structured, pipe-delimited entries to health.log.

Exposes check_site(url) for reuse in other Python modules without triggering a full scan on import.

Prerequisites

Python 

requests library

Install the dependency using pip:

pip install requests


Project Structure

.
├── checker.py      # Main health-check script
├── sites.txt       # Input list of URLs to monitor (one per line)
├── health.log      # Generated log file (created automatically on first run)
└── README.md       # Project documentation


Setup & Usage

Create sites.txt in the same directory as monitor.py and add one full URL (including http:// or https://) per line:

https://www.google.com
https://github.com
https://unreachable.example.invalid


Run the script:

python monitor.py


Output Format

Each check prints to stdout and appends a line to health.log in the following format:

YYYY-MM-DD HH:MM:SS | <URL> | <STATUS> | <HTTP_CODE> | <LATENCY>ms


Example Output

2026-11-23 21:15:00 | https://www.google.com | UP | 200 | 118ms
2026-11-23 21:15:00 | https://example.com/missing | WARN | 404 | 94ms
2026-11-23 21:15:00 | https://unreachable.example.invalid | DOWN | None | Nonems


