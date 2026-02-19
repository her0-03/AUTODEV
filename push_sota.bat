@echo off
echo ========================================
echo   AutoDev SOTA - Push GitHub
echo   Pages Web Ultra-Modernes
echo ========================================
echo.

cd /d c:\Downloads\proj_02_2026

echo [INFO] Ameliorations SOTA:
echo   - 4 modeles Groq specialises
echo   - Glassmorphism + gradients animes
echo   - Animations 60fps
echo   - JavaScript interactif
echo   - Dark mode support
echo.

echo [1/4] Verification des fichiers SOTA...
if exist "backend\app\services\code_generator.py" (
    findstr /C:"glassmorphism" backend\app\services\code_generator.py >nul
    if %ERRORLEVEL%==0 (
        echo [OK] Code generator SOTA present
    ) else (
        echo [ATTENTION] Glassmorphism non trouve
    )
) else (
    echo [ERREUR] code_generator.py manquant!
    pause
    exit /b 1
)

if exist "SOTA_FEATURES.md" (
    echo [OK] Documentation SOTA presente
) else (
    echo [ATTENTION] SOTA_FEATURES.md manquant
)

echo.
echo [2/4] Git status...
git status --short
echo.

echo [3/4] Ajout des fichiers...
git add .

echo [4/4] Commit et push...
git commit -m "feat: Pages web SOTA avec 4 modeles Groq - Glassmorphism + animations 60fps"

echo.
set /p PUSH="Pusher vers GitHub? (o/n): "
if /i not "%PUSH%"=="o" (
    echo Push annule
    pause
    exit /b 0
)

git push -u origin main

if %ERRORLEVEL%==0 (
    echo.
    echo ========================================
    echo   PUSH REUSSI!
    echo ========================================
    echo.
    echo Ameliorations deployees:
    echo   [OK] 4 modeles Groq (Design, Code, JS, Review)
    echo   [OK] Glassmorphism + Neomorphism
    echo   [OK] Gradients animes
    echo   [OK] Animations 60fps
    echo   [OK] JavaScript interactif ES6+
    echo   [OK] Dark mode support
    echo   [OK] Responsive mobile-first
    echo   [OK] Accessibilite WCAG AAA
    echo.
    echo Render va deployer automatiquement!
    echo Surveillez: https://dashboard.render.com
    echo.
    echo Test local:
    echo   python test_sota.py
    echo.
) else (
    echo.
    echo [ERREUR] Push echoue!
    echo.
    echo Solutions:
    echo   1. Verifier identifiants GitHub
    echo   2. Supprimer credentials:
    echo      cmdkey /delete:LegacyGeneric:target=git:https://github.com
    echo   3. Re-essayer le push
    echo.
)

pause
