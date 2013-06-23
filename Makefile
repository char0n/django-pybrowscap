bootstrap:
	pip install -e . --use-mirrors
	pip install "file://`pwd`#egg=django_pybrowscap" --use-mirrors
	pip install "file://`pwd`#egg=django_pybrowscap[tests]" --use-mirrors

test: bootstrap
	@echo "Running Python tests"
	python setup.py test
	@echo ""

clean:
	rm -rf ./dist
	rm -rf ./django_pybrowscap.egg-info
