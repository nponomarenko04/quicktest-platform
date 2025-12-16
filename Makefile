.PHONY: help up down test test-chrome test-firefox test-api clean allure-report

help:
	@echo "QuickTest Platform Commands:"
	@echo "  make up       - Start all services"
	@echo "  make down     - Stop all services"
	@echo "  make test     - Run all tests"
	@echo "  make test-chrome  - Run Chrome tests only"
	@echo "  make test-firefox - Run Firefox tests only"
	@echo "  make test-api - Run API tests only"
	@echo "  make clean    - Remove all containers and volumes"
	@echo "  make allure-report - Generate Allure report"

up:
	docker compose up -d --build

down:
	docker compose down

test:
	docker compose exec test-runner pytest tests/ -v

test-chrome:
	docker compose exec test-runner pytest tests/ -m chrome -v

test-firefox:
	docker compose exec test-runner pytest tests/ -m firefox -v

test-api:
	docker compose exec test-runner pytest tests/ -m api -v

clean:
	docker compose down -v
	docker system prune -f

allure-report:
	docker compose exec test-runner allure generate allure-results --clean -o results/allure-reports
	@echo "📊 Allure report generated: results/allure-reports/index.html"
