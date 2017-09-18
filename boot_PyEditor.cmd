@echo off

REM ###########################################
REM # PyEditor install helper batch for Windows
REM #
REM # Create a virtualenv
REM # installs PyEditor via pip from PyPi
REM #

title %~0

set BASE_PATH=.\PyEditor
set PIP_ARGS=PyEditor
REM ~ set PIP_ARGS=-e PyEditor

cd /d "%~dp0"

for /f "delims=;" %%i in ('py -V') do set VERSION=%%i
for /f "delims=;" %%i in ('py -3 -V') do set VERSION3=%%i

cls
echo.

if "%VERSION%"=="" (
    echo Sorry, Python 'py' launcher seems not to exist:
    echo.
    echo on
    py -V
    @echo off
    echo.
    echo Please install Python!
    echo.
    pause
    exit
)
echo Python 'py' launcher exists, default version is: %VERSION%

if "%VERSION3%"=="" (
    echo.
    echo ERROR: Python v3 not installed!
    echo.
    pause
    exit
) else (
    echo Python v3 is: %VERSION%
)


echo on
mkdir "%BASE_PATH%"
@echo off
call:test_exist "%BASE_PATH%" "venv not found here:"

echo on
py -3 -m venv "%BASE_PATH%"
@echo off

set SCRIPT_PATH=%BASE_PATH%\Scripts
call:test_exist "%SCRIPT_PATH%" "venv/Script path not found here:"

set ACTIVATE=%SCRIPT_PATH%\activate.bat
call:test_exist "%ACTIVATE%" "venv activate not found here:"

set PYTHON=%SCRIPT_PATH%\python.exe
call:test_exist "%PYTHON%" "python not found here:"

echo on
call "%ACTIVATE%"

set PIP_EXE=%SCRIPT_PATH%\pip.exe
call:test_exist "%PIP_EXE%" "pip not found here:"
echo on
"%PYTHON%" -m pip install -U pip
REM ~ "%PIP_EXE%" install --upgrade wheel
"%PIP_EXE%" install %PIP_ARGS%
@echo off

echo on
explorer.exe %BASE_PATH%
@echo off
pause
exit 0


:test_exist
    if NOT exist "%~1" (
        echo.
        echo ERROR: %~2
        echo.
        echo "%~1"
        echo.
        pause
        exit 1
    )
goto:eof
