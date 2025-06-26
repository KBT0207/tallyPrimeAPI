@echo off

:: Define log file location
set LOG_DIR=E:\logs
set LOG_FILE=%LOG_DIR%\task_log.log

:: Check if the logs directory exists, if not, create it
if not exist "%LOG_DIR%" (
    echo Logs directory not found, creating it...
    mkdir "%LOG_DIR%"
)

:: Log the start time
echo Task started at: %date% %time% >> %LOG_FILE%

:: Change to the project directory
cd /d E:\Automation\tallyPrimeAPI

:: Check if the directory change was successful
if errorlevel 1 (
    echo Failed to change directory to E:\Automation\tallyPrimeAPI at %date% %time% >> %LOG_FILE%
    exit /b 1
)

:: Log that the Python script is running
echo Running Python script using Poetry... >> %LOG_FILE%

:: Run the Python script and log output (both stdout and stderr)
poetry run python main.py >> %LOG_FILE% 2>&1

:: Check if the Python script ran successfully
if errorlevel 1 (
    echo Python script execution failed at: %date% %time% >> %LOG_FILE%
    exit /b 1
)

:: Log the completion time
echo Task completed at: %date% %time% >> %LOG_FILE%
exit /b 0
