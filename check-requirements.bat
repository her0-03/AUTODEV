@echo off
echo ========================================
echo AutoDev System Requirements Checker
echo ========================================
echo.

echo Checking Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Docker is NOT installed
    echo     Please install Docker Desktop from https://www.docker.com/products/docker-desktop
) else (
    echo [OK] Docker is installed
    docker --version
)
echo.

echo Checking Docker Compose...
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Docker Compose is NOT installed
    echo     Please install Docker Compose
) else (
    echo [OK] Docker Compose is installed
    docker-compose --version
)
echo.

echo Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Python is NOT installed
    echo     Please install Python 3.11+ from https://www.python.org/downloads/
) else (
    echo [OK] Python is installed
    python --version
)
echo.

echo Checking .env file...
if exist .env (
    echo [OK] .env file exists
    echo.
    echo Checking for API keys...
    findstr /C:"OPENAI_API_KEY=" .env | findstr /V /C:"OPENAI_API_KEY=$" >nul
    if %errorlevel% equ 0 (
        echo [OK] OpenAI API key is set
    ) else (
        findstr /C:"GROQ_API_KEY=" .env | findstr /V /C:"GROQ_API_KEY=$" >nul
        if %errorlevel% equ 0 (
            echo [OK] Groq API key is set
        ) else (
            echo [!] WARNING: No AI API key found in .env
            echo     Please add OPENAI_API_KEY or GROQ_API_KEY to .env file
        )
    )
) else (
    echo [X] .env file NOT found
    echo     Creating .env from .env.example...
    copy .env.example .env >nul
    echo [OK] .env file created
    echo     Please edit .env and add your API keys!
)
echo.

echo Checking required directories...
if exist uploads\ (
    echo [OK] uploads directory exists
) else (
    echo [!] Creating uploads directory...
    mkdir uploads
    echo [OK] uploads directory created
)

if exist generated\ (
    echo [OK] generated directory exists
) else (
    echo [!] Creating generated directory...
    mkdir generated
    echo [OK] generated directory created
)
echo.

echo ========================================
echo System Check Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure Docker Desktop is running
echo 2. Edit .env file and add your API key
echo 3. Run: docker-compose up --build
echo.

pause
