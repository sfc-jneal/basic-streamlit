.EXPORT_ALL_VARIABLES:
ifneq (,$(wildcard .env))
include .env
endif

.PHONY: help build up down logs sh clean

help:
	@echo "Targets: build, up, down, logs, sh, clean"
	@echo "- build: Build local image"
	@echo "- up: Start app (docker compose up)"
	@echo "- down: Stop app"
	@echo "- logs: Tail container logs"
	@echo "- sh: Open shell in running container"
	@echo "- clean: Remove dangling images/containers (careful)"

build:
	docker compose build

build_clean:
	docker compose build --no-cache

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f app

sh:
	docker compose exec app /bin/bash

clean:
	docker system prune -f


