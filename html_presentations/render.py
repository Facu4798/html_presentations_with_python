from html import escape


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
      background: linear-gradient(180deg, #ffffff, #f8fafc);
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
      box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
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
      background: #eef4ff;
    }
    .code-block {
      background: #111827;
      color: #f9fafb;
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

    if presentation.css_file:
        try:
            with open(presentation.css_file, "r", encoding="utf-8") as css:
                custom_css = css.read()
                style = default_style + "\n" + custom_css
        except OSError:
            style = default_style
    else:
        style = default_style

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
