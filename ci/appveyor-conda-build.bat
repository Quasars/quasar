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
    "%CONDA%" install --yes conda-build=3.17.8  || exit /b !ERRORLEVEL!
    "%CONDA%" build --python %PYTHON_VERSION% --no-test ../specs/conda-recipe ^
        || exit /b !ERRORLEVEL!

    rem # Copy the build conda pkg to artifacts dir
    rem # and the cache\conda-pkgs which is used later by build-conda-installer
    rem # script

    mkdir ..\conda-pkgs        || exit /b !ERRORLEVEL!
    mkdir ..\cache             || exit /b !ERRORLEVEL!
    mkdir ..\cache\conda-pkgs  || exit /b !ERRORLEVEL!

    for /f %%s in ( '"%CONDA%" build --output --python %PYTHON_VERSION% ../specs/conda-recipe' ) do (
        copy /Y "%%s" ..\conda-pkgs\  || exit /b !ERRORLEVEL!
        copy /Y "%%s" ..\cache\conda-pkgs\  || exit /b !ERRORLEVEL!
    )

    for /f %%s in ( '"%PYTHON%" setup.py --version' ) do (
        set "VERSION=%%s"
    )
) else (
    set "VERSION=%BUILD_COMMIT%"
)

echo VERSION = %VERSION%

if "%CONDA_SPEC_FILE%" == "" (
    "%CONDA%" create -n env --yes --use-local ^
                 python=%PYTHON_VERSION% ^
                 numpy=1.14.* ^
                 scipy=1.1.* ^
                 scikit-learn=0.20.* ^
                 bottleneck=1.2.* ^
                 pyqt=5.6.* ^
                 Orange3=%VERSION% ^
        || exit /b !ERRORLEVEL!

    "%CONDA%" list -n env --export --explicit --md5 > env-spec.txt
    set CONDA_SPEC_FILE=env-spec.txt
)

type "%CONDA_SPEC_FILE%"

bash -e scripts/windows/build-conda-installer.sh ^
        --platform %PLATTAG% ^
        --cache-dir ../cache ^
        --dist-dir dist ^
        --env-spec "%CONDA_SPEC_FILE%" ^
        --online no ^
    || exit /b !ERRORLEVEL!


for %%s in ( dist/Orange3-*Miniconda*.exe ) do (
    set "INSTALLER=%%s"
)

for /f %%s in ( 'sha256sum -b dist/%INSTALLER%' ) do (
    set "CHECKSUM=%%s"
)

echo INSTALLER = %INSTALLER%
echo SHA256    = %CHECKSUM%

@echo on
