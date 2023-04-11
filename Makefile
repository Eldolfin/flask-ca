run:
	docker compose up -d
	flask --app todo_app/app.py run --debug

test:
	python todo_app/test_app.py

default: run
