@echo off
REM ===============================
REM Run all tests for the project
REM ===============================

echo Activating virtual environment...
call venv\Scripts\activate

if errorlevel 1 (
    echo ❌ Could not activate virtual environment. Make sure venv exists.
    exit /b 1
)

echo Running tests...
pytest --disable-warnings -v
if errorlevel 1 (
    echo ❌ Tests failed!
    exit /b 1
) else (
    echo ✅ All tests passed!
    exit /b 0
)
