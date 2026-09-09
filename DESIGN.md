# HTML Presentations using Python

This document defines the design for a Python library that builds HTML presentations from declarative Python code. The goal is to provide a fluent, chainable API inspired by PySpark-style builders and expression chains while generating clean HTML and CSS output that can be opened directly in a browser or hosted as a static site.

## 1. Goals

- Create a presentation DSL that feels natural and expressive in Python.
- Allow building slides, grids, cards, text blocks, and code examples with minimal boilerplate.
- Support chained builder-style methods similar to:
  - `Presentation().slide(...).slide(...)`
  - `Grid(2, 2).withCell(0, 0, "A").withCell(1, 1, "B")`
- Keep the generated output easy to inspect and customize.
- Separate content definition from HTML and CSS rendering.
- Support custom CSS files and a default theme.
- Render to a final HTML document with embedded or external CSS.

## 2. Core Design Principles

### 2.1 Fluent API
The library should favor object methods returning `self` so users can chain calls naturally.

Example:

```python
Presentation("styles.css") \
    .withSlide(
        Slide()
            .withContent(
                h("My presentation", 1),
                b("Hello"),
                link("Docs", "https://example.com")
            )
    ) \
    .render()
```

### 2.2 Builder Objects
Each presentation element should be represented as a Python object rather than a raw string. This makes it easier to validate structure, attach CSS classes, and render recursively.

### 2.3 Render Tree
The library will build an internal render tree of nodes. Rendering happens in a final pass that serializes the tree into HTML. This allows layout logic and output generation to stay separate from the user-facing DSL.

### 2.4 Composable Content
Helpers like `h()`, `b()`, `i()`, `code()`, and `link()` should be composable and may be nested inside larger objects.

---

## 3. Package Structure

Proposed package layout:

```text
html_presentations/
    __init__.py
    presentation.py
    slide.py
    elements.py
    render.py
    css.py
    utils.py
```

### 3.1 `presentation.py`
Defines the `Presentation` class.

Responsibilities:
- Store the list of slides.
- Attach CSS configuration.
- Serialize a complete HTML document.
- Expose methods such as `withSlide()`, `render()`, `save()`, and `to_html()`.

### 3.2 `slide.py`
Defines the `Slide` class.

Responsibilities:
- Container for one slide.
- Accept arbitrary content nodes or callables.
- Convert child content into HTML blocks.
- Optionally support slide-specific classes, IDs, and layout options.

### 3.3 `elements.py`
Defines reusable HTML elements and helper functions.

Classes:
- `Grid`
- `Card`
- `CodeBlock`
- `TextBlock`
- `ListBlock`
- `Image`
- `Section`

Helper functions:
- `h(text, level=1)`
- `p(text)`
- `b(text)`
- `i(text)`
- `code(text)`
- `link(display, url)`
- `ul(items)`
- `ol(items)`

### 3.4 `render.py`
Contains the HTML serialization logic.

Responsibilities:
- Traverse the render tree.
- Convert Python objects into HTML strings.
- Escape content safely.
- Render nested elements recursively.

### 3.5 `css.py`
Defines default theme CSS and CSS loader logic.

Responsibilities:
- Provide a default presentation theme.
- Support user-provided CSS file injection.
- Merge custom classes with foundation styles.

### 3.6 `utils.py`
General utilities such as:
- class name normalization
- HTML escaping
- content validation
- string helpers

---

## 4. Public API

## 4.1 Presentation

```python
class Presentation:
    def __init__(self, css_file=None, title="Presentation"):
        ...

    def withSlide(self, slide):
        ...

    def add_slide(self, slide):
        ...

    def render(self):
        ...

    def save(self, filename="presentation.html"):
        ...

    def to_html(self):
        ...
```

### Behavior
- Maintains a list of `Slide` instances.
- Accepts an optional custom CSS file name or stylesheet content.
- Produces a complete HTML document including `<!DOCTYPE html>` and `<html>` tags.
- Can render all slides into a deck container.

## 4.2 Slide

```python
class Slide:
    def __init__(self, css_class=None, id=None):
        ...

    def withContent(self, *content):
        ...

    def add(self, *content):
        ...

    def render(self):
        ...
```

### Behavior
- Holds a list of children.
- Each child may be:
  - a renderable object,
  - a string,
  - a helper function result,
  - a callable that returns content,
  - a nested layout container such as `Grid` or `Card`.

## 4.3 Grid

```python
class Grid:
    def __init__(self, horizontal=1, vertical=1, css_class=None, content=None):
        ...

    def withCell(self, row, col, content):
        ...
```

### Behavior
- Represents a CSS Grid or table-like layout container.
- Accepts a grid shape using `horizontal` and `vertical` dimensions.
- `withCell` assigns content to a given cell coordinate.
- If a specified location is out of range, expand the grid as needed.
- Supports nested content in each cell.

Example:

```python
grid = Grid(2, 2)
   .withCell(0, 0, h("A", 3))
   .withCell(0, 1, Card("highlight").withContent("B"))
   .withCell(1, 0, "C")
   .withCell(1, 1, "D")
```

## 4.4 Card

```python
class Card:
    def __init__(self, css_class=None):
        ...

    def withContent(self, *content):
        ...
```

### Behavior
- Produces a styled container with optional CSS class.
- Useful for emphasis blocks, callouts, summaries, and highlights.

## 4.5 CodeBlock

```python
class CodeBlock:
    def __init__(self, language="python", css_class=None):
        ...

    def withContent(self, code_text):
        ...
```

### Behavior
- Produces a `<pre><code>` block.
- Applies syntax-friendly styling based on the chosen language.
- Accepts raw code strings or a list of lines.

---

## 5. Helper Functions

These functions return lightweight renderable objects rather than raw HTML strings so they can be nested inside containers.

```python
h(text, level=1)
p(text)
b(text)
i(text)
code(text)
link(display, url)
```

### 5.1 `h(text, level)`
Creates a heading element.

- `level` must be between 1 and 6.
- Returns an object that renders as `<hN>text</hN>`.

### 5.2 `p(text)`
Creates a paragraph element for normal body text inside slide content or containers.

### 5.3 `b(text)`
Returns a bold inline element.

### 5.4 `i(text)`
Returns an italic inline element.

### 5.5 `code(text)`
Returns inline code markup.

### 5.6 `link(display, url)`
Returns an anchor element with a display label and URL.

---

## 6. Fluent Usage Examples

### 6.1 Minimal slide

```python
from html_presentations import Presentation, Slide, h, b, link

presentation = Presentation()
presentation.withSlide(
    Slide().withContent(
        h("Hello World", 1),
        b("This is a presentation"),
        link("Read more", "https://example.com")
    )
)

html = presentation.to_html()
```

### 6.2 Chained builder styling

```python
from html_presentations import Presentation, Slide, Grid, Card, CodeBlock, h, code

html = (
    Presentation()
    .withSlide(
        Slide()
            .withContent(
                h("Intro", 2),
                Card("note").withContent("This is a highlight card."),
                Grid(2, 2)
                    .withCell(0, 0, h("Left", 4))
                    .withCell(0, 1, h("Right", 4))
                    .withCell(1, 0, CodeBlock("python").withContent("print('hello')"))
                    .withCell(1, 1, "Footer")
            )
    )
    .to_html()
)
```

### 6.3 Object composition pattern

```python
slide = (
    Slide("cover")
    .withContent(
        h("My talk", 1),
        b("Python + HTML"),
        code("pip install html_presentations")
    )
)
```

---

## 7. Rendering Architecture

The library should follow a simple rendering pipeline:

1. User creates objects in Python.
2. Objects are stored in a tree of renderable nodes.
3. `Presentation.render()` traverses the tree.
4. `render.py` serializes each node to HTML.
5. A final document is assembled with embedded CSS or linked stylesheet.

