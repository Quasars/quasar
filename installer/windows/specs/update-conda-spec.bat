call conda config --add channels conda-forge
call conda remove -y -n orange --all
REM added some spectroscopy dependencies by hand as it is packaged manually
call conda create -y -n orange python=3.6.* orange3=3.20.0 ^
 keyring scipy=1.1.* numpy=1.15.* pyqt=5.6.* ^
 scikit-learn=0.20.* spectral ^
 colorcet h5py
call conda list -n orange --export --explicit --md5 > conda-spec.txt
