# html-presentations-with-python

A lightweight Python DSL for building HTML presentations.

See the [User Guide](USER_GUIDE.md) for the complete public API reference and usage examples.

## Install

Install from a local checkout:

```bash
python -m pip install "git+https://github.com/Facu4798/html_presentations_with_python.git"
```

For development, clone the repository and install it in editable mode:

```bash
git clone https://github.com/Facu4798/html_presentations_with_python.git
cd html_presentations_with_python
python -m pip install -e .
```

The plain GitHub webpage URL cannot be passed directly to `pip`; it downloads an HTML page rather than a Python package archive. The `git+https://` prefix tells `pip` to install from the Git repository.

## Quick Start

```python
from html_presentations import Presentation, Slide, h, p

presentation = (
	Presentation()
	.withSlide(Slide().withContent(h("Hello", 1), p("Built with Python.")))
)

presentation.save("presentation.html")
```