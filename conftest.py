import pytest

from client.api_client import APIClient
from utils.logger import logger, setup_logger
from utils.reporting import get_log_path, write_csv_row

# === Setup Logger for This Run ===
setup_logger(get_log_path())


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


@pytest.fixture(autouse=True, scope="function")
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


# === REPORTING HOOK ===
def pytest_runtest_logreport(report):
    if report.when == "call":
        write_csv_row(report)
