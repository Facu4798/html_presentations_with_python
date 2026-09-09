from html import escape

from .elements import _validate_alignment


class Slide:
    def __init__(self, css_class=None, id=None, alignment=None):
        self.css_class = css_class
        self.id = id
        self.alignment = _validate_alignment(alignment)
        self.content = []

    def withContent(self, *content):
        for item in content:
            if item is not None:
                self.content.append(item)
        return self

    def addContent(self, *content):
        return self.withContent(*content)

    def add(self, *content):
        return self.withContent(*content)

    def render(self):
        classes = ["slide"]
        if self.css_class:
            classes.append(self.css_class)
        if self.alignment:
            classes.append(f"align-{self.alignment}")
        attrs = f'class="{" ".join(classes)}"'
        if self.id:
            attrs += f' id="{escape(str(self.id), quote=True)}"'

        inner = "".join(
            item.render() if hasattr(item, "render") else str(item) for item in self.content
        )
        return f'<section {attrs}>{inner}</section>'
