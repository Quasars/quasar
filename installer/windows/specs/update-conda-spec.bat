setlocal EnableDelayedExpansion

if "%CONDA%" == "" (
    set "%CONDA%"=conda
)

"%CONDA%" config --append channels conda-forge
"%CONDA%" config --append channels https://quasar.codes/conda/

rem %CONDA% remove -y -n orange --all

"%CONDA%" create -y -n env python=3.7.* quasar=0.9.0 ^
 orange3=3.27.1 orange-widget-base=4.10.0 orange-canvas-core=0.1.18 ^
 orange-spectroscopy=0.5.7 opusFC=1.2.* ^
 keyring scipy=1.5.* numpy=1.19.* pyqt=5.12.* ^
 scikit-learn=0.23.* ^
 h5py || exit /b !ERRORLEVEL!
"%CONDA%" list -n env --export --explicit --md5 > env-spec.txt
