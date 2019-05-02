@echo off
setlocal EnableDelayedExpansion

if "%PYTHON_VERSION%" == "" (
    echo PYTHON_VERSION must be defined >&2
    exit /b 1
)

if  "%PLATTAG%" == "" (
    echo Missing PLATTAG variable >&2
    exit /b 1
)

"%CONDA%" config --append channels conda-forge  || exit /b !ERRORLEVEL!

if not "%BUILD_LOCAL%" == "" (
    rem # Disabled local builds
) else (
    set "VERSION=%BUILD_COMMIT%"
)

echo VERSION = %VERSION%

if "%CONDA_SPEC_FILE%" == "" (
    call installer/windows/specs/update-conda-spec.bat || exit /b !ERRORLEVEL!
    set CONDA_SPEC_FILE=env-spec.txt
)

type "%CONDA_SPEC_FILE%"

bash -e installer/windows/build-conda-installer.sh ^
        --platform %PLATTAG% ^
        --cache-dir ../cache ^
        --dist-dir dist ^
        --env-spec "%CONDA_SPEC_FILE%" ^
        --online no ^
    || exit /b !ERRORLEVEL!


for %%s in ( dist/Quasar-*Miniconda*.exe ) do (
    set "INSTALLER=%%s"
)

for /f %%s in ( 'sha256sum -b dist/%INSTALLER%' ) do (
    set "CHECKSUM=%%s"
)

echo INSTALLER = %INSTALLER%
echo SHA256    = %CHECKSUM%

@echo on
