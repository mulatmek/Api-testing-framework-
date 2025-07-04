#!/bin/bash

# Default endpoint fallback
ENDPOINT=${ENDPOINT:-"https://jsonplaceholder.typicode.com"}

echo "✅ Running tests against endpoint: $ENDPOINT"

# Run pytest
pytest --endpoint="$ENDPOINT"
