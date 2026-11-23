import requests
import time
from datetime import datetime

def check_site(url):
    try:
        start = time.time()
        response = requests.get(url, timeout=5)
        elapsed = round((time.time() - start) * 1000)
        status = "UP" if response.status_code == 200 else "WARN"
        return status, response.status_code, elapsed
    except requests.RequestException:
        return "DOWN", None, None

def main():
    with open("sites.txt") as f:
        sites = [line.strip() for line in f if line.strip()]

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("health.log", "a") as log:
        for site in sites:
            status, code, ms = check_site(site)
            line = f"{timestamp} | {site} | {status} | {code} | {ms}ms"
            print(line)
            log.write(line + "\n")

if __name__ == "__main__":
    main()