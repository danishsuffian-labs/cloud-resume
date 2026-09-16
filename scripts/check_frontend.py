from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


class FrontendParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.references = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)

        if "id" in attributes:
            self.ids.add(attributes["id"])

        for name in ("href", "src"):
            if name in attributes:
                self.references.append(attributes[name])


project_root = Path(__file__).resolve().parent.parent
html_file = project_root / "frontend" / "index.html"
html = html_file.read_text(encoding="utf-8")

parser = FrontendParser()
parser.feed(html)

errors = []

for reference in parser.references:
    parts = urlsplit(reference)

    if parts.scheme or parts.netloc:
        continue

    if not parts.path and parts.fragment:
        if parts.fragment not in parser.ids:
            errors.append(f"Missing section: #{parts.fragment}")

    if parts.path:
        target = html_file.parent / parts.path

        if not target.is_file():
            errors.append(f"Missing file: {parts.path}")

if errors:
    for error in errors:
        print(error)
    raise SystemExit(1)

print("Frontend references passed.")
