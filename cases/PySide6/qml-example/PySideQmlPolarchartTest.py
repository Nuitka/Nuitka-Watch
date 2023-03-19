"""PySide2/PySide6 port of the QML Polar Chart Example from Qt v5.x"""

# Decide to use either PySide2 or PySide6.
# nuitka-project-if: "pyside2" in os.getenv("TEST_VARIANT", "standalone,pyside2,commercial").lower().split(","):
#   nuitka-project: --enable-plugin=pyside2
# nuitka-project-if: "pyside6" in os.getenv("TEST_VARIANT", "standalone,pyside2,commercial").lower().split(","):
#   nuitka-project: --enable-plugin=pyside6

# For standalone, the Qt plugins must be included, and this uses QML so add that too.
# nuitka-project-if: "standalone" in os.getenv("TEST_VARIANT", "standalone,pyside2,commercial").split(","):
#   nuitka-project: --standalone
#   nuitka-project: --include-qt-plugins=sensible,qml

# Commercial file inclusion vs. free file inclusion.
# nuitka-project: --include-data-dir={MAIN_DIRECTORY}/qmlpolarchart=qmlpolarchart
# nuitka-project-if: "commercial" in os.getenv("TEST_VARIANT", "standalone,pyside2,commercial").split(","):
#   nuitka-project: --embed-data-files-qt-resource-pattern=qmlpolarchart/**
# nuitka-project-if: {OS} == "Windows":
#    nuitka-project: --windows-icon-from-ico={MAIN_DIRECTORY}/qmlpolarchart/Example-Icon.png
# nuitka-project-if: {OS} == "Linux":
#    nuitka-project: --linux-onefile-icon={MAIN_DIRECTORY}/qmlpolarchart/Example-Icon.png
# nuitka-project-if: {OS} == "Darwin":
#    nuitka-project: --macos-app-icon={MAIN_DIRECTORY}/qmlpolarchart/Example-Icon.png
#    nuitka-project: --macos-create-app-bundle
#    nuitka-project: --macos-sign-identity="Nuitka Test"
#    nuitka-project-if: "pyside2" in os.getenv("TEST_VARIANT", "standalone,pyside2,commercial").split(","):
#       nuitka-project: --onefile

# Avoid options-nanny to complain, we want to see errors easily. Do not do this
# for normal GUI deployments of course.
# nuitka-project: --enable-console

import os
import sys

try:
    from PySide2.QtCore import QUrl
    from PySide2.QtGui import QIcon
    from PySide2.QtQuick import QQuickView
    from PySide2.QtWidgets import QApplication
except ImportError:
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
