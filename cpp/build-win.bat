@echo off
setlocal
cd /d %~dp0
where g++ >nul 2>nul
if %errorlevel%==0 goto :build
where clang++ >nul 2>nul
if %errorlevel%==0 (
  echo Found clang, building...
  clang++ -std=c++17 -O2 -o AllSee.exe allsee.cpp
  if %errorlevel%==0 (echo built: AllSee.exe & pause & exit /b 0)
)
where cl >nul 2>nul
if %errorlevel%==0 (
  echo Found MSVC, building...
  cl /EHsc /O2 allsee.cpp /FeAllSee.exe
  if %errorlevel%==0 (echo built: AllSee.exe & pause & exit /b 0)
)
echo No C++ compiler found. Installing MinGW via winget...
winget install -e --id BrechtSanders.WinLibs.POSIX.UCRT --accept-source-agreements --accept-package-agreements
if %errorlevel% neq 0 (
  echo INSTALL FAILED. Install manually: https://winlibs.com/ then re-run.
  pause
  exit /b 1
)
echo Close + reopen terminal, then re-run build-win.bat.
pause
exit /b 0
:build
echo Found g++, building...
g++ -std=c++17 -O2 -static -static-libgcc -static-libstdc++ -o AllSee.exe allsee.cpp
if %errorlevel% neq 0 (
  echo BUILD FAILED.
  pause
  exit /b 1
)
echo built: AllSee.exe
pause
