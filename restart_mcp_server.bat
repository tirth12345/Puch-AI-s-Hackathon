@echo off
REM MCP Server Restart Script for Puch AI Health Buddy
echo Restarting Puch AI Health Buddy MCP Server...

cd /d "C:\Users\Admin\Desktop\PuchAi Hackathon"

REM Check if Python is available
C:\Users\Admin\AppData\Local\Microsoft\WindowsApps\python3.12.exe --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.12+
    pause
    exit /b 1
)

echo.
echo Server ID: puch-health-buddy-mcp
echo Working Directory: %CD%
echo.

REM Restart the MCP server using the manager
C:\Users\Admin\AppData\Local\Microsoft\WindowsApps\python3.12.exe scripts\mcp_server_manager.py restart

echo.
echo MCP Server restart completed.
pause
