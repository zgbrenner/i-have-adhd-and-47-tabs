.PHONY: validate package test check

validate:
	python scripts/validate_skill.py

package: validate
	python scripts/build_zip.py

test: package
	python -m unittest discover -s tests -v

check: test
