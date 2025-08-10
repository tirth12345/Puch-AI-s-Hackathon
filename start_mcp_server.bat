@echo off
REM MCP Server Startup Script for Puch AI Health Buddy
echo Starting Puch AI Health Buddy MCP Server...

cd /d "C:\Users\Admin\Desktop\PuchAi Hackathon"

REM Check if Python is available
C:\Users\Admin\AppData\Local\Microsoft\WindowsApps\python3.12.exe --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.12+
    pause
    exit /b 1
)

REM Start the MCP server
echo.
echo Server ID: puch-health-buddy-mcp
echo Working Directory: %CD%
echo.

C:\Users\Admin\AppData\Local\Microsoft\WindowsApps\python3.12.exe -m src.puch_health_buddy.mcp.simple_server

echo.
echo MCP Server stopped.
pause
