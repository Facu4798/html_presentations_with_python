import pytest

from html_presentations import Infographic, Page, Presentation, Slide
from html_presentations.elements import (
    Card,
    CodeBlock,
    Grid,
    Image,
    Table,
)
from html_presentations.functions import (
    b,
    code,
    h,
    html,
    i,
    img,
    link,
    ol,
    p,
    ul,
)
from html_presentations.plots import Bar, Box, Hist, Line, Pie


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

    assert '<div class="grid grid-2x2" style="grid-template-columns: repeat(2, minmax(0, 1fr)); grid-template-rows: repeat(2, minmax(0, 1fr));">' in html
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
    assert "height: 100vh" in html
    assert "overflow: hidden" in html


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


def test_alignment_is_supported_by_helpers_and_containers():
    html = (
        Presentation()
        .withSlide(
            Slide(alignment="center").withContent(
                h("Centered", alignment="center"),
                p("Right aligned", alignment="right"),
                Card(alignment="left").withContent("Card"),
                Grid(2, 2, alignment="center"),
                img("/image.png", alignment="right"),
            )
        )
        .to_html()
    )

    assert '<section class="slide align-center">' in html
    assert '<h1 class="align-center">Centered</h1>' in html
    assert '<p class="align-right">Right aligned</p>' in html
    assert '<div class="card align-left">Card</div>' in html
    assert 'class="grid grid-2x2 align-center"' in html
    assert 'class="image align-right"' in html


def test_alignment_rejects_unknown_values():
    with pytest.raises(ValueError, match="Alignment must be"):
        p("Invalid", alignment="justify")


def test_html_helper_accepts_raw_html_and_file_paths(tmp_path):
    html_file = tmp_path / "fragment.html"
    html_file.write_text('<aside class="from-file">File content</aside>', encoding="utf-8")

    rendered = Presentation().withSlide(
        Slide().withContent(html("<div class=\"raw\">Raw content</div>", html_file))
    ).to_html()

    assert '<div class="raw">Raw content</div>' in rendered
    assert '<aside class="from-file">File content</aside>' in rendered


def test_add_script_accepts_mixed_raw_code_and_file_paths(tmp_path):
    script_file = tmp_path / "custom.js"
    script_file.write_text("window.fromFile = true;", encoding="utf-8")

    rendered = Presentation().addScript("window.fromRaw = true;", script_file).to_html()

    assert "window.fromRaw = true;" in rendered
    assert "window.fromFile = true;" in rendered
    assert rendered.count("<script>") >= 3


def test_plot_classes_render_plotly_and_fluent_guides():
    plot = Line({"Jan": [1, 2], "Feb": [2, 4]}).addVLine(10).addHLine(3).setTitle("Trend")

    rendered = Presentation().withSlide(Slide().withContent(plot)).to_html()

    assert 'class="plot-container"' in rendered
    assert "plotly-2.35.2.min.js" in rendered
    assert "Plotly.newPlot" in rendered
    assert '"type":"line"' in rendered
    assert '"x0":10' in rendered
    assert '"y0":3' in rendered
    assert '"title":"Trend"' in rendered


def test_plot_classes_accept_common_data_shapes():
    class DataFrameLike:
        def to_dict(self, orient):
            assert orient == "list"
            return {"score": [2, 5, 3]}

    assert '"type":"bar"' in Bar([1, 2, 3]).render()
    assert '"type":"box"' in Box({"Group A": [1, 2]}).render()
    assert '"type":"histogram"' in Hist(DataFrameLike()).render()
    assert '"labels":["A","B"]' in Pie({"A": 1, "B": 2}).render()


def test_infographic_renders_pages_with_horizontal_menu():
    rendered = (
        Infographic(title="Metrics")
        .withPage(Page("Overview").withContent(h("Overview", 1)))
        .withPage(Page("Details", id="details").withContent(p("More data")))
        .to_html()
    )

    assert '<main class="infographic horizontal">' in rendered
    assert '<nav class="infographic-menu"' in rendered
    assert 'data-page-target="page-0"' in rendered
    assert '>Overview</button>' in rendered
    assert 'data-page-target="details"' in rendered
    assert 'data-page-id="page-0"' in rendered
    assert 'data-page-id="details"' in rendered
    assert "showPage" in rendered


def test_infographic_supports_vertical_menu_and_page_aliases():
    rendered = (
        Infographic(orientation="vertical")
        .page(Page("First").withContent("One"))
        .addPage(Page("Second").withContent("Two"))
        .to_html()
    )

    assert '<main class="infographic vertical">' in rendered
    assert '<section class="page" id="page-0" data-page-id="page-0">One</section>' in rendered
    assert '<section class="page" id="page-1" data-page-id="page-1">Two</section>' in rendered


def test_infographic_rejects_unknown_menu_orientation():
    with pytest.raises(ValueError, match="Menu orientation must be"):
        Infographic(menu_orientation="diagonal")
