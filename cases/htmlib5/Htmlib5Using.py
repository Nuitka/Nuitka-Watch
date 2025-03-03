# nuitka-project: --standalone
# nuitka-project: --include-data-dir={MAIN_DIRECTORY}/data=data

import io
import pathlib
import html5lib


__author__ = "collinwinter@google.com (Collin Winter)"



if __name__ == "__main__":
    filename = pathlib.Path(__file__).parent / "data" / "w3_tr_html5.html"
    with filename.open("rb") as fp:
        html_file = io.BytesIO(fp.read())

    html_file.seek(0)
    html5lib.parse(html_file)
