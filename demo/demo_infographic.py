from html_presentations import Infographic, Page
from html_presentations.elements import Card, CodeBlock, Grid, Table
from html_presentations.functions import b, code, h, img, link, p, ul


def build_infographic(menu_orientation):
    return (
        Infographic(
            css_file="demo/infographic_theme.css",
            title="Product Pulse Infographic",
            menu_orientation=menu_orientation,
        )
        .withPage(
            Page("Overview", id="overview").withContent(
                h("Product Pulse", 1),
                p("A compact view of what shipped, what changed, and where the team is headed."),
                Grid(3, 1)
                .withCell(0, 0, Card().withContent(h("24", 2), p("features shipped")))
                .withCell(0, 1, Card().withContent(h("91%", 2), p("weekly adoption")))
                .withCell(0, 2, Card().withContent(h("4.8/5", 2), p("customer rating"))),
            )
        )
        .withPage(
            Page("Highlights", id="highlights").withContent(
                h("What changed", 1),
                p("The latest release focuses on a faster path from insight to action."),
                ul(
                    [
                        "Navigation is clearer across the core workflow.",
                        "Reports load faster on large datasets.",
                        "Teams can share decisions with a single link.",
                    ]
                ),
                p("Read the ", b("release notes"), " or ", link("open the product tour", "https://example.com"), "."),
            )
        )
        .withPage(
            Page("Details", id="details").withContent(
                h("Release details", 1),
                Table(
                    headers=["Area", "Status", "Signal"],
                    rows=[
                        ["Onboarding", "Improved", "+18% completion"],
                        ["Performance", "Improved", "-32% load time"],
                        ["Sharing", "New", "2.4k links created"],
                    ],
                ),
                Grid(2, 1)
                .withCell(0, 0, Card().withContent(h("Next up", 3), p("More flexible exports and saved views.")))
                .withCell(
                    0,
                    1,
                    CodeBlock("python").withContent(
                        'Infographic(menu_orientation="vertical")'
                    ),
                ),
            )
        )
        .withPage(
            Page("Signal", id="signal").withContent(
                h("The signal", 1),
                p("A page can contain the same reusable elements as a presentation slide."),
                img("https://placehold.co/960x320/e8eefc/26324a?text=Product+Signal", alt="Product signal chart", alignment="center"),
                p(code("Page"), " objects keep the content model simple and composable."),
            )
        )
    )


build_infographic("horizontal").save("demo/demo_infographic_horizontal.html")
build_infographic("vertical").save("demo/demo_infographic_vertical.html")
