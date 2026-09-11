from .elements import Element, Image, RawHTML, _read_raw_or_file


def h(text, level=1, alignment=None):
    if not 1 <= int(level) <= 6:
        raise ValueError("Heading level must be between 1 and 6")
    return Element(f"h{int(level)}", content=text, alignment=alignment, default_css_class="heading")


def html(*content):
    return RawHTML("".join(_read_raw_or_file(item) for item in content))


def b(*content, alignment=None):
    return Element("strong", content=list(content) if content else [""], alignment=alignment, default_css_class="bold")


def i(*content, alignment=None):
    return Element("em", content=list(content) if content else [""], alignment=alignment, default_css_class="italic")


def code(*content, alignment=None):
    return Element("code", content=list(content) if content else [""], alignment=alignment, default_css_class="inline-code")


def link(display, url, alignment=None):
    return Element("a", content=display, attrs={"href": url}, alignment=alignment, default_css_class="link")


def p(*content, alignment=None):
    return Element("p", content=list(content) if content else [""], alignment=alignment, default_css_class="paragraph")


def img(src, alt="", css_class=None, alignment=None):
    return Image(src, alt=alt, css_class=css_class, alignment=alignment)


def ul(items, alignment=None):
    if items is None:
        return Element("ul", content=[], alignment=alignment, default_css_class="unordered-list")
    values = list(items)
    return Element(
        "ul",
        content=[Element("li", content=str(v), default_css_class="list-item") for v in values],
        alignment=alignment,
        default_css_class="unordered-list",
    )


def ol(items, alignment=None):
    if items is None:
        return Element("ol", content=[], alignment=alignment, default_css_class="ordered-list")
    values = list(items)
    return Element(
        "ol",
        content=[Element("li", content=str(v), default_css_class="list-item") for v in values],
        alignment=alignment,
        default_css_class="ordered-list",
    )
