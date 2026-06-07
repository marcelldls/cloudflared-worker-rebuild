from pathlib import Path
from shutil import copy2, rmtree

DEPS = Path(__file__).parent / "modules"
TARGET = Path(__file__).parent / "dist"
TEMPLATES = Path(__file__).parent / "templates"


def fetch_and_build():

    if TARGET.exists():
        rmtree(TARGET)
    TARGET.mkdir()
    copy2(DEPS / "index.global.js", TARGET / "index.global.js")
    copy2(TEMPLATES / "index.html", TARGET / "index.html")


if __name__ == "__main__":
    fetch_and_build()
