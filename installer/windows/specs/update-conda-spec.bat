setlocal EnableDelayedExpansion

if "%CONDA%" == "" (
    set "%CONDA%"=conda
)

"%CONDA%" config --append channels conda-forge
"%CONDA%" config --append channels https://quasar.codes/conda/

rem %CONDA% remove -y -n orange --all

"%CONDA%" create -y -n env python=3.6.* quasar=0.9.0 ^
 orange3=3.26.0 orange-spectroscopy=0.5.4 opusFC=1.2.* ^
 keyring scipy=1.2.* numpy=1.16.* pyqt=5.12.* ^
 scikit-learn=0.22.* ^
 colorcet h5py || exit /b !ERRORLEVEL!
"%CONDA%" list -n env --export --explicit --md5 > env-spec.txt
