@echo off
echo ========================================
echo   PUSH FINAL - Toutes Ameliorations
echo ========================================
echo.

cd /d c:\Downloads\proj_02_2026

echo Ameliorations incluses:
echo   [OK] AI Factory - 13 agents IA
echo   [OK] Bouton Ameliorer avec IA
echo   [OK] HTML fallback de qualite
echo   [OK] Timeout fix (heartbeat SSE)
echo   [OK] AI Improver recursif
echo.

git add .
git commit -m "feat: AI Factory complete + Bouton amelioration + HTML fallback qualite"
git push -u origin main

if %ERRORLEVEL%==0 (
    echo.
    echo ========================================
    echo   PUSH REUSSI!
    echo ========================================
    echo.
    echo Votre application est maintenant:
    echo   - Generee par 13 agents IA
    echo   - Ameliorable a l'infini
    echo   - HTML de qualite garanti
    echo   - Sans timeout sur Render
    echo.
) else (
    echo [ERREUR] Push echoue
)

pause
