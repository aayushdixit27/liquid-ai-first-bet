#!/bin/bash
# Builds llama.cpp for the Modalix board's Debian 12, in a Linux container on this Mac.
# The ready-made arm64 download needs GLIBC 2.38 and the board should have 2.36, so it won't run.
# Takes about 5 minutes. Output: .cache/board/llama-server
set -e
cd "$(dirname "$0")/.."
export DOCKER_HOST="unix://$HOME/.colima/default/docker.sock"
docker run --rm -v "$PWD/.cache/board:/out" debian:12 bash -c '
set -e
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq && apt-get install -y -qq git cmake g++ make ca-certificates >/dev/null
git clone -q --depth 1 --branch b12128 https://github.com/ggml-org/llama.cpp /src
cd /src
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF -DGGML_NATIVE=OFF \
  -DGGML_CPU_ARM_ARCH=armv8.2-a+dotprod -DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_EXAMPLES=OFF \
  -DLLAMA_BUILD_SERVER=ON -DCMAKE_EXE_LINKER_FLAGS="-static-libgcc -static-libstdc++" >/dev/null
cmake --build build -j8 --target llama-server
cp build/bin/llama-server /out/
/out/llama-server --version | head -1
'
ls -la .cache/board/llama-server
