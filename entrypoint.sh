#!/bin/bash

# Default endpoint fallback
ENDPOINT=${ENDPOINT:-"https://jsonplaceholder.typicode.com"}

echo "✅ Running tests against endpoint: $ENDPOINT"

# Run pytest with HTML report
pytest --endpoint="$ENDPOINT" --html=report.html --self-contained-html
