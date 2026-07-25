from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FB2Kindle")
        self.resize(1000, 700)

        self.create_ui()

    def create_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Заголовок
        title = QLabel("FB2Kindle")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            padding: 10px;
        """)

        main_layout.addWidget(title)

        # Панель кнопок
        buttons_layout = QHBoxLayout()

        self.add_button = QPushButton("Добавить книги")
        self.remove_button = QPushButton("Удалить")

        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.remove_button)
        buttons_layout.addStretch()

        main_layout.addLayout(buttons_layout)

        # Таблица книг
        self.books_table = QTableWidget()

        self.books_table.setColumnCount(2)
        self.books_table.setHorizontalHeaderLabels(
            ["Файл", "Статус"]
        )

        self.books_table.setRowCount(0)

        main_layout.addWidget(self.books_table)

        # Папка сохранения
        folder_layout = QHBoxLayout()

        folder_label = QLabel("Папка сохранения:")

        self.folder_edit = QLineEdit()
        self.folder_edit.setPlaceholderText(
            "Папка для EPUB файлов"
        )

        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.folder_edit)

        main_layout.addLayout(folder_layout)

        # Кнопка конвертации
        self.convert_button = QPushButton(
            "Конвертировать"
        )

        main_layout.addWidget(
            self.convert_button
        )

        # Журнал
        log_label = QLabel("Журнал работы:")

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        main_layout.addWidget(log_label)
        main_layout.addWidget(self.log)

        self.log.append(
            "FB2Kindle запущен."
        )