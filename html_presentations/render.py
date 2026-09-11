from html import escape

from .themes import read_theme


def render_node(node):
    if node is None:
        return ""
    if isinstance(node, str):
        return escape(node, quote=False)
    if hasattr(node, "render"):
        return node.render()
    return escape(str(node), quote=False)


def render_document(presentation):
    slides_html = "".join(render_node(slide) for slide in presentation.slides)
    custom_scripts = "".join(f"\n  <script>\n{script}\n  </script>" for script in presentation.scripts)

    default_style = """
    :root {
      --bg: #f4f6fb;
      --panel: #ffffff;
      --ink: #1f2937;
      --muted: #6b7280;
      --border: #dfe7f5;
      --accent: #2563eb;
      --accent-soft: #eef4ff;
      --page-gradient: linear-gradient(180deg, #ffffff, #f8fafc);
      --table-header: #eef4ff;
      --code-bg: #111827;
      --code-ink: #f9fafb;
      --card-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
    }
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      overflow: hidden;
    }
    .deck {
      display: flex;
      flex-direction: row;
      width: 100vw;
      height: 100vh;
      overflow-x: auto;
      overflow-y: hidden;
      scroll-snap-type: x mandatory;
      scroll-behavior: smooth;
      -webkit-overflow-scrolling: touch;
      scrollbar-width: none;
    }
    .deck::-webkit-scrollbar {
      display: none;
    }
    .slide {
      flex: 0 0 100vw;
      width: 100vw;
      height: 100vh;
      box-sizing: border-box;
      padding: 48px;
      overflow: hidden;
      scroll-snap-align: start;
      background: var(--page-gradient);
    }
    .grid {
      display: grid;
      gap: 16px;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    }
    .grid-cell {
      border: 1px solid var(--border);
      padding: 16px;
      background: var(--panel);
      border-radius: 8px;
    }
    .card {
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
      background: var(--panel);
      box-shadow: var(--card-shadow);
    }
    .plot-container {
      width: 100%;
      min-height: 240px;
    }
    .table {
      width: 100%;
      border-collapse: collapse;
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: hidden;
    }
    .table th, .table td {
      padding: 12px 16px;
      border: 1px solid var(--border);
      text-align: left;
    }
    .table th {
      background: var(--table-header);
    }
    .code-block {
      background: var(--code-bg);
      color: var(--code-ink);
      padding: 16px;
      border-radius: 8px;
      overflow-x: auto;
    }
    img.image {
      max-width: 100%;
      border-radius: 8px;
      border: 1px solid var(--border);
    }
    a { color: var(--accent); }
    .align-left { text-align: left; }
    .align-center { align-self: center; }
    .align-right { text-align: right; }
    img.image.align-center { margin-left: auto; margin-right: auto; }
    img.image.align-right { margin-left: auto; margin-right: 0; }
    @media (max-width: 640px) {
      .slide {
        padding: 32px 20px;
      }
      .grid {
        grid-template-columns: 1fr;
      }
    }
    """

    theme_css = read_theme(presentation.theme_name)
    if presentation.css_file:
      try:
        with open(presentation.css_file, "r", encoding="utf-8") as css:
          custom_css = css.read()
          style = default_style + "\n" + theme_css + "\n" + custom_css
      except OSError:
        style = default_style + "\n" + theme_css
    else:
      style = default_style + "\n" + theme_css

    script = """
    <script>
      const deck = document.querySelector('.deck');
      const slides = Array.from(document.querySelectorAll('.slide'));
      let currentIndex = 0;
      let touchStartX = 0;

      function getCurrentIndex() {
        if (!deck || !slides.length) return 0;
        const slideWidth = slides[0].offsetWidth || window.innerWidth;
        return Math.max(0, Math.min(slides.length - 1, Math.round(deck.scrollLeft / slideWidth)));
      }

      function scrollToSlide(index) {
        if (!deck || !slides.length) return;
        const safeIndex = Math.max(0, Math.min(index, slides.length - 1));
        currentIndex = safeIndex;
        deck.scrollTo({ left: slides[safeIndex].offsetLeft, behavior: 'smooth' });
      }

      document.addEventListener('keydown', function(event) {
        const activeIndex = getCurrentIndex();
        if (event.key === 'ArrowRight' || event.key === 'PageDown' || event.key === ' ') {
          event.preventDefault();
          scrollToSlide(activeIndex + 1);
        }
        if (event.key === 'ArrowLeft' || event.key === 'PageUp') {
          event.preventDefault();
          scrollToSlide(activeIndex - 1);
        }
      });

      deck.addEventListener('touchstart', function(event) {
        touchStartX = event.touches[0].clientX;
      }, { passive: true });

      deck.addEventListener('touchend', function(event) {
        const touchEndX = event.changedTouches[0].clientX;
        const diff = touchStartX - touchEndX;
        if (Math.abs(diff) > 50) {
          const activeIndex = getCurrentIndex();
          scrollToSlide(activeIndex + (diff > 0 ? 1 : -1));
        }
      }, { passive: true });

      deck.addEventListener('scroll', function() {
        currentIndex = getCurrentIndex();
      }, { passive: true });
    </script>
    """

    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{escape(presentation.title)}</title>
  <style>{style}</style>
</head>
<body>
  <div class="deck">
    {slides_html}
  </div>
  {script}
  {custom_scripts}
