conda config --add channels conda-forge
conda remove -y -n orange --all
REM added some spectroscopy dependencies by hand as it is packaged manually
conda create -y -n orange python=3.6.* orange3=3.18.0 keyring scipy=1.1.0 numpy=1.15.4 scikit-learn=0.20.1 spectral>=0.18 colorcet h5py
conda list -n orange --export --explicit --md5 > conda-spec.txt
