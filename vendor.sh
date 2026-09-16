#!/usr/bin/env bash
set -euo pipefail

npmvendor() {
    local name=$1
    local version="${2:-$(npm show "$name" version)}"
    local dir="${3:-assets/vendor/$name}"
    local tarargs="${4:-}"
    
    echo "===== $name"

    local urlname=$(echo "$name" | sed 's/\//%2F/g')
    local pkgname=$(basename "$name")

    mkdir -p "$dir"
    curl -sLf "https://registry.npmjs.org/$urlname/-/$pkgname-$version.tgz" \
      | (tar -vxz -C "$dir" --strip-components=1 package $tarargs || true)
    echo "Please do not worry if it says 'package: not found in archive'."
}

npmvendor three 0.186.0 assets/vendor/threejs "--exclude=package/src"
npmvendor @pmndrs/detect-gpu 6.0.22

echo
echo "done!"