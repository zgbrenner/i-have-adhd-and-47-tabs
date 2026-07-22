.PHONY: validate package test check

validate:
	python3 scripts/validate_skill.py

package: validate
	python3 scripts/build_zip.py

test: package
	python3 -m unittest discover -s tests -v

check: test
