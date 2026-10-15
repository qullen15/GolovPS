@echo off
chcp 65001 >nul
echo === 1. Без параметров (интерактив, сразу exit через pipe) ===
echo exit | py src/main.py

echo === 2. Только --vfs ===
echo exit | py src/main.py --vfs data/vfs.img

echo === 3. Только --script, успешный скрипт ===
py src/main.py --script scripts/demo.start
echo Код завершения: %ERRORLEVEL%

echo === 4. Оба параметра сразу ===
py src/main.py --vfs data/vfs.img --script scripts/demo.start
echo Код завершения: %ERRORLEVEL%