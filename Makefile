.PHONY: validate package test check install-hooks release

validate:
	python3 scripts/validate_skill.py

package: validate
	python3 scripts/build_zip.py

test: package
	python3 -m unittest discover -s tests -v

check: test

install-hooks:
	bash scripts/install_git_hooks.sh

release:
	bash scripts/create_release.sh
