# only working on python3.4

from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtWebKit import *


app = QApplication([])

webview = QWebView()
loop = QEventLoop()
webview.loadFinished.connect(loop.quit)
webview.load(QUrl('http://example.webscraping.com/places/ajax/search.json?&search_term=.&page_size=1000&page=0'))
loop.exec_()
webview.show()
frame = webview.page().mainFrame()
frame.findFirstElement('#search_term').setAttribute('value', '.')
frame.findFirstElement('#page_size option:checked').setPlainText('1000')
frame.findFirstElement('#search').evaluateJavaScript('this.click()')
app.exec_()


