from .elements import Element, Image, RawHTML, _read_raw_or_file


def h(text, level=1, alignment=None):
    if not 1 <= int(level) <= 6:
        raise ValueError("Heading level must be between 1 and 6")
    return Element(f"h{int(level)}", content=text, alignment=alignment)


def html(*content):
    return RawHTML("".join(_read_raw_or_file(item) for item in content))


def b(*content, alignment=None):
    return Element("strong", content=list(content) if content else [""], alignment=alignment)


def i(*content, alignment=None):
    return Element("em", content=list(content) if content else [""], alignment=alignment)


def code(*content, alignment=None):
    return Element("code", content=list(content) if content else [""], alignment=alignment)


def link(display, url, alignment=None):
    return Element("a", content=display, attrs={"href": url}, alignment=alignment)


def p(*content, alignment=None):
    return Element("p", content=list(content) if content else [""], alignment=alignment)


def img(src, alt="", css_class=None, alignment=None):
    return Image(src, alt=alt, css_class=css_class, alignment=alignment)


def ul(items, alignment=None):
    if items is None:
        return Element("ul", content=[], alignment=alignment)
    values = list(items)
    return Element("ul", content=[Element("li", content=str(v)) for v in values], alignment=alignment)


def ol(items, alignment=None):
    if items is None:
        return Element("ol", content=[], alignment=alignment)
    values = list(items)
    return Element("ol", content=[Element("li", content=str(v)) for v in values], alignment=alignment)
