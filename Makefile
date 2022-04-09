VENV?=venv
PYTHON?=$(shell which python3.7)

.PHONY: run venv remove-venv rebuild-venv clean

run: venv
	$(VENV)/bin/python app.py

venv: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install -Ur requirements.txt
	touch $(VENV)/bin/activate

remove-venv:
	rm -rf $(VENV)

rebuild-venv: remove-venv venv

lint: venv
	$(VENV)/bin/flake8

docker-build:
	docker build . -t automod

docker-run:
	docker run --name automod-dev --env SLACK_BOT_TOKEN -it automod

docker-exec:
	docker exec -it automod-dev bash

clean: remove-venv
