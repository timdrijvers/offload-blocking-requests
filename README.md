# Offloading blocking requests

This project demonstrates various ways to offload blocking requests in a wsgi style application. Two ways
are demonstrated: offloading using uwsgi threads and nging njs.

The general idea is that some actions can take long to be performed. Instead of making an async API, this project
demonstrates a way to handle blocked requests at scale. Eventually the long request should be split in:
- Initial action, which would start a background process (lets say a Celery task)
- a polling end-point to check if the celery task is done, and return the final result.


# Getting started
Start the application stack.

```
$ docker-compose up
```

The demonstration application is build up of the following containers:
- redis: for storage
- flask: a simple demo application, wrapped with uwsgi
- apipoller: asyncio (Starlette) poller
- nginx: nginx server


# uwsgi offloading
The uwsgi Python binding is used to signal uwsgi from Flask to do a routing offload. This will do a new
upstream call, this time to the apipoller service, to poll for the final result. The initial call will perform a
non-blocking operation, the subsequent poll will wait for the background process to be done.

```
$ curl 'http://localhost:5000/create_uwsgi'
```


# nginx njs offloading
This example shows how to perform the split request scenario using nginx njs scripting.

```
$ curl 'http://localhost:5000/create_nginx
```
