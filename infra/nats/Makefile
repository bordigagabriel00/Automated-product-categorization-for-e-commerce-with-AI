.PHONY: run
# Run Arango server
run:
	@docker compose -f docker-compose.yml up

run.bg:
	@docker compose -f docker-compose.yml up -d

down:
	@docker compose -f docker-compose.yml down

check:
	@poetry run python nats_interaction.py
