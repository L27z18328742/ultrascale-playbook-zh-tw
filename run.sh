#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/webapp"
exec python3 -m http.server 8643
