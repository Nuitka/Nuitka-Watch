# nuitka-project: --standalone
from genshi.template import MarkupTemplate, NewTextTemplate


BIGTABLE_XML = """\
<table xmlns:py="http://genshi.edgewall.org/">
<tr py:for="row in table">
<td py:for="c in row.values()" py:content="c"/>
</tr>
</table>
"""

BIGTABLE_TEXT = """\
<table>
{% for row in table %}<tr>
{% for c in row.values() %}<td>$c</td>{% end %}
</tr>{% end %}
</table>
"""


if __name__ == "__main__":
    to_test = {
        "xml": (MarkupTemplate, BIGTABLE_XML),
        "text": (NewTextTemplate, BIGTABLE_TEXT),
    }

    table = [
        dict(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, j=10) for _ in range(1000)
    ]

    for template_name, (tmpl_cls, tmpl_str) in to_test.items():
        tmpl = tmpl_cls(tmpl_str)
        stream = tmpl.generate(table=table)
        stream.render()
