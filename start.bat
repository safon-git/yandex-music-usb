@echo off
title Yandex Music Downloader

@echo.
@echo Checking for Python...
@python --version >nul 2>&1
@if %ERRORLEVEL% NEQ 0 (
    @echo.
    @echo ERROR: Python is not installed on the system.
    @echo Please install Python from the official website: https://www.python.org/downloads/
    @echo.
    @echo IMPORTANT: During installation, make sure to check the box "Add Python to PATH".
    @echo.
    @pause
    @exit /b
)
@echo Python found, continuing...
@echo.

@echo Installing/checking required dependencies...
@pip install -r requirements.txt
@echo.
@echo Starting the main program...
@python main.py

@echo.
@echo The program has finished.
@pause