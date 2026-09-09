# html-presentations-with-python

A lightweight Python DSL for building HTML presentations.

## Install

Install from a local checkout:

```bash
python -m pip install https://github.com/Facu4798/html_presentations_with_python
```

For development, install the repository in editable mode:

```bash
python -m pip install -e https://github.com/Facu4798/html_presentations_with_python
```

## Quick Start

```python
from html_presentations import Presentation, Slide, h, p

presentation = (
	Presentation()
	.withSlide(Slide().withContent(h("Hello", 1), p("Built with Python.")))
)

presentation.save("presentation.html")
```