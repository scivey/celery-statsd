run:
	go run src/celery_statsd.go --redis-host=localhost --redis-port=6379 --statsd-host=localhost --statsd-port=8125 --queues=celery,sleepy

.PHONY: run build

build:
	go build src/celery_statsd.go