### 7.1 Node model

A minimal internal model could be:

```python
class Node:
    tag = None
    attrs = {}
    children = []

    def render(self):
        ...
```

This base model allows all content types to be rendered uniformly:
- text nodes
- inline elements
- block elements
- layout containers
- slide wrappers

### 7.2 Escaping and safety
The library should escape text content properly to avoid malformed HTML and unsafe injection. For example:

```python
"<script>alert('x')</script>" -> "&lt;script&gt;alert('x')&lt;/script&gt;"
```

### 7.3 HTML serialization
Rendering will be recursively generated with a function like:

```python
def render_node(node):
    if isinstance(node, str):
        return escape(node)
    return f"<{node.tag} ...>{''.join(render_node(child) for child in node.children)}</{node.tag}>"
```

---

## 8. CSS Strategy

### 8.1 Default theme
Provide a small built-in stylesheet that gives slides a clean, modern, presentation-friendly look.

Example theme features:
- full-page slide layout
- strong typography
- card shadows and borders
- code blocks with monospaced font
- responsive grid support
- accent colors and spacing

### 8.2 Custom CSS support
The `Presentation` class should support either:
- a file path string,
- `None` for default styles,
- inline CSS text if desired later.

Example:

```python
Presentation(css_file="custom.css")
```

### 8.3 Class system
Each element may set a CSS class via `css_class` or `class_name`. The renderer should include class names consistently.

---

## 9. Validation and Edge Cases

The library should validate common misuse early:
- invalid heading levels
- empty slide content
- bad grid coordinates
- invalid child types
- duplicate slide IDs

Suggested policy:
- raise `ValueError` for invalid inputs
- ignore `None` children silently where appropriate
- convert plain strings into text nodes for rendering

---

## 10. Suggested Public API Summary

```python
from html_presentations import (
    Presentation,
    Slide,
    Grid,
    Card,
    CodeBlock,
    h,
    b,
    i,
    code,
    link,
)
```

Common flow:

```python
presentation = Presentation("theme.css")
presentation.withSlide(
    Slide().withContent(
        h("Title", 1),
        Card().withContent("Example content"),
        Grid(2, 2).withCell(0, 0, "A").withCell(0, 1, "B")
    )
)

html = presentation.to_html()
presentation.save("deck.html")
```

---

## 11. Future Enhancements

- Add support for slide transitions and animation classes.
- Add reusable layout templates such as `TitleSlide`, `TwoColumnSlide`, and `AgendaSlide`.
- Add support for images, tables, and lists with richer styling.
- Add syntax highlighting for code blocks.
- Add export to PDF or static site generation.
- Add support for markdown-like input conversion.
- Add slide navigation and presenter notes.

---

## 12. Implementation Recommendation

The initial version should prioritize simplicity and correctness over feature breadth. The best MVP is:

1. `Presentation` + `Slide` + `Grid` + `Card` + `CodeBlock`
2. Helpers for heading, bold, italic, code, and links
3. Recursive HTML serialization
4. Default CSS theme
5. Save/export to HTML file

This is enough to satisfy the core design goal: a Pythonic, chainable API that produces polished HTML presentations from declarative code.

---

## 13. Example Final Output Concept

```python
Presentation("style.css").withSlide(
    Slide().withContent(
        h("Data Engineering Overview", 1),
        b("A quick look at modern pipelines"),
        Grid(2, 2)
            .withCell(0, 0, Card().withContent("Ingestion"))
            .withCell(0, 1, Card().withContent("Storage"))
            .withCell(1, 0, Card().withContent("Processing"))
            .withCell(1, 1, CodeBlock("python").withContent("print('Hello world')"))
    )
).save("presentation.html")
```

This design keeps the library approachable for Python users while producing attractive browser-based decks that feel lightweight and developer-friendly.
