
## ex00
check in request headers if it's AJAX or not

X-Requested-With: XMLHttpRequest

This header acts as a signal to the server, telling it that the request was initiated by client-side script, not by standard browser navigation.

## ex01
```
./django_venv/bin/python -m daphne d08.asgi:application
```