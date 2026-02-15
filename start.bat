@echo off
echo Starting AutoDev Platform...
echo.

echo Checking if .env exists...
if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env
    echo Please edit .env file and add your API keys!
    pause
)

echo.
echo Starting services with Docker Compose...
docker-compose up --build

pause
