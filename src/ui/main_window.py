from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
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

        # Полные пути ко всем выбранным книгам
        self.books = []

        self.create_ui()

    def create_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        title = QLabel("FB2Kindle")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            padding: 10px;
        """)

        main_layout.addWidget(title)

        # ---------- Кнопки ----------

        buttons_layout = QHBoxLayout()

        self.add_button = QPushButton("Добавить книги")
        self.remove_button = QPushButton("Удалить")

        self.add_button.clicked.connect(self.add_books)

        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.remove_button)
        buttons_layout.addStretch()

        main_layout.addLayout(buttons_layout)

        # ---------- Таблица ----------

        self.books_table = QTableWidget()

        self.books_table.setColumnCount(2)
        self.books_table.setHorizontalHeaderLabels(
            ["Имя книги", "Статус"]
        )

        self.books_table.horizontalHeader().setStretchLastSection(True)

        main_layout.addWidget(self.books_table)

        # ---------- Папка сохранения ----------

        folder_layout = QHBoxLayout()

        folder_label = QLabel("Папка сохранения:")

        self.folder_edit = QLineEdit()
        self.folder_edit.setPlaceholderText(
            "Папка для EPUB файлов"
        )

        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.folder_edit)

        main_layout.addLayout(folder_layout)

        # ---------- Кнопка конвертации ----------

        self.convert_button = QPushButton(
            "Конвертировать"
        )

        main_layout.addWidget(self.convert_button)

        # ---------- Журнал ----------

        log_label = QLabel("Журнал работы:")

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        main_layout.addWidget(log_label)
        main_layout.addWidget(self.log)

        self.log.append("FB2Kindle запущен.")

    # ======================================================

    def add_books(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Выберите книги",
            "",
            "FB2 files (*.fb2)"
        )

        if not files:
            return

        added = 0

        for file_path in files:

            if file_path in self.books:
                continue

            self.books.append(file_path)

            row = self.books_table.rowCount()
            self.books_table.insertRow(row)

            file_name = Path(file_path).name

            self.books_table.setItem(
                row,
                0,
                QTableWidgetItem(file_name)
            )

            self.books_table.setItem(
                row,
                1,
                QTableWidgetItem("Ожидание")
            )

            added += 1

        self.log.append(
            f"Добавлено книг: {added}"
        )