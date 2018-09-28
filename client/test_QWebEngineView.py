import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

from PyQt5.QtWebEngineWidgets import QWebEngineView

app = QApplication(sys.argv)

url = "localhost:5000"

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "code/template/login.html"))
local_url = QUrl.fromLocalFile(file_path)

web = QWebEngineView()
web.load(QUrl(url))
web.show()

sys.exit(app.exec_())
