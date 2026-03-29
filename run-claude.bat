@echo off
setlocal

rem Claude -> Ollama bridge for local model usage
rem Usage:
rem   run-claude-ollama.bat
rem   run-claude-ollama.bat qwen3-coder
rem   run-claude-ollama.bat gpt-oss:120b-cloud

set "OLLAMA_URL=http://localhost:11434"
set "DEFAULT_MODEL=gpt-oss:20b-cloud"

if "%~1"=="" (
    set "MODEL=%DEFAULT_MODEL%"
) else (
    set "MODEL=%~1"
)

echo ==========================================
echo Claude CLI with Ollama
echo ==========================================
echo Ollama endpoint: %OLLAMA_URL%
echo Model: %MODEL%
echo.

where ollama >nul 2>nul
if errorlevel 1 (
    echo [ERROR] ollama is not installed or not in PATH.
    echo Install Ollama and try again.
    exit /b 1
)

where claude >nul 2>nul
if errorlevel 1 (
    echo [ERROR] claude CLI is not installed or not in PATH.
    echo Install Claude CLI and try again.
    exit /b 1
)

rem Check whether Ollama responds
curl -s %OLLAMA_URL% >nul 2>nul
if errorlevel 1 (
    echo [WARN] Could not reach Ollama at %OLLAMA_URL%
    echo Make sure Ollama is running. You may need to start:
    echo   ollama serve
    echo.
)

rem Verify model exists
ollama list | findstr /i /c:"%MODEL%" >nul
if errorlevel 1 (
    echo [ERROR] Model "%MODEL%" was not found in ollama list.
    echo Available models:
    ollama list
    exit /b 1
)

rem Set Anthropic-compatible env vars for this session only
set "ANTHROPIC_BASE_URL=%OLLAMA_URL%"
set "ANTHROPIC_AUTH_TOKEN=ollama"
set "ANTHROPIC_API_KEY="

echo Environment configured:
echo   ANTHROPIC_BASE_URL=%ANTHROPIC_BASE_URL%
echo   ANTHROPIC_AUTH_TOKEN=%ANTHROPIC_AUTH_TOKEN%
echo   ANTHROPIC_API_KEY=[empty]
echo.

echo Launching Claude with Ollama model "%MODEL%"...
echo.

claude --model "%MODEL%"

endlocal