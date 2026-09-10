#!/bin/sh

echo "===== three.js ================================"
mkdir -p assets/vendor/threejs
curl https://registry.npmjs.org/three/-/three-0.186.0.tgz | tar -vxz -C assets/vendor/threejs --strip-components=1 --exclude="package/src" package
echo "Please do not worry if it says 'package: not found in archive'."

echo
echo "done!"