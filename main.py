import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('http://google.com'))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # Navbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Navigation Buttons
        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # URL Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # Bookmark Button
        bookmark_btn = QAction('Bookmark', self)
        bookmark_btn.triggered.connect(self.add_bookmark)
        navbar.addAction(bookmark_btn)

        # History Button
        history_btn = QAction('History', self)
        history_btn.triggered.connect(self.show_history)
        navbar.addAction(history_btn)

        # Bookmarks Button
        bookmarks_btn = QAction('Bookmarks', self)
        bookmarks_btn.triggered.connect(self.show_bookmarks)
        navbar.addAction(bookmarks_btn)

        # Bookmarks List
        self.bookmarks_list = []

        self.browser.urlChanged.connect(self.update_url)

    def navigate_home(self):
        self.browser.setUrl(QUrl('http://www.onlinegura.com'))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if url.startswith(('http://', 'https://')):
            self.browser.setUrl(QUrl(url))
        else:
            self.browser.setUrl(QUrl('http://' + url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def add_bookmark(self):
        current_url = self.browser.url().toString()
        current_title = self.browser.page().title()
        self.bookmarks_list.append((current_title, current_url))
        QMessageBox.information(self, "Bookmark Added", f"Bookmark added for {current_title}.")

    def show_history(self):
        history_dialog = QDialog(self)
        history_dialog.setWindowTitle('History')
        layout = QVBoxLayout()

        history_list_widget = QListWidget()
        history = self.browser.history()
        for i in range(history.count()):
            history_item = history.itemAt(i)
            if history_item.isValid():
                history_list_widget.addItem(f'{history_item.title()} - {history_item.url().toString()}')

        layout.addWidget(history_list_widget)
        history_dialog.setLayout(layout)
        history_dialog.exec_()

    def show_bookmarks(self):
        bookmark_dialog = QDialog(self)
        bookmark_dialog.setWindowTitle('Bookmarks')
        layout = QVBoxLayout()

        bookmarks_list_widget = QListWidget()
        for title, url in self.bookmarks_list:
            bookmarks_list_widget.addItem(f'{title} - {url}')
        layout.addWidget(bookmarks_list_widget)

        bookmark_dialog.setLayout(layout)
        bookmark_dialog.exec_()


app = QApplication(sys.argv)
QApplication.setApplicationName('Madhushan Browser')
window = MainWindow()
app.exec_()
