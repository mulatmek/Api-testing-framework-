# utils/reporting.py

import csv
import os
from datetime import datetime

# === INIT SECTION ===

TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
RUN_DIR = os.path.join("reports", f"run_{TIMESTAMP}")
os.makedirs(RUN_DIR, exist_ok=True)

CSV_REPORT_FILE = os.path.join(RUN_DIR, "test_report.csv")
LOG_FILE_PATH = os.path.join(RUN_DIR, "tests.log")
CSV_HEADER_WRITTEN = False


def get_log_path():
    return LOG_FILE_PATH


def write_csv_row(report):
    global CSV_HEADER_WRITTEN
    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "test": report.nodeid,
        "outcome": report.outcome,
        "duration_sec": round(report.duration, 4),
        "message": str(report.longreprtext[:300]) if report.failed else "",
    }
    with open(CSV_REPORT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not CSV_HEADER_WRITTEN:
            writer.writeheader()
            CSV_HEADER_WRITTEN = True
        writer.writerow(row)
