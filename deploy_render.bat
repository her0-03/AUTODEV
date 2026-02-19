@echo off
REM Script de déploiement AutoDev avec fix timeout
echo ========================================
echo   AutoDev - Deploiement Render
echo   Fix: Timeout analyses longues
echo ========================================
echo.

REM Vérifier si on est dans le bon dossier
if not exist "backend\" (
    echo [ERREUR] Dossier backend/ introuvable
    echo Executez ce script depuis la racine du projet
    pause
    exit /b 1
)

echo [1/5] Verification des fichiers modifies...
echo.

REM Vérifier les fichiers critiques
set FILES_OK=1

if not exist "backend\app\services\ai_service.py" (
    echo [X] backend\app\services\ai_service.py manquant
    set FILES_OK=0
)

if not exist "frontend\app.py" (
    echo [X] frontend\app.py manquant
    set FILES_OK=0
)

if not exist "frontend\gunicorn.conf.py" (
    echo [X] frontend\gunicorn.conf.py manquant
    set FILES_OK=0
)

if not exist "render.yaml" (
    echo [X] render.yaml manquant
    set FILES_OK=0
)

if %FILES_OK%==0 (
    echo.
    echo [ERREUR] Fichiers manquants!
    pause
    exit /b 1
)

echo [OK] Tous les fichiers sont presents
echo.

echo [2/5] Verification du heartbeat SSE...
findstr /C:"heartbeat" backend\app\services\ai_service.py >nul
if %ERRORLEVEL%==0 (
    echo [OK] Heartbeat SSE present dans ai_service.py
) else (
    echo [ATTENTION] Heartbeat SSE non trouve!
)
echo.

echo [3/5] Verification des timeouts...
findstr /C:"timeout-keep-alive 300" render.yaml >nul
if %ERRORLEVEL%==0 (
    echo [OK] Timeout backend configure (300s)
) else (
    echo [ATTENTION] Timeout backend non configure!
)

findstr /C:"timeout=600" frontend\app.py >nul
if %ERRORLEVEL%==0 (
    echo [OK] Timeout frontend SSE configure (600s)
) else (
    echo [ATTENTION] Timeout frontend non configure!
)
echo.

echo [4/5] Git status...
git status --short
echo.

echo [5/5] Pret pour le deploiement!
echo.
echo Modifications:
echo   - Heartbeat SSE (10s)
echo   - Timeout backend: 5 min
echo   - Timeout frontend: 10 min
echo   - Gunicorn optimise
echo.

set /p CONFIRM="Deployer sur Render? (o/n): "
if /i not "%CONFIRM%"=="o" (
    echo Deploiement annule
    pause
    exit /b 0
)

echo.
echo [GIT] Ajout des fichiers...
git add .

echo [GIT] Commit...
git commit -m "fix: Support analyses longues avec heartbeat SSE + timeouts etendus"

echo [GIT] Push vers GitHub...
git push origin main

if %ERRORLEVEL%==0 (
    echo.
    echo ========================================
    echo   DEPLOIEMENT REUSSI!
    echo ========================================
    echo.
    echo Render va automatiquement:
    echo   1. Detecter le push
    echo   2. Rebuilder backend + frontend
    echo   3. Deployer avec nouveaux timeouts
    echo.
    echo Surveillez: https://dashboard.render.com
    echo.
    echo URLs apres deploiement:
    echo   Backend:  https://autodev-backend-54jo.onrender.com
    echo   Frontend: https://autodev-frontend.onrender.com
    echo.
    echo Test: Uploadez un gros document (2-3 min)
    echo       La connexion devrait rester active!
    echo.
) else (
    echo.
    echo [ERREUR] Push Git echoue!
    echo Verifiez vos identifiants GitHub
    echo.
)

pause
