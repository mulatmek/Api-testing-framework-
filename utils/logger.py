import logging
import os

logger = logging.getLogger("api_test")
logger.setLevel(logging.INFO)


def setup_logger(log_file_path):
    if logger.handlers:
        return  # Prevent adding handlers multiple times

    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logger.addHandler(ch)

    # File handler
    fh = logging.FileHandler(log_file_path, mode="w")
    fh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(fh)
