from dataclasses import dataclass
import html.parser
import urllib.parse
import requests
import collections

class HTML:
    class BaseNode: pass

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
                lambda e: getattr(e, "tag", "").casefold() == \
                tag_name.casefold(), self.all_children()
            )

    @dataclass
    class Element(ParentNode):
        tag: str
        attrs: dict
        children: list
        
        @property
        def text(self):
            return "".join(
                child.text for child in self.all_children()
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
        VOID_TAGS = {"meta", "br", "hr", "img", "input", "link", "source"}

        def __init__(self):
            super().__init__()
            self._pending_close = collections.deque()
            self._top_level_nodes = []
            self.root = None

        def handle_starttag(self, tag, attrs):
            elmnt = HTML.Element(tag, {k.lower(): v for k, v in attrs}, [])
            if tag in self.VOID_TAGS:
                # Void element: close immediately
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
                self._pending_close[-1].children.append(HTML.Text(text))

        def handle_endtag(self, tag):
            if self._pending_close:
                e = self._pending_close.pop()
                if self._pending_close:
                    self._pending_close[-1].children.append(e)
                else:
                    self._top_level_nodes.append(e)

        def handle_pi(self, data):
            # Split manually into target + data if needed
            parts = data.split(maxsplit=1)
            target = parts[0]
            detail = parts[1] if len(parts) > 1 else ""
            pi = HTML.ProcessingInstruction(target, detail)
            if self._pending_close:
                self._pending_close[-1].children.append(pi)
            else:
                self._top_level_nodes.append(pi)

        def close(self):
            super().close()
            if not self.root:
                self.root = HTML.Document(self._top_level_nodes)

    @staticmethod
    def parse_dom(html_code):
        parser = HTML._Parser()
        parser.feed(html_code)
        parser.close()
        return parser.root
#
VISITED = set()
TO_VISIT = ["https://tiash.is-cool.dev/"]

def crawl():
    for url in TO_VISIT:
        res = requests.get(url)
        doc = HTML.parse_dom(res.text)
        
        for a in doc.select_all("a"):
            if "href" not in a.attrs:
                continue
                
            abs_lk = urllib.parse.urljoin(url, a.attrs["href"])
            
            if urllib.parse.urlsplit(abs_lk).netloc != "tiash.is-cool.dev":
                continue
            
            abs_lk = \
                urllib.parse.urlsplit(abs_lk)._replace(fragment="").geturl()
            
            if abs_lk in VISITED:
                continue
                
            VISITED.add(abs_lk)
            TO_VISIT.append(abs_lk)
            
            print(abs_lk)
#
if __name__ == "__main__": crawl()