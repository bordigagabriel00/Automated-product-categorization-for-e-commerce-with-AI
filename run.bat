@echo off
SETLOCAL ENABLEEXTENSIONS

:: Definir los comandos para subir y bajar servicios
SET UP_NATS=docker-compose -f infra/nats/docker-compose.yml up -d
SET DOWN_NATS=docker-compose -f infra/nats/docker-compose.yml down
SET UP_ARANGODB=docker-compose -f infra/arangodb/docker-compose.yml up -d
SET DOWN_ARANGODB=docker-compose -f infra/arangodb/docker-compose.yml down
SET UP_INFERENCE=docker-compose -f src/inference/docker-compose.yml up -d
SET DOWN_INFERENCE=docker-compose -f src/inference/docker-compose.yml down
SET UP_WEBUI=docker-compose -f src/webui/docker-compose.yml up -d
SET DOWN_WEBUI=docker-compose -f src/webui/docker-compose.yml down

:main
if "%1"=="" goto help
if "%1"=="up-all" goto up-all
if "%1"=="down-all" goto down-all
if "%1"=="up-nats" call :up-nats
if "%1"=="down-nats" call :down-nats
if "%1"=="up-arangodb" call :up-arangodb
if "%1"=="down-arangodb" call :down-arangodb
if "%1"=="up-inference" call :up-inference
if "%1"=="down-inference" call :down-inference
if "%1"=="up-webui" call :up-webui
if "%1"=="down-webui" call :down-webui
goto end

:up-all
call :up-nats
call :up-arangodb
call :up-inference
call :up-webui
goto end

:down-all
call :down-nats
call :down-arangodb
call :down-inference
call :down-webui
goto end

:up-nats
%UP_NATS%
goto end

:down-nats
%DOWN_NATS%
goto end

:up-arangodb
%UP_ARANGODB%
goto end

:down-arangodb
%DOWN_ARANGODB%
goto end

:up-inference
%UP_INFERENCE%
goto end

:down-inference
%DOWN_INFERENCE%
goto end

:up-webui
%UP_WEBUI%
goto end

:down-webui
%DOWN_WEBUI%
goto end

:help
echo Usage: script.bat [command]
echo Commands:
echo up-all, down-all, up-nats, down-nats, up-arangodb, down-arangodb, up-inference, down-inference, up-webui, down-webui
goto end

:end
ENDLOCAL
