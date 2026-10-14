#!/bin/sh
set -e
g++ -std=c++17 -O2 -o allsee allsee.cpp
echo "built: ./allsee"
