\
    @echo off
    cd /d "%~dp0"
    if not exist ".venv\Scripts\python.exe" (
        echo Virtual environment not found. Create it with:
        echo py -m venv .venv
        echo .venv\Scripts\python.exe -m pip install -r requirements.txt
        pause
        exit /b 1
    )
    ".venv\Scripts\python.exe" manage.py runserver
    pause
