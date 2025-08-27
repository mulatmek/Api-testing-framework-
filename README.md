# API Test Framework

A **FastAPI** app packaged in Docker with a **Pytest-based** test suite.  
Running `pytest` will **automatically build, start, health-check, and stop** the Dockerized API, and export **JUnit XML** for CI/CD.

---

## Quickstart (one command)

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-name>
   ```

2. **Run the tests**
   ```bash
   pytest
   ```

What happens:
- `conftest.py` runs `docker-compose up --build -d` before tests.
- It polls `GET /health` until `{"status":"ok"}`.
- Tests run against `http://localhost:8000` (configurable).
- When finished, it runs `docker-compose down` and writes a JUnit report to `test-results/report.xml`.

> **Prereqs:** Docker + Docker Compose installed and running.

---

##  Configuration

- **Base URL (optional):**
  ```bash
  export API_BASE_URL=http://staging-server:8000
  pytest
  ```

- **Health check timeout (optional, seconds):**
  ```bash
  export TIMEOUT=30
  pytest
  ```

> Defaults: `API_BASE_URL=http://localhost:8000`, `TIMEOUT=15`

---

##  Endpoints Covered

- **`GET /reverse?in=your text`** – returns the words in reverse order.  
  Example:
  ```http
  GET /reverse?in=The quick brown fox
  → {"result": "fox brown quick The"}
  ```

- **`GET /restore`** – returns the last result produced by `/reverse`.  
  Example:
  ```http
  GET /restore
  → {"result": "fox brown quick The"}
  ```

- **`GET /health`** – simple health check.  
  Example:
  ```http
  GET /health
  → {"status": "ok"}
  ```

---

##  Project Structure

```
.
├── app/
│   └── server.py          # FastAPI application
├── tests/
│   ├── test_api.py        # API tests
│   └── conftest.py        # Pytest fixtures (Docker orchestration + health check)
├── Dockerfile             # Docker build for the app
├── docker-compose.yml     # Container orchestration
├── pytest.ini             # Pytest config (JUnit XML output path)
├── requirements.txt       # App/test dependencies
└── README.md              # This file
```

---

## Manual Checks (optional)

If you **want** to run the app yourself (not required for tests):

```bash
docker-compose up --build -d
# App at http://localhost:8000

curl "http://localhost:8000/reverse?in=hello world"
curl "http://localhost:8000/restore"
curl "http://localhost:8000/health"

docker-compose down
```

---

##  CI/CD Notes

- The JUnit file is written to:
  ```
  test-results/report.xml
  ```
- In CI (GitHub Actions / GitLab / Jenkins), collect that path as your test report artifact.

---

