# User Guide

`html-presentations-with-python` lets you create HTML slide decks from Python. You build a presentation by composing slides and content elements, then save the result as an HTML file.

This guide describes the public API and the normal workflow for creating presentations.

## Installation

From a local checkout:

```bash
python -m pip install .
```

For development, use editable mode:

```bash
python -m pip install -e .
```

Import the package with:

```python
from html_presentations import Presentation, Slide, h, p
```

## Basic Workflow

A presentation normally follows these steps:

1. Create a `Presentation`.
2. Create one or more `Slide` objects.
3. Add content to each slide.
4. Add the slides to the presentation.
5. Save the presentation as an HTML file.

```python
from html_presentations import Presentation, Slide, h, p

presentation = (
    Presentation(title="My Presentation")
    .withSlide(
        Slide().withContent(
            h("Welcome", 1),
            p("This presentation was created with Python."),
        )
    )
)

presentation.save("presentation.html")
```

Open `presentation.html` in a browser. Slides are arranged horizontally. You can move between them with the left and right arrow keys, swipe on a touch device, or scroll horizontally.

## Presentation

`Presentation` is the deck container.

### Constructor

```python
Presentation(css_file=None, title="Presentation")
```

- `css_file`: Optional path to a custom CSS file. The custom CSS is included in the generated HTML along with the built-in presentation styles.
- `title`: The title placed in the generated HTML document. The default is `"Presentation"`.

### Methods

#### `withSlide(slide)`

Adds a `Slide` to the presentation and returns the same presentation object, allowing method chaining.

```python
presentation.withSlide(Slide().withContent(h("Second slide", 2)))
```

#### `slide(slide)`

Alias for `withSlide`.

```python
presentation.slide(Slide().withContent(p("Another slide")))
```

#### `add_slide(slide)` and `addSlide(slide)`

Additional aliases for `withSlide`.

```python
presentation.add_slide(Slide().withContent(h("Results", 2)))
presentation.addSlide(Slide().withContent(p("Next topic")))
```

#### `to_html()`

Returns the complete presentation as an HTML string.

```python
html = presentation.to_html()
```

#### `render()`

Alias for `to_html()`.

```python
html = presentation.render()
```

#### `save(filename="presentation.html")`

Writes the generated HTML to `filename` and returns the filename.

```python
presentation.save("build/my_deck.html")
```

#### `addScript(*scripts)`

Adds custom JavaScript to the generated document and returns the presentation for chaining. Each argument can be either JavaScript source as a string or a path to a JavaScript file. You can mix both forms in the same call. The source is automatically wrapped in a `<script>` element, so do not include the wrapper tags yourself.

```python
presentation.addScript(
    "document.body.classList.add('ready');",
    "scripts/analytics.js",
)
```

## Slide

`Slide` is a single slide in the deck.

### Constructor

```python
Slide(css_class=None, id=None, alignment=None)
```

- `css_class`: Optional CSS class to add to the slide.
- `id`: Optional HTML `id` attribute.
- `alignment`: Optional text alignment: `"left"`, `"center"`, or `"right"`.

```python
Slide(
    css_class="summary-slide",
    id="summary",
    alignment="center",
)
```

### Methods

#### `withContent(*content)`

Adds one or more content elements to the slide and returns the slide for chaining. Content can include text, headings, paragraphs, cards, grids, tables, images, and other supported elements.

```python
Slide().withContent(
    h("Agenda", 2),
    p("Today we will cover:"),
    ul(["Overview", "Demo", "Questions"]),
)
```

#### `addContent(*content)` and `add(*content)`

Aliases for `withContent`.

```python
slide = Slide().addContent(h("Details", 2))
slide.add(p("More information"))
```

## Content Elements

### Card

`Card` creates a bordered content panel.

```python
Card(css_class=None, alignment=None)
```

- `css_class`: Optional replacement CSS class.
- `alignment`: Optional `"left"`, `"center"`, or `"right"` alignment.

Cards use the same content methods as other elements:

```python
Card(alignment="center").withContent(
    h("Key point", 3),
    p("A short explanation."),
)
```

Available content methods are `withContent(*content)`, `addContent(*content)`, and `add(*content)`. Each returns the card so calls can be chained.

### Grid

`Grid` arranges content in rows and columns.

```python
Grid(horizontal=1, vertical=1, css_class=None, content=None, alignment=None)
```

- `horizontal`: Number of columns.
- `vertical`: Number of rows.
- `css_class`: Optional CSS class prefix.
- `content`: Optional initial content.
- `alignment`: Optional `"left"`, `"center"`, or `"right"` alignment.

Use `withCell(row, column, content)` to place content in a cell. Row and column indexes start at zero.

```python
layout = (
    Grid(2, 2)
    .withCell(0, 0, Card().withContent(h("One", 3), p("Alpha")))
    .withCell(0, 1, Card().withContent(h("Two", 3), p("Beta")))
    .withCell(1, 0, Card().withContent(h("Three", 3), p("Gamma")))
    .withCell(1, 1, Card().withContent(h("Four", 3), p("Delta")))
)
```

#### `withCell(row, col, content)`

Places `content` at the specified zero-based row and column. Returns the grid for chaining.

#### `addCell(row, col, content)`

Alias for `withCell`.

### CodeBlock

`CodeBlock` displays formatted code in a dark code panel.

```python
CodeBlock(language="python", css_class=None, alignment=None)
```

- `language`: Language label used for the code element. The default is `"python"`.
- `css_class`: Optional CSS class.
- `alignment`: Optional `"left"`, `"center"`, or `"right"` alignment.

