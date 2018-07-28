import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

from PyQt5.QtWebEngineWidgets import QWebEngineView

app = QApplication(sys.argv)

web = QWebEngineView()
web.load(QUrl("http://duckduckgo.com"))
web.show()

sys.exit(app.exec_())
