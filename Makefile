# =============================================
# AgriVision AI — Makefile
# Common development commands
# =============================================

.PHONY: help install dev-backend dev-frontend train docker-up docker-down clean test

# Default target
help: ## Show this help message
	@echo "AgriVision AI — Development Commands"
	@echo "====================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# --- Development ---
install: ## Install all dependencies
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

dev-backend: ## Start backend dev server
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Start frontend dev server
	cd frontend && npm run dev

# --- ML ---
train: ## Train the ML model
	cd backend && python ml/train.py

evaluate: ## Evaluate the ML model
	cd backend && python ml/evaluate.py

# --- Docker ---
docker-build: ## Build Docker images
	docker compose build

docker-up: ## Start all services
	docker compose up -d

docker-down: ## Stop all services
	docker compose down

docker-logs: ## View service logs
	docker compose logs -f

# --- Testing ---
test: ## Run all tests
	cd backend && pytest tests/ -v --tb=short

test-coverage: ## Run tests with coverage
	cd backend && pytest tests/ -v --cov=app --cov-report=term-missing

# --- Code Quality ---
lint: ## Run linters
	cd backend && python -m ruff check app/
	cd frontend && npm run lint

format: ## Format code
	cd backend && python -m ruff format app/
	cd frontend && npm run format

# --- Cleanup ---
clean: ## Clean build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	cd frontend && rm -rf dist node_modules/.vite 2>/dev/null || true
