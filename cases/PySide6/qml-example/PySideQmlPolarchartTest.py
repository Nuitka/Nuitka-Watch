"""PySide6 port of the QML Polar Chart Example from Qt v5.x"""

# Decide to use either PySide2 or PySide6.
# nuitka-project: --enable-plugin=pyside6

# For standalone, the Qt plugins must be included, and this uses QML so add that too.
# nuitka-project: --standalone
# nuitka-project: --include-qt-plugins=sensible,qml

# Commercial file inclusion vs. free file inclusion.
# nuitka-project: --include-data-dir={MAIN_DIRECTORY}/qmlpolarchart=qmlpolarchart
# nuitka-project-if: {Commercial} is not None:
#   nuitka-project: --embed-data-files-qt-resource-pattern=qmlpolarchart/**
# nuitka-project-if: {OS} == "Windows":
#    nuitka-project: --windows-icon-from-ico={MAIN_DIRECTORY}/qmlpolarchart/Example-Icon.png
# nuitka-project-if: {OS} == "Linux":
#    nuitka-project: --linux-onefile-icon={MAIN_DIRECTORY}/qmlpolarchart/Example-Icon.png
# nuitka-project-if: {OS} == "Darwin":
#    nuitka-project: --macos-app-icon={MAIN_DIRECTORY}/qmlpolarchart/Example-Icon.png
#    nuitka-project: --macos-create-app-bundle
#    nuitka-project: --macos-sign-identity="Nuitka Test Company"

import os
import sys

from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon
from PySide6.QtQuick import QQuickView
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = QQuickView()

    icon_filename = os.path.join(
        os.path.dirname(__file__), "qmlpolarchart/Example-Icon.svg"
    )
    app.setWindowIcon(QIcon(icon_filename))

    viewer.engine().addImportPath(os.path.dirname(__file__))
    viewer.engine().quit.connect(viewer.close)

    viewer.setTitle("QML Polar Chart using %s" % app.__module__)
    qmlFile = os.path.join(os.path.dirname(__file__), "qmlpolarchart/main.qml")
    viewer.setSource(QUrl.fromLocalFile(os.path.abspath(qmlFile)))
    viewer.setResizeMode(QQuickView.SizeRootObjectToView)
    viewer.show()

    sys.exit(app.exec_())
