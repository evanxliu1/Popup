@echo off
REM Build DesktopNoti as a Windows EXE using PyInstaller
REM Usage: build_windows.bat

REM Clean previous build
rmdir /S /Q dist
rmdir /S /Q build
del DesktopNoti.spec

REM Build with PyInstaller
pyinstaller ^
  --windowed ^
  --name DesktopNoti ^
  --icon assets\app_icon.ico ^
  --add-data "config\\config.json;config" ^
  --add-data "config\\credentials.json;config" ^
  --add-data "config\\token.json;config" ^
  --add-data "assets\\icon_1024.png;assets" ^
  notification\main.py

if exist dist\DesktopNoti.exe (
  echo DesktopNoti.exe created!
) else (
  echo Build failed: .exe not found.
  exit /b 1
)
