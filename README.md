# Docker API Test Framework

## Overview

This project contains a FastAPI app with two endpoints and a Pytest framework for containerized API testing.

## REST API

- **GET /reverse?in=your text**
  - Reverses word order.
- **GET /restore**
  - Returns the last reversed result.

## How to Use

### Build and Run the App

```bash
docker-compose up --build
