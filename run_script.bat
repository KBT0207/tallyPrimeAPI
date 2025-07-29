@echo off

set LOG_DIR=E:\logs
set LOG_FILE=%LOG_DIR%\task_log.log

if not exist "%LOG_DIR%" (
    echo Logs directory not found, creating it...
    mkdir "%LOG_DIR%"
)

echo Task started at: %date% %time% >> %LOG_FILE%

cd /d E:\Automation\tallyPrimeAPI

if errorlevel 1 (
    echo Failed to change directory to E:\Automation\tallyPrimeAPI at %date% %time% >> %LOG_FILE%
    exit /b 1
)

echo Running Python script using Poetry... >> %LOG_FILE%

poetry run python main.py >> %LOG_FILE% 2>&1

if errorlevel 1 (
    echo Python script execution failed at: %date% %time% >> %LOG_FILE%
    exit /b 1
)

echo Task completed at: %date% %time% >> %LOG_FILE%
exit /b 0
