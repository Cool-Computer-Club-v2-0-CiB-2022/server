# Cool Computer Club v2.0 CiB 2022 Prototype Server

Cool Computer Club v2.0's server side prototype system for CiB week 2022

## [API Reference](https://github.com/Cool-Computer-Club-v2-0-CiB-2022/server/blob/main/APIReference.md)

Documentation on all of the API endpoints can be found in [`APIReference.md`](https://github.com/Cool-Computer-Club-v2-0-CiB-2022/server/blob/main/APIReference.md)

## Usage

To start the server run:

`./server.py`

The default host is `0.0.0.0` and port is `80` and you can change it with the `--host` and `-port`:

`./server.py --host 127.0.0.1 --port 8080`

Data is stored in `.` and this can be changed with `--data-dir`:

`./server.py --data-dir /path/to/data/directory/`

By default waitress will be used as the WSGI if it is installed and will use werkzeug (the built-in WSGI) if it isn't. To force the server to only use werkzeug add the `--werkzeug` argument:

`./server.py --werkzeug`

To stop the server send a KeyboardInterrupt (ctrl + C).

## Dependencies

- Python 3.7+
- Flask
- Waitress (optional; werkzeug will be used if not installed)

## Misc

- Server tested with Python 3.10.4 on Linux
