update-deps:
	pip-compile --upgrade --generate-hashes --output-file requirements.txt requirements.in

init:
	pip install --upgrade -r requirements.txt

install:
	pip install pip-tools

update: install update-deps init

.PHONY: update-deps init update