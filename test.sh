python -m unittest discover -v

python -m build

python -m twine upload dist/*
