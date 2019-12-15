develop:
	pip install -e .[test]
dist:
	python setup.py sdist bdist_wheel
upload:
	twine upload dist/*
clean:
	rm -rf *.egg-info/ dist/ build/
test:
	pytest -vx
