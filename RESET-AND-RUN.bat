@echo off
setlocal
cd /d "%~dp0"
title KISSAN SATHI - FINAL

echo ========================================
echo        KISSAN SATHI - FINAL VERSION
echo ========================================
echo.
echo Checking and installing packages...
echo.
call npm run install:all
if errorlevel 1 (
  echo.
  echo Package installation failed.
  echo Please send this entire window to ChatGPT.
  pause
  exit /b 1
)

echo.
echo Starting KISSAN SATHI...
echo.
call npm run dev
pause
