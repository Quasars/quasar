setlocal EnableDelayedExpansion

if "%CONDA%" == "" (
    set "%CONDA%"=conda
)

"%CONDA%" config --append channels conda-forge
"%CONDA%" config --append channels https://quasar.codes/conda/

rem %CONDA% remove -y -n orange --all

"%CONDA%" create -y -n env python=3.6.* quasar=0.6.0 ^
 orange3=3.23.0 orange-spectroscopy=0.4.6 opusFC=1.2.* ^
 keyring scipy=1.2.* numpy=1.16.* pyqt=5.9.* ^
 scikit-learn=0.21.* ^
 colorcet h5py || exit /b !ERRORLEVEL!
"%CONDA%" list -n env --export --explicit --md5 > env-spec.txt