class Slide:
    def __init__(self, css_class=None, id=None):
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

    def render(self):
        classes = ["slide"]
        if self.css_class:
            classes.append(self.css_class)
        attrs = f'class="{" ".join(classes)}"'
        if self.id:
            attrs += f' id="{self.id}"'

        inner = "".join(
            item.render() if hasattr(item, "render") else str(item) for item in self.content
        )
        return f'<section {attrs}>{inner}</section>'
