.PHONY: run
# Run server
run:
	@poetry run uvicorn main:app --reload --port 9001
check-port:
	@sudo -S lsof -i :9001

