# API Testing Framework

A robust and flexible API test automation framework using **Pytest** — designed to be clean, configurable, and CI-ready.

---

##  Features

- ✅ Command-line configuration for base URL and cleanup control
- ✅ Custom CSV reports with timestamped folders
- ✅ Structured logging per test run
- ✅ Docker-compatible with volume support
- ✅ Pre-commit hooks with `black` + `isort`

---

##  Run Locally (Python CLI)

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run tests with default settings:

```bash
pytest
```

3. Run tests with custom API endpoint:

```bash
pytest --endpoint=https://jsonplaceholder.typicode.com
```

#### CLI Options

| Option             | Description                                   |
|--------------------|-----------------------------------------------|
| `--endpoint`       | Base URL of the API (default: JSONPlaceholder) |
| `--skip_cleanup`   | Skip resource cleanup during teardown          |

---

##  Run with Docker

### 1. Build the image:

```bash
docker build -t api-test-runner .
```

### 2. Run with default settings:

```bash
docker run --rm api-test-runner
```

### 3. Run with custom endpoint:

```bash
docker run --rm -e ENDPOINT=https://your.api.com api-test-runner
```

### 4. Save logs/reports to your host:

```bash
docker run --rm -v ${PWD}/reports:/app/reports api-test-runner
```

> All logs and reports will be saved in `reports/run_<timestamp>/`

---

##  Logs & Reports

Each test run generates a timestamped folder:

```
reports/
└── run_YYYY-MM-DD_HH-MM-SS/
    ├── tests.log           # Full log output
    └── test_report.csv     # Per-test results
```

The CSV includes:
- Timestamp
- Test name
- Outcome (`passed`, `failed`, etc.)
- Duration
- Failure message (if any)

---

## Pre-commit Hooks

Keep your code clean automatically with `black` and `isort`.

### 1. Install & enable hooks:

```bash
pip install pre-commit
pre-commit install
```

### 2. Run manually on all files:

```bash
pre-commit run --all-files
```

---

## Tech Stack

- Python 3.9+
- Pytest
- Docker
- Custom CLI integration
- CSV + log reporting
- Pre-commit: `black`, `isort`


