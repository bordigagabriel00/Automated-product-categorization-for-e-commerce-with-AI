# DC=docker-compose
#COMPOSE_FILES=src/inference/docker-compose.yml
#src/webui/docker-compose.yml infra/nats/docker-compose.yml infra/arangodb/docker-compose.yml
#UP_FILES=infra/nats/docker-compose.yml infra/arangodb/docker-compose.yml src/inference/docker-compose.yml src/webui/docker-compose.yml

# Función para ejecutar docker-compose con cualquier conjunto de argumentos
docker_compose_cmd = $(foreach file,$(1),$(DC) -f $(file) $(2);)

build:
	@$(call docker_compose_cmd,$(COMPOSE_FILES),build)

up-nats:
	@docker-compose -f infra/nats/docker-compose.yml up -d

down-nats:
	@docker-compose -f infra/nats/docker-compose.yml down

up-arangodb:
	@docker-compose -f infra/arangodb/docker-compose.yml up -d

down-arangodb:
	@docker-compose -f infra/arangodb/docker-compose.yml down

up-inference:
	@docker-compose -f src/inference/docker-compose.yml up -d

build-inference:
	@docker-compose -f src/inference/docker-compose.yml build

up-inference-log:
	@docker-compose -f src/inference/docker-compose.yml up

down-inference:
	@docker-compose -f src/inference/docker-compose.yml down

build-webui:
	@docker-compose -f src/webui/docker-compose.yml build

up-webui:
	@docker-compose -f src/webui/docker-compose.yml up -d

up-webui-log:
	@docker-compose -f src/webui/docker-compose.yml up

up-infra: up-nats up-arangodb

down-infra: down-nats down-arangodb

down-webui:
	@docker-compose -f src/webui/docker-compose.yml down

build-webui:
	@docker-compose -f src/webui/docker-compose.yml build

up-hub:
	@docker-compose -f docker-compose-hub.yml up -d

down-hub:
	@docker-compose -f docker-compose-hub.yml down

up-all: up-nats up-arangodb up-inference up-webui

down-all: down-nats down-arangodb down-inference down

up-hub: up-infra up-hub

up-down: down-hub down-infra


.PHONY:
