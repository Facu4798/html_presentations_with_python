from pathlib import Path


THEMES_DIR = Path(__file__).with_name("themes")


def read_theme(theme_name):
    name = str(theme_name).strip()
    if not name:
        raise ValueError("Theme name cannot be empty")

    filename = name if name.endswith(".css") else f"{name}.css"
    theme_path = THEMES_DIR / filename
    if theme_path.parent != THEMES_DIR or not theme_path.is_file():
        raise ValueError(f"Unknown theme: {theme_name}")

    return theme_path.read_text(encoding="utf-8")