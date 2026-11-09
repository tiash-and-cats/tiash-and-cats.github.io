from dataclasses import dataclass
from pathlib import Path
from collections import deque
import html.parser
import urllib.parse
import requests
import collections
import sys


DOMAIN = "tiash.is-cool.dev"
ROOT_URL = f"https://{DOMAIN}/"
SITE_DIR = Path("_site")

VISITED = set()
TO_VISIT = deque()


def log(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class HTML:
    class BaseNode:
        pass

    class ParentNode(BaseNode):
        def all_children(self):
            def walk(node):
                for child in getattr(node, "children", []):
                    yield child
                    yield from walk(child)
            return walk(self)

        def __iter__(self):
            return iter(self.children)

    @dataclass
    class Document(ParentNode):
        children: list

        def select_all(self, tag_name):
            return filter(
                lambda e: getattr(e, "tag", "").casefold() ==
                tag_name.casefold(),
                self.all_children()
            )

    @dataclass
    class Element(ParentNode):
        tag: str
        attrs: dict
        children: list

        @property
        def text(self):
            return "".join(
                child.text
                for child in self.all_children()
                if isinstance(child, HTML.Text)
            )

        def __getitem__(self, k):
            return self.attrs[k]

        def __setitem__(self, k, v):
            self.attrs[k] = v

    @dataclass
    class Text(BaseNode):
        text: str

    @dataclass
    class Comment(BaseNode):
        text: str

    @dataclass
    class ProcessingInstruction(BaseNode):
        target: str
        data: str

    class _Parser(html.parser.HTMLParser):
        VOID_TAGS = {
            "meta", "br", "hr", "img",
            "input", "link", "source"
        }

        def __init__(self):
            super().__init__()
            self._pending_close = collections.deque()
            self._top_level_nodes = []
            self.root = None

        def handle_starttag(self, tag, attrs):
            elmnt = HTML.Element(
                tag,
                {k.lower(): v for k, v in attrs},
                []
            )

            if tag in self.VOID_TAGS:
                if self._pending_close:
                    self._pending_close[-1].children.append(elmnt)
                else:
                    self._top_level_nodes.append(elmnt)
            else:
                self._pending_close.append(elmnt)

        def handle_comment(self, data):
            comment = HTML.Comment(data)

            if self._pending_close:
                self._pending_close[-1].children.append(comment)
            else:
                self._top_level_nodes.append(comment)

        def handle_data(self, text):
            if self._pending_close and text.strip():
                self._pending_close[-1].children.append(
                    HTML.Text(text)
                )

        def handle_endtag(self, tag):
            if not self._pending_close:
                return

            e = self._pending_close.pop()

            if self._pending_close:
                self._pending_close[-1].children.append(e)
            else:
                self._top_level_nodes.append(e)

        def handle_pi(self, data):
            parts = data.split(maxsplit=1)

            target = parts[0]
            detail = parts[1] if len(parts) > 1 else ""

            pi = HTML.ProcessingInstruction(
                target,
                detail
            )

            if self._pending_close:
                self._pending_close[-1].children.append(pi)
            else:
                self._top_level_nodes.append(pi)

        def close(self):
            super().close()

            if not self.root:
                self.root = HTML.Document(
                    self._top_level_nodes
                )

    @staticmethod
    def parse_dom(html_code):
        parser = HTML._Parser()
        parser.feed(html_code)
        parser.close()
        return parser.root


def normalize_url(url):
    parts = urllib.parse.urlsplit(url)

    return parts._replace(
        scheme="https",
        fragment=""
    ).geturl()


def same_site(url):
    return urllib.parse.urlsplit(url).netloc == DOMAIN


def file_to_url(path):
    rel = path.relative_to(SITE_DIR)

    if rel.name == "index.html":
        rel = rel.parent
    else:
        rel = rel.with_suffix("")

    rel = str(rel).replace("\\", "/")

    if not rel or rel == ".":
        return ROOT_URL

    return urllib.parse.urljoin(
        ROOT_URL,
        rel.rstrip("/") + "/"
    )


def seed_from_build():
    """
    Add all generated pages and links found in them.
    This ensures we operate on the latest _site build,
    then the crawler can discover linked sibling repos.
    """

    discovered = set()

    for page in SITE_DIR.rglob("*.html"):
        page_url = normalize_url(
            file_to_url(page)
        )

        discovered.add(page_url)

        try:
            doc = HTML.parse_dom(
                page.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )
            )
        except Exception as exc:
            log("parse failed:", page, exc)
            continue

        for a in doc.select_all("a"):
            href = a.attrs.get("href")

            if not href:
                continue

            target = normalize_url(
                urllib.parse.urljoin(
                    page_url,
                    href
                )
            )

            if same_site(target):
                discovered.add(target)

    return discovered


def crawl():
    while TO_VISIT:
        url = TO_VISIT.popleft()

        if url in VISITED:
            continue

        VISITED.add(url)

        log("visit", url)

        try:
            res = requests.get(
                url,
                timeout=15,
                headers={
                    "User-Agent":
                    "Tiash Sitemap Generator"
                }
            )
        except Exception as exc:
            log("request failed:", url, exc)
            continue

        ctype = res.headers.get(
            "content-type",
            ""
        ).lower()

        if "html" not in ctype:
            continue

        try:
            doc = HTML.parse_dom(res.text)
        except Exception as exc:
            log("html failed:", url, exc)
            continue

        for a in doc.select_all("a"):
            href = a.attrs.get("href")

            if not href:
                continue

            target = normalize_url(
                urllib.parse.urljoin(
                    url,
                    href
                )
            )

            if not same_site(target):
                continue

            if target not in VISITED:
                TO_VISIT.append(target)


if __name__ == "__main__":
    log("seeding from", SITE_DIR)

    for url in sorted(seed_from_build()):
        TO_VISIT.append(url)

    log("seeded", len(TO_VISIT), "urls")

    crawl()

    log("discovered", len(VISITED), "urls")

    for url in sorted(VISITED):
        print(url)