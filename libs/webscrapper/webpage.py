"""
USAGE
# generate some test urls
urls = []
url = 'http://pyqt.sourceforge.net/Docs/PyQt5/%s.html'
for name in dir(QtWebEngineWidgets):
    if name.startswith('Q'):
        urls.append(url % name.lower())


app = QtWidgets.QApplication(sys.argv)
webpage = WebPage()
webpage.start(urls)
sys.exit(app.exec_())
"""

import sys
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor

class RequestInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, parent=None):
        super().__init__(parent)

    def interceptRequest(self, info):
        info.setHttpHeader("X-Frame-Options", "ALLOWALL")
        info.setHttpHeader("User-Agent", "Mozilla/5.0")
        print(info.requestUrl())

class WebPage(QtWebEngineWidgets.QWebEnginePage):
    def __init__(self):
        super(WebPage, self).__init__()
        self.profile().setRequestInterceptor(RequestInterceptor())
        self.loadFinished.connect(self.handleLoadFinished)

    def start(self, urls):
        self._urls = iter(urls)
        self.current_url = ""
        self.fetchNext()

    def fetchNext(self):
        try:
            url = next(self._urls)
            self.current_url = url
        except StopIteration:
            return False
        else:
            self.load(QtCore.QUrl(url))
        return True

    def processCurrentPage(self, html):
        url = self.url().toString()
        # do stuff with html...
        print('loaded: [%d chars] %s' % (len(html), url))
        if not self.fetchNext():
            QtWidgets.qApp.quit()

    def handleLoadFinished(self):
        self.toHtml(self.processCurrentPage)
