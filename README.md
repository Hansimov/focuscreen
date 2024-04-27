# Mouse-Screen

Python script to track mouse and screen-shot nearby area.

## Setup

Generate `requirements.txt`:

```bash
pipreqs . --force --mode no-pin --encoding=utf-8
# remove the line with `opencv-python`
```

Install dependencies:

```bash
pip install -r requirements.txt
```

For windows, to make opencv support GUI:

```bash
pip uninstall opencv-python
pip uninstall opencv-python-headless
pip install opencv-python
```