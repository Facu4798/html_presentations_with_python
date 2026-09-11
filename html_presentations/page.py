from html import escape


class Page:
    def __init__(self, name, css_class=None, id=None):
        self.name = str(name)
        self.css_class = css_class
        self.id = id
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

    def render(self, page_id=None):
        classes = ["page"]
        if self.css_class:
            classes.append(self.css_class)
        attrs = f'class="{escape(" ".join(classes), quote=True)}"'
        rendered_id = self.id if self.id else page_id
        if rendered_id:
            attrs += f' id="{escape(str(rendered_id), quote=True)}"'

        inner = "".join(
            item.render() if hasattr(item, "render") else escape(str(item), quote=False)
            for item in self.content
        )
        return f"<section {attrs}>{inner}</section>"
