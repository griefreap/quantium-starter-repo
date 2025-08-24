@echo off
echo Activating virtual environment...
call test_env\Scripts\activate

echo Running tests...
pytest tests/
if %errorlevel% neq 0 (
    echo Tests failed!
    exit /b 1
) else (
    echo All tests passed!
    exit /b 0
)
