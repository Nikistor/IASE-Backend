@echo off
REM Установка кодировки UTF-8
chcp 65001 > nul

REM Скрипт для запуска Django-проекта
echo --- Начинаем процесс подготовки и запуска Django-проекта ---

REM Шаг 1: Создание миграций
echo [1/5] Создание миграций...
python manage.py makemigrations
if %ERRORLEVEL% neq 0 (
    echo Ошибка при создании миграций. Завершение работы.
    exit /b %ERRORLEVEL%
)

REM Шаг 2: Проверка наличия миграций перед выполнением migrate
echo [2/5] Проверка наличия непримененных миграций...
python manage.py showmigrations --list | findstr "[ ]"
if %ERRORLEVEL% equ 0 (
    echo Найдены непримененные миграции. Применяем их...
    python manage.py migrate
    if %ERRORLEVEL% neq 0 (
        echo Ошибка при выполнении миграций. Завершение работы.
        exit /b %ERRORLEVEL%
    )
) else (
    echo Миграции уже применены. Пропускаем шаг.
)

REM Шаг 3: Добавление пользователей
echo [3/5] Добавление пользователей...
python manage.py add_users
if %ERRORLEVEL% neq 0 (
    echo Ошибка при добавлении пользователей. Завершение работы.
    exit /b %ERRORLEVEL%
)

REM Шаг 4: Заполнение базы данных
echo [4/5] Заполнение базы данных...
python manage.py fill_db
if %ERRORLEVEL% neq 0 (
    echo Ошибка при заполнении базы данных. Завершение работы.
    exit /b %ERRORLEVEL%
)

REM Шаг 5: Запуск сервера разработки
echo [5/5] Запуск сервера разработки...
python manage.py runserver
if %ERRORLEVEL% neq 0 (
    echo Ошибка при запуске сервера. Завершение работы.
    exit /b %ERRORLEVEL%
)

echo --- Процесс успешно завершен ---