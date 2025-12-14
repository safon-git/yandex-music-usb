@echo off
title Yandex Music Downloader

echo.
echo Проверка наличия Python...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ОШИБКА: Python не найден в системе.
    echo Пожалуйста, установите Python с официального сайта: https://www.python.org/downloads/
    echo.
    echo ВАЖНО: Во время установки ОБЯЗАТЕЛЬНО поставьте галочку "Add Python to PATH".
    echo.
    pause
    exit /b
)
echo Python найден, продолжаем...
echo.

echo Установка/проверка необходимых библиотек...
pip install -r requirements.txt
echo.
echo Запуск основной программы...
python main.py

echo.
echo Программа завершила свою работу.
pause