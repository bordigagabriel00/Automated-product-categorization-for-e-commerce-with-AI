.PHONY: run
# Run prefect server
run:
	@docker-compose --profile server up

run.bg:
	@docker-compose --profile server up -d

down:
	@docker-compose --profile server down

check:
	@poetry run python flow.py