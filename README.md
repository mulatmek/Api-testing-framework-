# API Test Framework

## overview
This project provides a **FastAPI application** packaged in Docker, along with a **Pytest-based testing framework**.  
It is designed so developers can:
- Run the API inside a container
- Automatically test endpoints with Pytest
- Publish results as **JUnit XML** for CI/CD integration

---

## REST API Endpoints

- **`GET /reverse?in=your text`**  
  Reverses the order of words in the input string.  
  Example:  
  ```http
  GET /reverse?in=The quick brown fox
  → {"result": "fox brown quick The"}
  ```

- **`GET /restore`**  
  Returns the last reversed result produced by `/reverse`.  
  Example:  
  ```http
  GET /restore
  → {"result": "fox brown quick The"}
  ```

- **`GET /health`**  
  Simple health check endpoint.  
  Example:  
  ```http
  GET /health
  → {"status": "ok"}
  ```

---

## 🐳 Running the Application

### 1. Build and Start the Container
```bash
docker-compose up --build -d
```

This will:
- Build the Docker image from the `Dockerfile`
- Start the FastAPI app container
- Expose the API at: [http://localhost:8000](http://localhost:8000)

### 2. Stop the Container
```bash
docker-compose down
```

---

## 🧪 Running the Tests

### 1. Execute Tests with Pytest
```bash
pytest
```

### 2. JUnit XML Report
Pytest is configured to export results in JUnit XML format:

```
test-results/report.xml
```

This report can be integrated with Jenkins, GitLab, GitHub Actions, or other CI/CD tools.

---

## ⚙️ Project Structure

```
.
├── app/
│   └── server.py          # FastAPI application
├── tests/
│   ├── test_api.py        # API tests
│   └── conftest.py        # Pytest fixtures (Docker + health check)
├── Dockerfile             # Docker build instructions
├── docker-compose.yml     # Container orchestration
├── pytest.ini             # Pytest config (JUnit output)
├── requirements.txt       # Dependencies
└── README.md              # Documentation
```

---

##  Development Notes
- Default base URL for tests is `http://localhost:8000`
- Override it for staging or remote testing:
  ```bash
  export API_BASE_URL=http://staging-server:8000
  pytest
  ```
- You can manually test endpoints using curl:
  ```bash
  curl "http://localhost:8000/reverse?in=hello world"
  curl "http://localhost:8000/restore"
  curl "http://localhost:8000/health"
  ```

---

## Quickstart

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-name>
   ```

2. **Build and run the app**
   ```bash
   docker-compose up --build -d
   ```

3. **Run tests**
   ```bash
   pytest
   ```

4. **Check results**
   - API available at: [http://localhost:8000](http://localhost:8000)  
   - Test report: `test-results/report.xml`  

---

