@echo off
cd /d %~dp0
echo =========================================================== >> collection_log.txt
echo Starting AliExpress Coin Collector at %date% %time% >> collection_log.txt
echo =========================================================== >> collection_log.txt

:: Make sure the PATH includes Python
set PATH=%PATH%;C:\Users\mouad\anaconda3;C:\Users\mouad\anaconda3\Scripts

:: Make sure the script can find its dependencies
set PYTHONPATH=%PYTHONPATH%;%~dp0

:: Run with maximum debugging
echo Running Python version: >> collection_log.txt
python --version >> collection_log.txt 2>&1
echo. >> collection_log.txt

:: Clean up the drivers directory to ensure fresh ChromeDriver download
echo Cleaning up drivers directory... >> collection_log.txt
if exist drivers\chromedriver.exe (
    echo Removing old chromedriver.exe >> collection_log.txt
    del /F /Q drivers\chromedriver.exe >> collection_log.txt 2>&1
)

echo Running coin collector script... >> collection_log.txt
python collect_coins.py >> collection_log.txt 2>&1
echo =========================================================== >> collection_log.txt
echo Collection completed at %date% %time% >> collection_log.txt
echo =========================================================== >> collection_log.txt

:: Keep log file from growing too large (keep only last 100 KB)
for %%F in (collection_log.txt) do if %%~zF gtr 102400 (
    echo Trimming log file... >> collection_log.txt
    copy /y collection_log.txt collection_log.bak > nul
    type nul > collection_log.txt
    for /f "tokens=1,* delims=:" %%a in ('findstr /n "." collection_log.bak') do (
        if %%a gtr 500 echo %%b >> collection_log.txt
    )
    del collection_log.bak
)