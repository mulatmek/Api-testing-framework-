# 🧪 Dockerized API Testing Framework – User Guide

## 1. Introduction
This framework provides a **generic solution** for testing Dockerized applications.  
It automates the lifecycle of your service under test:
- Builds and runs the container
- Waits until the service is healthy
- Executes your test suite
- Stops the container afterward
- Publishes test results as **JUnit XML** for CI/CD

It is designed to be **agnostic of the application itself**. Any API running inside Docker can be tested by plugging in your own test cases.

---

## 2. How It Works
The framework uses **Pytest fixtures** to orchestrate Docker and test execution:
1. **Start container** – `docker-compose up --build -d` before tests run  
2. **Health check** – waits until the service responds with a healthy status  
3. **Run tests** – executes all test files under the `tests/` directory  
4. **Stop container** – `docker-compose down` after completion (success or failure)  
5. **Export results** – stores JUnit-style report at `test-results/report.xml`

This flow means developers only need to run **`pytest`** — the framework manages everything else.

---

## 3. Project Structure
```
.
├── app/                   # Your application code (any service)
├── tests/
│   ├── test_example.py    # Example test cases
│   └── conftest.py        # Fixtures (Docker orchestration + health checks)
├── Dockerfile             # Build instructions for your service
├── docker-compose.yml     # Container orchestration
├── pytest.ini             # Pytest config (JUnit XML output)
├── requirements.txt       # Python dependencies
└── DOCUMENTATION.md       # This guide
```

---

## 4. Prerequisites
- **Docker** installed and running  
- **Docker Compose** installed  
- **Python 3.9+** with `pytest` and `requests` installed  

Install test dependencies:
```bash
pip install -r requirements.txt
```

---

## 5. Quickstart

1. **Clone your project**
   ```bash
   git clone <your-repo-url>
   cd <your-repo>
   ```

2. **Run the framework**
   ```bash
   pytest
   ```

That’s it ✅ — this will automatically:
- Build and start your container
- Wait until the service is available
- Run all discovered tests
- Shut down the container
- Write test results to `test-results/report.xml`

---

## 6. Configuration

- **Target Base URL**  
  By default, the framework tests against `http://localhost:8000`.  
  Override with:
  ```bash
  export API_BASE_URL=http://my-service:port
  pytest
  ```

- **Startup Timeout**  
  By default, it waits 15 seconds for the service to become ready.  
  Override with:
  ```bash
  export TIMEOUT=30
  pytest
  ```

---

## 7. Writing Your Own Tests

To test your own API endpoints:
1. Add a new test file under `tests/` (e.g. `test_users.py`)  
2. Use the `base_url` fixture provided by the framework  
3. Write Pytest test functions:

```python
import requests

def test_health(base_url):
    response = requests.get(f"{base_url}/health")
    assert response.status_code == 200
```

The framework will automatically discover and run these tests.

---

## 8. CI/CD Integration
- Test results are exported in **JUnit XML** format to:
  ```
  test-results/report.xml
  ```
- Most CI/CD platforms support this format natively:
  - GitHub Actions → `actions/upload-artifact`
  - GitLab CI → `artifacts:reports:junit`
  - Jenkins → JUnit plugin

---

## 9. Troubleshooting
- **Service not reachable**  
  Ensure Docker is running and ports are free. Increase timeout if needed:
  ```bash
  export TIMEOUT=60
  pytest
  ```

- **Port conflicts**  
  If another service uses the same port, update `docker-compose.yml` and adjust `API_BASE_URL`.

---
