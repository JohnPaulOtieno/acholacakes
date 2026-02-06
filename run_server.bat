@echo off
echo Starting Achola Cakes Server...
echo Activating Virtual Environment...
call venv\Scripts\activate
echo Virtual Environment Activated.
echo.
echo Running Server at http://127.0.0.1:8000/
echo Press Ctrl+C to stop the server.
python manage.py runserver
pause
