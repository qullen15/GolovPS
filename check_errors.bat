@echo off
chcp 65001 >nul
echo === 1. Скрипт с ошибкой: остановка на первой ошибке ===
py src/main.py --script scripts/error.start
echo Код завершения: %ERRORLEVEL%

echo === 2. Несуществующий скрипт ===
py src/main.py --script scripts/nope.start
echo Код завершения: %ERRORLEVEL%

echo === 3. Неизвестный параметр командной строки ===
py src/main.py --unknown
echo Код завершения: %ERRORLEVEL%