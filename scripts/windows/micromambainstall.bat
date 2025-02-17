@echo off

setlocal EnableDelayedExpansion

rem Target install prefix
set PREFIX=%~1
rem Path to micromamba executable
set MICROMAMBA=%~2

if not exist "%PREFIX%\conda-meta" (
    echo Creating a conda env in "%PREFIX%"
    mkdir "%PREFIX%\conda-meta"
)
if not exist "%PREFIX%\pkgs" (
    mkdir "%PREFIX%\pkgs"
)
call "%MICROMAMBA%" install --yes --root-prefix "%PREFIX%" --prefix "%PREFIX%" --file .\conda-spec.txt ^
        || exit /b !ERRORLEVEL!

rem # Create .condarc file that includes conda-forge channel
rem # We need it so add-ons can be installed from conda-forge
echo Appending conda-forge channel
echo channels:         > "%PREFIX%\.condarc"
echo   - conda-forge  >> "%PREFIX%\.condarc"
echo   - defaults     >> "%PREFIX%\.condarc"

rem Layout a back-compatible conda.bat file that dispatches to micromamba,
rem for add-on dialog logic.
set "CONDA_BAT=%PREFIX%\Scripts\conda.bat"
echo @echo off>                    "%CONDA_BAT%"
echo set "__PREFIX=%%~dp0\..">>     "%CONDA_BAT%"
echo call "%%__PREFIX%%\micromamba" --root-prefix "%%__PREFIX%%" --prefix "%%__PREFIX%%" %%*>>          "%CONDA_BAT%"

rem Initialize activate hook, ...
"%MICROMAMBA%" --root-prefix "%PREFIX%" shell hook -s cmd.exe

rem # install custom sitecustomize module
copy sitecustomize.py "%PREFIX%\Lib\
exit 0