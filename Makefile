.PHONY: help up down build dev-backend dev-frontend test crawl index eval verify

help:
	@echo "Indonesian Gadget Vertical Search Engine Commands:"
	@echo "  make up           - Start all services with Docker Compose"
	@echo "  make down         - Stop Docker Compose services"
	@echo "  make build        - Build Docker images"
	@echo "  make test         - Run test suite"
	@echo "  make crawl        - Run multi-source crawlers"
	@echo "  make index        - Build offline Inverted Index & S-BERT embeddings"
	@echo "  make eval         - Run quantitative IR evaluation (MAP, P, R, F1)"
	@echo "  make verify       - Run pre-flight quality gatekeeper (7 gates)"

up:
	docker compose up --build

down:
	docker compose down

build:
	docker compose build

test:
	pytest tests/ -v

crawl:
	python3 -m crawler.main_crawler

index:
	python3 -m backend.app.engine.indexer

eval:
	python3 -m backend.app.engine.evaluator

verify:
	python3 scripts/verify_pipeline.py
