setlocal EnableDelayedExpansion

if "%CONDA%" == "" (
    set "%CONDA%"=conda
)

"%CONDA%" config --append channels conda-forge
"%CONDA%" config --append channels https://quasar.codes/conda/

rem %CONDA% remove -y -n orange --all

rem added some spectroscopy dependencies by hand as it is packaged manually
"%CONDA%" create -y -n env python=3.6.* orange3=3.20.1 ^
 quasar=0.3.2 orange-spectroscopy=0.4.4 opusFC=1.2.* extranormal3=0.0.3 ^
 keyring scipy=1.1.* numpy=1.15.* pyqt=5.6.* ^
 scikit-learn=0.20.* spectral ^
 colorcet h5py || exit /b !ERRORLEVEL!
"%CONDA%" list -n env --export --explicit --md5 > env-spec.txt