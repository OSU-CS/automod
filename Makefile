VENV?=venv
PYTHON?=$(shell which python3.7)
PORT?=3000

.PHONY: run venv remove-venv rebuild-venv clean run-with-reload run-ngrok

run: venv
	$(VENV)/bin/python app.py

run-with-reload: venv
	uvicorn app:api --reload --port $(PORT) --log-level debug

run-ngrok:
	ngrok http $(PORT)

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

clean: remove-venv
