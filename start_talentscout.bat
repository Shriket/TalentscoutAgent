@echo off
echo ================================================
echo TalentScout Hiring Assistant Launcher
echo ================================================
echo.

echo Checking Python installation...
"C:\Users\kcc\anaconda3\python.exe" --version
if errorlevel 1 (
    echo Error: Python not found at specified path
    echo Please check your Anaconda installation
    pause
    exit /b 1
)

echo.
echo Installing required packages...
"C:\Users\kcc\anaconda3\python.exe" -m pip install streamlit pandas pydantic python-dotenv textblob

echo.
echo Starting TalentScout Hiring Assistant...
echo Open your browser to: http://localhost:8501
echo Press Ctrl+C to stop the application
echo.

"C:\Users\kcc\anaconda3\python.exe" -m streamlit run main.py --server.port 8501

pause
