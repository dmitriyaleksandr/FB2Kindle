from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FB2Kindle")
        self.resize(900, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        title = QLabel("FB2Kindle")

        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            padding: 20px;
        """)

        layout.addWidget(title)