from html_presentations import (
    Presentation, Slide, Grid, Card, CodeBlock,
    h, p, b, i, code, link, ul, img, Table
)

presentation = (
    Presentation("demo/theme.css")
    .withSlide(
        Slide("title-slide").withContent(
            h("Python-Powered Presentation Demo", 1),
            p("A lightweight HTML slide deck built with Python."),
            b("Fluent API"),
            " ",
            i("and reusable components"),
            p(link("Open docs", "https://example.com"))
        )
    )
    .withSlide(
        Slide().withContent(
            h("Agenda", 2),
            ul(["Build slides declaratively", "Compose layout blocks", "Render clean HTML"]),
            p("This deck mixes text, code, cards, and tables.")
        )
    )
    .withSlide(
        Slide().withContent(
            h("Layout Example", 2),
            Grid(2, 2)
                .withCell(0, 0, Card().withContent(h("One", 4), p("Alpha")))
                .withCell(0, 1, Card().withContent(h("Two", 4), p("Beta")))
                .withCell(1, 0, Card().withContent(h("Three", 4), p("Gamma")))
                .withCell(1, 1, CodeBlock("python").withContent("print('hello from slides')"))
        )
    )
    .withSlide(
        Slide().withContent(
            h("Table + Image", 2),
            img("https://placehold.co/600x200/png", alt="Example graphic"),
            Table(
                headers=["Feature", "Status"],
                rows=[
                    ["Text helpers", "OK"],
                    ["Grid layout", "OK"],
                    ["Code blocks", "OK"],
                ],
            ),
        )
    )
)

presentation.save("demo/demo_presentation.html")