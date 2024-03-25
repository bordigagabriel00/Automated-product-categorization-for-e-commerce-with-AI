SERVICE = app
DC = docker-compose -f docker-compose.yml

# Run server
run:
	@poetry run uvicorn main:app --reload --port 9001
check-port:
	@sudo -S lsof -i :9001



# Build images as defined in docker-compose.yml
build:
	@$(DC) build

up-fg:
# Create and start containers in foreground
	@$(DC) up

# Create and start containers in detached mode
up:
	@$(DC) up -d

# Stop and remove containers, networks, and volumes
down:
	@$(DC) down -v

# Follow log output from containers
logs:
	@$(DC) logs -f

# Stop services without removing them
stop:
	@$(DC) stop

# Start services if they're stopped
start:
	@$(DC) start

# Access shell inside the 'web' service container
shell:
	@$(DC) exec web /bin/sh

.PHONY: build up down logs stop start shell
