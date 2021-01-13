#!/usr/bin/env bash

make clean
sphinx-apidoc -o source ../GenerIter -f
make html
