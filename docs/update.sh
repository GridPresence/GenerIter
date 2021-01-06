#!/usr/bin/env bash

make clean
sphinx-apidoc -o source ../pyrobodj -f
make html
