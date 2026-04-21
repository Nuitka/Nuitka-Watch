# nuitka-project: --mode=standalone

from __future__ import print_function

from textual.app import App
from textual.widgets import Footer, Header, Static


class TextualUsingApp(App):
    def compose(self):
        yield Header()
        yield Static("Textual body", id="body")
        yield Footer()

    def on_ready(self):
        header = self.query_one(Header)
        body = self.query_one(Static)
        footer = self.query_one(Footer)

        print("Header module:", Header.__module__)
        print("Static module:", Static.__module__)
        print("Footer module:", Footer.__module__)
        print(
            "Mounted widgets:",
            ",".join(widget.__class__.__name__ for widget in (header, body, footer)),
        )
        print("Body id:", body.id)

        self.exit()


if __name__ == "__main__":
    TextualUsingApp().run(headless=True)
    print("OK.")
