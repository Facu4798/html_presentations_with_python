from html_presentations import (
    Card,
    CodeBlock,
    Grid,
    Image,
    Presentation,
    Slide,
    Table,
    b,
    code,
    h,
    i,
    img,
    link,
    ol,
    p,
    ul,
)


def test_paragraph_helper_and_slide_content_render():
    html = (
        Presentation()
        .withSlide(
            Slide().withContent(
                h("Title", 1),
                p("This is a paragraph."),
                b("bold"),
                i("italic"),
                code("print('hi')"),
                link("Docs", "https://example.com"),
            )
        )
        .to_html()
    )

    assert "<h1>Title</h1>" in html
    assert "<p>This is a paragraph.</p>" in html
    assert "<strong>bold</strong>" in html
    assert "<em>italic</em>" in html
    assert "<code>print('hi')</code>" in html
    assert '<a href="https://example.com">Docs</a>' in html


def test_grid_and_card_rendering():
    html = (
        Presentation()
        .withSlide(
            Slide().withContent(
                Grid(2, 2)
                .withCell(0, 0, Card().withContent(p("First")))
                .withCell(0, 1, p("Second"))
                .withCell(1, 0, CodeBlock("python").withContent("print('x')"))
                .withCell(1, 1, "Final")
            )
        )
        .to_html()
    )

    assert "<div class=\"grid grid-2x2\"" in html
    assert "<div class=\"card\">" in html
    assert "<p>First</p>" in html
    assert "<pre><code class=\"language-python\">print('x')</code></pre>" in html
    assert "Final" in html


def test_list_helpers_and_multiple_slides_render():
    html = (
        Presentation()
        .withSlide(Slide().withContent(h("Agenda", 2), ul(["One", "Two", "Three"])))
        .withSlide(Slide().withContent(ol(["Alpha", "Beta"])))
        .to_html()
    )

    assert html.count("<section") == 2
    assert "<ul>" in html
    assert "<li>One</li>" in html
    assert "<li>Three</li>" in html
    assert "<ol>" in html
    assert "<li>Alpha</li>" in html
    assert "<li>Beta</li>" in html


def test_image_and_table_support():
    html = (
        Presentation()
        .withSlide(
            Slide().withContent(
                h("Gallery", 2),
                img("/images/logo.png", alt="Logo"),
                Table(headers=["Name", "Value"], rows=[["A", 1], ["B", 2]]),
            )
        )
        .to_html()
    )

    assert '<img src="/images/logo.png" alt="Logo"' in html
    assert "<table" in html
    assert "<th>Name</th>" in html
    assert "<th>Value</th>" in html
    assert "<td>A</td>" in html
    assert "<td>2</td>" in html


def test_default_css_theme_is_included():
    html = Presentation().to_html()

    assert "body" in html
    assert ".slide" in html
    assert ".card" in html
    assert ".grid" in html


def test_horizontal_slide_navigation_and_mobile_scroll_support():
    html = Presentation().withSlide(Slide()).withSlide(Slide()).to_html()

    assert ".deck" in html
    assert "scroll-snap-type: x mandatory" in html
    assert "scrollTo" in html
    assert "keydown" in html
    assert "touchstart" in html
    assert "scrollLeft" in html


def test_custom_css_file_is_injected(tmp_path):
    css_file = tmp_path / "custom.css"
    css_file.write_text(".custom-slide { color: red; }\n", encoding="utf-8")

    html = Presentation(css_file=str(css_file)).to_html()

    assert "<style>" in html
    assert ".custom-slide" in html
    assert "color: red" in html
    assert ".deck" in html
    assert "scroll-snap-type: x mandatory" in html


def test_inline_helpers_accept_nested_content():
    html = (
        Presentation()
        .withSlide(
            Slide().withContent(
                p("Start ", b("bold"), " and ", i("italic"), " ", link("docs", "https://example.com"))
            )
        )
        .to_html()
    )

    assert "Start <strong>bold</strong> and <em>italic</em>" in html
    assert '<a href="https://example.com">docs</a>' in html