</body>
</html>
"""


def render_infographic(infographic):
    page_ids = [str(page.id) if page.id else f"page-{index}" for index, page in enumerate(infographic.pages)]
    pages_html = "".join(
      page.render(page_ids[index]).replace(
        f'id="{escape(page_ids[index], quote=True)}"',
        f'id="{escape(page_ids[index], quote=True)}" data-page-id="{escape(page_ids[index], quote=True)}"',
        1,
      )
        for index, page in enumerate(infographic.pages)
    )
    menu_html = "".join(
        f'<button type="button" class="page-link{" active" if index == 0 else ""}" '
        f'data-page-target="{escape(page_ids[index], quote=True)}" '
        f'aria-selected="{"true" if index == 0 else "false"}">{escape(page.name)}</button>'
        for index, page in enumerate(infographic.pages)
    )
    custom_scripts = "".join(f"\n  <script>\n{script}\n  </script>" for script in infographic.scripts)

    default_style = """
    :root {
      --bg: #f4f6fb;
      --panel: #ffffff;
      --ink: #1f2937;
      --muted: #6b7280;
      --border: #dfe7f5;
      --accent: #2563eb;
      --accent-soft: #eef4ff;
      --page-gradient: linear-gradient(180deg, #ffffff, #f8fafc);
      --table-header: #eef4ff;
      --code-bg: #111827;
      --code-ink: #f9fafb;
      --card-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
    }
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      background: var(--bg);
      color: var(--ink);
    }
    .infographic {
      display: flex;
      min-height: 100vh;
    }
    .infographic.horizontal {
      flex-direction: column;
    }
    .infographic-menu {
      display: flex;
      background: var(--panel);
      border-color: var(--border);
      border-style: solid;
      gap: 4px;
      padding: 12px;
      box-sizing: border-box;
    }
    .infographic.horizontal .infographic-menu {
      flex-direction: row;
      border-width: 0 0 1px;
      overflow-x: auto;
    }
    .infographic.vertical .infographic-menu {
      flex-direction: column;
      flex: 0 0 220px;
      border-width: 0 1px 0 0;
    }
    .page-link {
      border: 0;
      border-radius: 4px;
      background: transparent;
      color: var(--muted);
      cursor: pointer;
      font: inherit;
      padding: 10px 14px;
      text-align: left;
      white-space: nowrap;
    }
    .page-link:hover,
    .page-link.active {
      background: var(--accent-soft);
      color: var(--accent);
    }
    .infographic-content {
      flex: 1;
      min-width: 0;
    }
    .page {
      box-sizing: border-box;
      display: none;
      min-height: 100vh;
      padding: 48px;
      background: var(--page-gradient);
    }
    .page.active {
      display: block;
    }
    .grid {
      display: grid;
      gap: 16px;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    }
    .grid-cell {
      border: 1px solid var(--border);
      padding: 16px;
      background: var(--panel);
      border-radius: 8px;
    }
    .card {
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
      background: var(--panel);
      box-shadow: var(--card-shadow);
    }
    .table {
      width: 100%;
      border-collapse: collapse;
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: hidden;
    }
    .table th, .table td {
      padding: 12px 16px;
      border: 1px solid var(--border);
      text-align: left;
    }
    .table th {
      background: var(--table-header);
    }
    .code-block {
      background: var(--code-bg);
      color: var(--code-ink);
      padding: 16px;
      border-radius: 8px;
      overflow-x: auto;
    }
    img.image {
      max-width: 100%;
      border-radius: 8px;
      border: 1px solid var(--border);
    }
    a { color: var(--accent); }
    .align-left { text-align: left; }
    .align-center { align-self: center; }
    .align-right { text-align: right; }
    @media (max-width: 640px) {
      .infographic.vertical .infographic-menu {
        flex-basis: 160px;
      }
      .page {
        padding: 32px 20px;
      }
      .grid {
        grid-template-columns: 1fr;
      }
    }
    """

    theme_css = read_theme(infographic.theme_name)
    if infographic.css_file:
        try:
            with open(infographic.css_file, "r", encoding="utf-8") as css:
                style = default_style + "\n" + theme_css + "\n" + css.read()
        except OSError:
            style = default_style + "\n" + theme_css
    else:
        style = default_style + "\n" + theme_css

    script = """
    <script>
      const pageLinks = Array.from(document.querySelectorAll('.page-link'));
      const pages = Array.from(document.querySelectorAll('.page'));

      function showPage(pageId) {
        pages.forEach(function(page) {
          page.classList.toggle('active', page.dataset.pageId === pageId);
        });
        pageLinks.forEach(function(link) {
          const selected = link.dataset.pageTarget === pageId;
          link.classList.toggle('active', selected);
          link.setAttribute('aria-selected', selected ? 'true' : 'false');
        });
      }

      pageLinks.forEach(function(link) {
        link.addEventListener('click', function() {
          showPage(link.dataset.pageTarget);
        });
      });

      if (pageLinks.length) showPage(pageLinks[0].dataset.pageTarget);
    </script>
    """

    orientation = escape(infographic.menu_orientation, quote=True)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(infographic.title)}</title>
  <style>{style}</style>
</head>
<body>
  <main class="infographic {orientation}">
    <nav class="infographic-menu" aria-label="Infographic pages">
      {menu_html}
    </nav>
    <div class="infographic-content">
      {pages_html}
    </div>
  </main>
  {script}
  {custom_scripts}
</body>
</html>
"""
