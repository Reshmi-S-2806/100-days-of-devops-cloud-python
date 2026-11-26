import argparse
import csv
import json
import os
import time
from datetime import datetime

import psutil


def collect_metrics():
    # Use the drive root so it works on Windows and Linux
    disk_path = os.path.abspath(os.sep)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage(disk_path)
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": mem.percent,
        "memory_used_gb": round(mem.used / 1024**3, 2),
        "memory_total_gb": round(mem.total / 1024**3, 2),
        "disk_percent": disk.percent,
        "disk_free_gb": round(disk.free / 1024**3, 2),
    }


def top_processes(n=5):
    procs = []
    for p in psutil.process_iter(["pid", "name", "memory_percent"]):
        try:
            procs.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    procs.sort(key=lambda x: x["memory_percent"] or 0, reverse=True)
    return procs[:n]


def check_alerts(metrics, cpu_limit, mem_limit, disk_limit):
    alerts = []
    if metrics["cpu_percent"] > cpu_limit:
        alerts.append(f"CPU high: {metrics['cpu_percent']}% (limit {cpu_limit}%)")
    if metrics["memory_percent"] > mem_limit:
        alerts.append(f"Memory high: {metrics['memory_percent']}% (limit {mem_limit}%)")
    if metrics["disk_percent"] > disk_limit:
        alerts.append(f"Disk high: {metrics['disk_percent']}% (limit {disk_limit}%)")
    return alerts


def print_report(metrics, procs, alerts):
    print(f"\n=== System Report | {metrics['timestamp']} ===")
    print(f"CPU:    {metrics['cpu_percent']}%")
    print(f"Memory: {metrics['memory_percent']}% "
          f"({metrics['memory_used_gb']}/{metrics['memory_total_gb']} GB)")
    print(f"Disk:   {metrics['disk_percent']}% ({metrics['disk_free_gb']} GB free)")
    print("\nTop processes by memory:")
    for p in procs:
        print(f"  {p['pid']:>6}  {p['name']:<25} {p['memory_percent']:.1f}%")
    if alerts:
        print("\n!! ALERTS !!")
        for a in alerts:
            print(f"  - {a}")
    else:
        print("\nAll good.")


def save_csv(metrics, path):
    new_file = not os.path.exists(path)
    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=metrics.keys())
        if new_file:
            writer.writeheader()
        writer.writerow(metrics)


def main():
    parser = argparse.ArgumentParser(description="Simple system monitor")
    parser.add_argument("--cpu", type=float, default=80, help="CPU alert threshold %")
    parser.add_argument("--mem", type=float, default=80, help="Memory alert threshold %")
    parser.add_argument("--disk", type=float, default=90, help="Disk alert threshold %")
    parser.add_argument("--top", type=int, default=5, help="Number of top processes")
    parser.add_argument("--json", action="store_true", help="Print metrics as JSON")
    parser.add_argument("--csv", metavar="FILE", help="Append metrics to a CSV file")
    parser.add_argument("--watch", type=int, metavar="SECONDS",
                        help="Repeat every N seconds (Ctrl+C to stop)")
    args = parser.parse_args()

    try:
        while True:
            metrics = collect_metrics()
            alerts = check_alerts(metrics, args.cpu, args.mem, args.disk)

            if args.json:
                print(json.dumps({**metrics, "alerts": alerts}, indent=2))
            else:
                print_report(metrics, top_processes(args.top), alerts)

            if args.csv:
                save_csv(metrics, args.csv)

            if not args.watch:
                break
            time.sleep(args.watch)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()