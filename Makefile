run:
	docker compose up -d
	venv/bin/flask --app todo_app run --debug

test:
	venv/bin/python test_todo.py

default: run
