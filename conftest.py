import csv
import os
from datetime import datetime

import pytest

from client.api_client import APIClient
from utils.logger import logger, setup_logger  # updated import

# === INIT SECTION ===

# Timestamped folder for the current run
TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
RUN_DIR = os.path.join("reports", f"run_{TIMESTAMP}")
os.makedirs(RUN_DIR, exist_ok=True)

# Set paths
CSV_REPORT_FILE = os.path.join(RUN_DIR, "test_report.csv")
LOG_FILE_PATH = os.path.join(RUN_DIR, "tests.log")
CSV_HEADER_WRITTEN = False

# Setup logger to write to this run’s log file
setup_logger(LOG_FILE_PATH)

# === CLI OPTIONS ===


def pytest_addoption(parser):
    parser.addoption(
        "--endpoint",
        action="store",
        default="https://jsonplaceholder.typicode.com",
        help="Base URL of the API to test",
    )
    parser.addoption(
        "--skip_cleanup",
        action="store_true",
        default=False,
        help="Skip environment cleanup during teardown",
    )


# === CLEANUP FUNCTION ===


def clean_up_resources():
    logger.info("🧹 Cleaning up test resources...")


# === FIXTURES ===


@pytest.fixture(scope="session")
def skip_clean_up(pytestconfig):
    return pytestconfig.getoption("skip_cleanup")


@pytest.fixture(autouse=True, scope="session")
def per_test_setup_teardown(skip_clean_up):
    logger.info("[TEST SETUP] Starting a new test...")
    yield
    if not skip_clean_up:
        clean_up_resources()
    logger.info("[TEST TEARDOWN] Finished the test.")


@pytest.fixture(scope="session")
def base_url(pytestconfig):
    return pytestconfig.getoption("endpoint")


@pytest.fixture(scope="session")
def client(base_url):
    logger.info(f"[SETUP] Creating APIClient with base URL: {base_url}")
    api_client = APIClient(base_url=base_url)
    yield api_client
    logger.info("[TEARDOWN] APIClient session completed.")


# === CUSTOM CSV REPORTING ===


def pytest_runtest_logreport(report):
    if report.when != "call":
        return

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
