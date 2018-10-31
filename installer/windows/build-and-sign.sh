#!/usr/bin/env bash

set -e

INSTALLER="$( cd "$(dirname "$0")/.." ; pwd -P )"
BUILD="$INSTALLER/windows/build"
BASE="$( cd "$(dirname "$0")/../.." ; pwd -P )"
DIST="$BASE/dist"

# Build updated conda package
mkdir -p "$BUILD/conda"
rm -rf "$BUILD/conda"/*

# Manually build orange-spectroscopy that is in the same folder as quasar
SPECTROSCOPY="$( cd "$(dirname "$0")/../../../orange-spectroscopy" ; pwd -P )"
conda build "$SPECTROSCOPY/conda" \
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

# Build new installer
./build-conda-installer.sh \
  --env-spec $NEW_SPEC \
  --online=no \
  --dist-dir $DIST

# Sign the installer
VERSION=$( echo $CONDA_PACKAGE | sed -n 's/.*-\([0-9.]*\)-.*/\1/p' )
signcode \
  -spc ~/Desktop/ulfri.spc \
  -v ~/Desktop/ulfri.pvk \
  -a sha1 \
  -t http://timestamp.verisign.com/scripts/timstamp.dll \
  -n scOrange \
  -i http://singlecell.biolab.si \
  "$DIST/scOrange-$VERSION-Miniconda-x86_64.exe"