Use `withContent(code_text)` to set the code shown in the block.

```python
CodeBlock("python").withContent(
    "def greet(name):\n    return f\"Hello, {name}\""
)
```

`withContent` replaces the current code content and returns the code block.

### Image

`Image` represents an image in the presentation. The `img()` helper is usually more convenient.

```python
Image(src, alt="", css_class=None, alignment=None)
```

- `src`: Image URL or path.
- `alt`: Alternative text for accessibility.
- `css_class`: Optional CSS class.
- `alignment`: Optional `"left"`, `"center"`, or `"right"` alignment.

```python
from html_presentations import Image

Image(
    "images/chart.png",
    alt="Monthly sales chart",
    alignment="center",
)
```

### Table

`Table` creates a table with optional column headers and rows.

```python
Table(headers=None, rows=None, css_class=None, alignment=None)
```

- `headers`: A list of column headings.
- `rows`: A list of rows, where each row is a list of cell values.
- `css_class`: Optional CSS class.
- `alignment`: Optional `"left"`, `"center"`, or `"right"` alignment.

```python
Table(
    headers=["Feature", "Status"],
    rows=[
        ["Text helpers", "Ready"],
        ["Grid layout", "Ready"],
        ["Code blocks", "Ready"],
    ],
)
```

## Helper Functions

The helper functions create common HTML content elements.

### `h(text, level=1, alignment=None)`

Creates a heading. `level` must be from 1 through 6.

```python
h("Main title", 1)
h("Section title", 2, alignment="center")
```

### `html(*content)`

Adds custom HTML without escaping it. Each argument can be raw HTML or a path to an HTML fragment file. Multiple raw strings and file paths can be mixed in one call.

```python
from html_presentations import html

custom_content = html(
    '<div class="notice">Inline content</div>',
    "fragments/notice.html",
)
```

Use custom HTML only with content you trust, because it is inserted into the document as provided.

### `p(*content, alignment=None)`

Creates a paragraph. It accepts text and nested elements.

```python
p("Read the ", b("important"), " section first.")
```

### `b(*content, alignment=None)`

Creates bold content.

```python
b("Important")
```

### `i(*content, alignment=None)`

Creates italic content.

```python
i("Optional note")
```

### `code(*content, alignment=None)`

Creates inline code content.

```python
p("Run ", code("python demo.py"), " to generate the deck.")
```

### `link(display, url, alignment=None)`

Creates a link.

```python
link("Project documentation", "https://example.com/docs")
```

### `img(src, alt="", css_class=None, alignment=None)`

Creates an `Image` element.

```python
img("https://placehold.co/800x300/png", alt="Example banner")
```

### `ul(items, alignment=None)`

Creates an unordered list from an iterable of values.

```python
ul(["First item", "Second item", "Third item"])
```

### `ol(items, alignment=None)`

Creates an ordered list from an iterable of values.

```python
ol(["Install the package", "Create slides", "Save the HTML"])
```

## Alignment

The accepted alignment values are:

- `"left"`
- `"center"`
- `"right"`

Alignment can be applied to a slide, a content container, or an individual helper-created element.

```python
Slide(alignment="center").withContent(
    h("Centered title", alignment="center"),
    p("This paragraph is aligned to the right.", alignment="right"),
)
```

An invalid alignment value raises `ValueError`.

## Combining Elements

Elements can be nested to build richer slide content. Inline helpers are especially useful inside paragraphs.

```python
from html_presentations import Slide, b, code, h, link, p

slide = Slide().withContent(
    h("Release checklist", 2),
    p(
        "Read the ",
        b("documentation"),
        ", run ",
        code("pytest"),
        ", and visit ",
        link("the project page", "https://example.com"),
        ".",
    ),
)
```

## Custom Styling

Pass a CSS file to `Presentation` to add a custom theme:

```python
presentation = Presentation(css_file="theme.css", title="Styled deck")
```

The custom stylesheet is included in the generated HTML. You can style the built-in classes such as:

- `.deck`
- `.slide`
- `.title-slide`
- `.grid`
- `.grid-cell`
- `.card`
- `.code-block`
- `.table`
- `.image`
- `.align-left`
- `.align-center`
- `.align-right`

A custom slide class can be added through `Slide(css_class="my-slide")` and styled in the same CSS file.

## Complete Example

```python
from html_presentations import (
    Card,
    CodeBlock,
    Grid,
    Presentation,
    Slide,
    Table,
    h,
    img,
    p,
    ul,
)

presentation = (
    Presentation(
        css_file="theme.css",
        title="Project Overview",
    )
    .withSlide(
        Slide(css_class="title-slide", alignment="center").withContent(
            h("Project Overview", 1),
            p("A presentation generated from Python."),
        )
    )
    .withSlide(
        Slide().withContent(
            h("Agenda", 2),
            ul(["Goals", "Architecture", "Next steps"]),
        )
    )
    .withSlide(
        Slide().withContent(
            h("Highlights", 2),
            Grid(2, 2)
            .withCell(0, 0, Card().withContent(h("Fast", 3), p("Build slides fluently.")))
            .withCell(0, 1, Card().withContent(h("Flexible", 3), p("Compose reusable content.")))
            .withCell(1, 0, CodeBlock().withContent("print('hello')"))
            .withCell(1, 1, img("images/result.png", alt="Result preview")),
        )
    )
    .withSlide(
        Slide().withContent(
            h("Status", 2),
            Table(
                headers=["Area", "Status"],
                rows=[["Slides", "Ready"], ["Themes", "Ready"]],
            ),
        )
    )
)

presentation.save("project_overview.html")
```
