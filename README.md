# iFrame-Prototype

No this isn't an iFrame, that's just what this prototype intended to replicate.

Very basic example of serving a local HTML/JS file from QWebEngine, and using QWebChannel to communicate back and forth between JS and python.

Built with Python 3.10 and PySide6.

## Quick Start

1. Create venv

```
python -m venv ./venv
```

2. Update pip

```
python -m pip install --upgrade pip
```

3. Install requirements

```
pip install -r .\requirements.txt
```

4. Launch the application
```
python .\main.py
```
Alternatively there is a VsCode launch.json configured, so you can start debugging with F5 as well.