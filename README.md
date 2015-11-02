## celery-statsd

A Go daemon that monitors celery queue depths.

### Running

```bash
celery_statsd --redis-host=localhost --redis-port=6379 --statsd-host=localhost --statsd-port=8125 --queues=celery,backups,long_running_jobs --interval=1000
```
Or:
```bash
celery_statsd --help
```

### Building

```bash
make build
```
