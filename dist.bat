python -m build
python -m twine upload --repository pypi dist/*
rmdir /s /q dist
rmdir /s /q evesso.egg-info