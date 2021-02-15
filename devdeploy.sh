#!/usr/bin/env bash

rm -fr dist
rm -fr *.egg-info

#bumpversion build --allow-dirty --verbose
python3 -m setup sdist bdist_wheel
python3 -m twine upload --verbose --repository pypi dist/*
