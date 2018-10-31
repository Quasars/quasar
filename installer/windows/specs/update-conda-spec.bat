conda config --add channels conda-forge
conda remove -y -n orange --all
REM added some spectroscopy dependencies by hand as it is packaged manually
conda create -y -n orange python=3.6.* Orange3=3.16.0 keyring scipy=0.19.1 numpy=1.12.1 scikit-learn=0.18.2 spectral>=0.18 colorcet h5py
conda list -n orange --export --explicit --md5 > conda-spec.txt
