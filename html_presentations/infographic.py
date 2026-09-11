from .elements import _read_raw_or_file
from .render import render_infographic


class Infographic:
    def __init__(self, css_file=None, title="Infographic", menu_orientation="horizontal", orientation=None):
        if orientation is not None:
            menu_orientation = orientation
        if menu_orientation not in {"horizontal", "vertical"}:
            raise ValueError("Menu orientation must be 'horizontal' or 'vertical'")

        self.css_file = css_file
        self.title = title
        self.menu_orientation = menu_orientation
        self.pages = []
        self.scripts = []

    def withPage(self, page):
        self.pages.append(page)
        return self

    def page(self, page):
        return self.withPage(page)

    def add_page(self, page):
        return self.withPage(page)

    def addPage(self, page):
        return self.withPage(page)

    def addScript(self, *scripts):
        self.scripts.extend(_read_raw_or_file(script) for script in scripts)
        return self

    def to_html(self):
        return render_infographic(self)

    def render(self):
        return self.to_html()

    def save(self, filename="infographic.html"):
        with open(filename, "w", encoding="utf-8") as file:
            file.write(self.to_html())
        return filename
