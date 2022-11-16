#!/bin/sh
python setup.py check
python3 -m pip install --user --upgrade setuptools wheel
python setup.py sdist build
python setup.py bdist_wheel --universal


#twine upload dist/*