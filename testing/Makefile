.env:
	virtualenv .env
	chmod +x .env/bin/activate
	. .env/bin/activate && pip install -r requirements.txt

run-beat:
	. .env/bin/activate && celery beat -A app.conf --loglevel=INFO

run-worker-1:
	. .env/bin/activate && celery worker -A app.conf --loglevel=INFO -Q celery,sleepy -c 8

.PHONY: run-beat run-worker-1
