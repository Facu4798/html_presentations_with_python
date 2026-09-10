from .elements import _read_raw_or_file
from .render import render_document


class Presentation:
    def __init__(self, css_file=None, title="Presentation"):
        self.css_file = css_file
        self.title = title
        self.slides = []
        self.scripts = []

    def withSlide(self, slide):
        self.slides.append(slide)
        return self

    def slide(self, slide):
        return self.withSlide(slide)

    def add_slide(self, slide):
        return self.withSlide(slide)

    def addSlide(self, slide):
        return self.withSlide(slide)

    def addScript(self, *scripts):
        self.scripts.extend(_read_raw_or_file(script) for script in scripts)
        return self

    def to_html(self):
        return render_document(self)

    def render(self):
        return self.to_html()

    def save(self, filename="presentation.html"):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.to_html())
        return filename
