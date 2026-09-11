from html import escape
from os import PathLike, fspath
from pathlib import Path

VALID_ALIGNMENTS = {"left", "right", "center"}


def _validate_alignment(alignment):
    if alignment is not None and alignment not in VALID_ALIGNMENTS:
        raise ValueError("Alignment must be 'left', 'right', or 'center'")
    return alignment


def _read_raw_or_file(value):
    if isinstance(value, PathLike):
        path = Path(value)
        return path.read_text(encoding="utf-8")
    if isinstance(value, str) and Path(value).is_file():
        return Path(value).read_text(encoding="utf-8")
    return fspath(value) if isinstance(value, PathLike) else str(value)


class Element:
    def __init__(self, tag, content=None, css_class=None, attrs=None, alignment=None):
        self.tag = tag
        self.content = [] if content is None else self._normalize_content(content)
        self.css_class = css_class
        self.attrs = attrs or {}
        self.alignment = _validate_alignment(alignment)

    def _render_class(self):
        classes = []
        if self.css_class:
            classes.append(self.css_class)
        if self.alignment:
            classes.append(f"align-{self.alignment}")
        return " ".join(classes)

    def _normalize_content(self, content):
        if isinstance(content, (list, tuple)):
            items = []
            for item in content:
                items.extend(self._normalize_content(item))
            return items
        if content is None:
            return []
        return [content]

    def withContent(self, *content):
        self.content.extend(self._normalize_content(content))
        return self

    def addContent(self, *content):
        return self.withContent(*content)

    def add(self, *content):
        return self.withContent(*content)

    def render(self):
        attrs = []
        css_class = self._render_class()
        if css_class:
            attrs.append(f'class="{escape(css_class, quote=True)}"')
        for key, value in self.attrs.items():
            attrs.append(f'{key}="{escape(str(value), quote=True)}"')
        attr_str = " " + " ".join(attrs) if attrs else ""
        inner = "".join(self._render_child(item) for item in self.content)
        return f"<{self.tag}{attr_str}>{inner}</{self.tag}>"

    def _render_child(self, item):
        if item is None:
            return ""
        if isinstance(item, str):
            return escape(item, quote=False)
        if hasattr(item, "render"):
            return item.render()
        return escape(str(item), quote=False)


class TextNode(Element):
    def __init__(self, tag, text):
        super().__init__(tag, content=text)


class RawHTML(Element):
    def __init__(self, content):
        self.raw_content = content

    def render(self):
        return self.raw_content


class Card(Element):
    def __init__(self, css_class=None, alignment=None):
        super().__init__("div", css_class=css_class or "card", alignment=alignment)


class Grid(Element):
    def __init__(self, horizontal=1, vertical=1, css_class=None, content=None, alignment=None):
        self.horizontal = max(1, int(horizontal))
        self.vertical = max(1, int(vertical))
        self.cells = {}
        super().__init__(
            "div",
            content=content,
            css_class=(css_class or "grid") + f" grid-{self.horizontal}x{self.vertical}",
            alignment=alignment,
        )

    def withCell(self, row, col, content):
        if row < 0 or col < 0:
            raise ValueError("Grid coordinates must be non-negative")
        new_rows = max(self.vertical, row + 1)
        new_cols = max(self.horizontal, col + 1)
        self.vertical = new_rows
        self.horizontal = new_cols
        self.cells[(row, col)] = content
        self.css_class = "grid" + f" grid-{self.horizontal}x{self.vertical}"
        return self

    def addCell(self, row, col, content):
        return self.withCell(row, col, content)

    def render(self):
        inner = []
        for row in range(self.vertical):
            for col in range(self.horizontal):
                cell_content = self.cells.get((row, col), "")
                inner.append(f'<div class="grid-cell">{self._render_child(cell_content)}</div>')
        style = (
            f'grid-template-columns: repeat({self.horizontal}, minmax(0, 1fr)); '
            f'grid-template-rows: repeat({self.vertical}, minmax(0, 1fr));'
        )
        return (
            f'<div class="{escape(self._render_class(), quote=True)}" '
            f'style="{escape(style, quote=True)}">{"".join(inner)}</div>'
        )


class CodeBlock(Element):
    def __init__(self, language="python", css_class=None, alignment=None):
        self.language = language
        super().__init__("pre", css_class=css_class or "code-block", alignment=alignment)
        self.attrs = {"class": "language-" + language}

    def withContent(self, code_text):
        if isinstance(code_text, str):
            self.content = [code_text]
        else:
            self.content = [str(code_text)]
        return self

    def render(self):
        code = self._render_child(self.content[0]) if self.content else ""
        class_attr = f' class="{escape(self._render_class(), quote=True)}"' if self.alignment else ""
        return (
            f'<pre{class_attr}>'
            f'<code class="language-{escape(self.language, quote=True)}">{code}</code></pre>'
        )


class Image(Element):
    def __init__(self, src, alt="", css_class=None, alignment=None):
        self.src = src
        self.alt = alt
        super().__init__("img", css_class=css_class or "image", alignment=alignment)
        self.attrs = {"src": src, "alt": alt}

    def render(self):
        attrs = [f'src="{escape(str(self.src), quote=True)}"', f'alt="{escape(str(self.alt), quote=True)}"']
        css_class = self._render_class()
        if css_class:
            attrs.append(f'class="{escape(css_class, quote=True)}"')
        return f'<img {" ".join(attrs)} />'


class Table(Element):
    def __init__(self, headers=None, rows=None, css_class=None, alignment=None):
        self.headers = headers or []
        self.rows = rows or []
        super().__init__("table", css_class=css_class or "table", alignment=alignment)

    def render(self):
        header_html = ""
        if self.headers:
            header_html = "<tr>" + "".join(f"<th>{escape(str(h), quote=False)}</th>" for h in self.headers) + "</tr>"

        row_html = ""
        for row in self.rows:
            cells = "".join(f"<td>{escape(str(cell), quote=False)}</td>" for cell in row)
            row_html += f"<tr>{cells}</tr>"

        return f'<table class="{escape(self._render_class(), quote=True)}">{header_html}{row_html}</table>'


