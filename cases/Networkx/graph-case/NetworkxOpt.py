# nuitka-project: --standalone
# maybe it's disabled standalone
# nuitka-project: --follow-imports
# nuitka-project: --enable-plugin=no-qt

# Current list of anti-bloat behavior:
# nuitka-project: --noinclude-default-mode=error
# nuitka-project: --noinclude-custom-mode=networkx.testing:error
# nuitka-project: --noinclude-custom-mode=networkx.tests:error
# nuitka-project: --noinclude-custom-mode=numpy.distutils:error
# nuitka-project: --noinclude-custom-mode=matplotlib:nofollow
# nuitka-project: --noinclude-custom-mode=pandas.util.testing:error
# nuitka-project: --noinclude-custom-mode=pandas.testing:error
# nuitka-project: --noinclude-custom-mode=pandas.util._tester:error

from __future__ import print_function

import networkx as nx

g = nx.DiGraph()
g.add_edge(1, 3)
print("OK:", g)

g = nx.MultiDiGraph()
g.add_edge(0, 2)
g.add_edge(2, 1)
g = nx.transitive_reduction(g)

print("OK:", g)
