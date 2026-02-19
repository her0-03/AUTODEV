@echo off
echo ========================================
echo   Push vers GitHub
echo ========================================
echo.

cd /d c:\Downloads\proj_02_2026

echo [1/3] Ajout des fichiers...
git add .

echo [2/3] Commit...
git commit -m "fix: Support analyses longues avec heartbeat SSE + timeouts etendus"

echo [3/3] Push vers GitHub...
git push -u origin main

echo.
echo ========================================
echo   TERMINE!
echo ========================================
echo.
echo Render va automatiquement deployer
echo Surveillez: https://dashboard.render.com
echo.
pause
