#!/usr/bin/env bash

set -e

INSTALLER="$( cd "$(dirname "$0")/.." ; pwd -P )"
BUILD="$INSTALLER/windows/build"
BASE="$( cd "$(dirname "$0")/../.." ; pwd -P )"
DIST="$BASE/dist"
OPUSFC="/home/marko/conda-opusfc"
SPECTROSCOPY_BRANCH="0.4.1"

# Build updated conda package
mkdir -p "$BUILD/conda"
rm -rf "$BUILD/conda"/*

rm -rf "$BUILD/spectroscopy"

git clone --single-branch --branch "$SPECTROSCOPY_BRANCH" \
   https://github.com/Quasars/orange-spectroscopy \
   "$BUILD/spectroscopy"

# Manually build orange-spectroscopy that is in the same folder as quasar
conda build "$BUILD/spectroscopy/conda" \
  --output-folder "$BUILD/conda"

conda build "$INSTALLER/conda" \
  --output-folder "$BUILD/conda"

# Build new conda package
NEW_SPEC="$BUILD/conda/conda-spec.txt"
sed '/^file/ d' \
  "$INSTALLER/windows/specs/conda-spec.txt" \
  > $NEW_SPEC
echo "" >> $NEW_SPEC
CONDA_PACKAGE=$( find "$BUILD/conda" \
  -name "quasar*bz2" \
  -exec echo "file://{}" \; )
echo "$CONDA_PACKAGE" >> $NEW_SPEC
CONDA_PACKAGE=$( find "$BUILD/conda" \
  -name "orange-spectroscopy*bz2" \
  -exec echo "file://{}" \; )
echo "$CONDA_PACKAGE" >> $NEW_SPEC
CONDA_PACKAGE=$( find "$OPUSFC" \
  -name "opusfc*py36*bz2" \
  -exec echo "file://{}" \; )
echo "$CONDA_PACKAGE" >> $NEW_SPEC

# Build new installer
./build-conda-installer.sh \
  --env-spec $NEW_SPEC \
  --online=no \
  --dist-dir $DIST


# The following way of signing packages does not work in Windows 10

if false; then
VERSION=$( echo $CONDA_PACKAGE | sed -n 's/.*-\([0-9.]*\)-.*/\1/p' )
signcode \
  -spc ~/Desktop/ulfri.spc \
  -v ~/Desktop/ulfri.pvk \
  -a sha1 \
  -t http://timestamp.verisign.com/scripts/timstamp.dll \
  -n scOrange \
  -i http://singlecell.biolab.si \
  "$DIST/scOrange-$VERSION-Miniconda-x86_64.exe"
fi
