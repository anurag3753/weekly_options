@echo off

cd /d %~dp0
set PYTHON_ENVIRONMENT=D:\trading\weekly_oprions\venv

"%PYTHON_ENVIRONMENT%\Scripts\activate.bat" & python main.py "NIFTY"