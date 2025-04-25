@echo off
REM --- Скрипт для запуска MinIO на Windows ---

REM Установка кодировки UTF-8
chcp 65001 > nul

REM Проверка наличия minio.exe
if not exist "minio.exe" (
    echo Error: File minio.exe not found in the current directory.
    echo Please place minio.exe in the same folder as this script.
    pause
    exit /b 1
)

REM Создание директории для данных MinIO (если она не существует)
if not exist "C:\minio-data" (
    mkdir C:\minio-data
    echo Created data directory for MinIO: C:\minio-data
) else (
    echo Data directory for MinIO already exists: C:\minio-data
)

REM Настройка учетных данных (если они не заданы)
if "%MINIO_ROOT_USER%" == "" (
    set MINIO_ROOT_USER=minioadmin
    echo Default login set: %MINIO_ROOT_USER%
)
if "%MINIO_ROOT_PASSWORD%" == "" (
    set MINIO_ROOT_PASSWORD=minioadmin123
    echo Default password set: %MINIO_ROOT_PASSWORD%
)

REM Запуск MinIO
echo Starting MinIO...
echo API will be available at: http://127.0.0.1:9000
echo Web console will be available at: http://127.0.0.1:9001
echo Login: %MINIO_ROOT_USER%
echo Password: %MINIO_ROOT_PASSWORD%

.\minio.exe server C:\minio-data --console-address ":9001"

REM Проверка завершения работы
if %ERRORLEVEL% neq 0 (
    echo Error starting MinIO. Exit code: %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)

echo MinIO started successfully!
pause