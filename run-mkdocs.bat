@echo off
setlocal
echo ==========================================
echo Local Documentation
echo ==========================================
echo.

:: Check if requirements-docs.txt exists
if exist "requirements-docs.txt" (
    echo [1/2] Installing documentation dependencies...
    pip install -r requirements-docs.txt
) else (
    echo [!] requirements-docs.txt not found. Skipping installation.
)

echo.
echo [2/2] Starting MkDocs server at http://127.0.0.1:8000
echo.

:: Run mkdocs via python module to avoid PATH issues
python -m mkdocs serve

endlocal
