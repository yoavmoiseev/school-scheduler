@echo off
REM Автоматическая настройка Python-проекта
REM 1. Проверка Python
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python не найден. Установите Python 3.7+ и добавьте в PATH.
    pause
    exit /b 1
)

REM 2. Создание виртуального окружения, если не существует
if not exist .venv (
    echo Создаю виртуальное окружение...
    python -m venv .venv
    if %ERRORLEVEL% neq 0 (
        echo Ошибка при создании виртуального окружения.
        pause
        exit /b 1
    )
)

REM 3. Установка зависимостей
if exist requirements.txt (
    echo Устанавливаю зависимости из requirements.txt...
    .venv\Scripts\pip install -r requirements.txt
    if %ERRORLEVEL% neq 0 (
        echo Ошибка при установке зависимостей.
        pause
        exit /b 1
    )
) else (
    echo Внимание: файл requirements.txt не найден!
)

echo Настройка завершена. Проект готов к запуску.
pause
