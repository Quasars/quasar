#!/usr/bin/env bash

set -e

INSTALLER="$( cd "$(dirname "$0")/.." ; pwd -P )"
BASE="$( cd "$(dirname "$0")/../.." ; pwd -P )"
DIST="$BASE/dist"

# Build new conda package
NEW_SPEC="$BASE/specs/win/conda-spec.txt"

# Build new installer
./build-conda-installer.sh \
  --env-spec $NEW_SPEC \
  --online=no \
  --dist-dir $DIST