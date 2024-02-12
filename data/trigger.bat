@echo off

cd /d %~dp0
set scriptName=%1
rem Start the batch script you want to run
start "Options" /B cmd /C "call %scriptName%.bat"

rem Wait for 3 minutes (180 seconds)
timeout /t 180

rem Kill all instances of Google Chrome
taskkill /f /im chrome.exe

rem Kill the batch script using taskkill
taskkill /f /im OpenConsole.exe