import os
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QAbstractItemView,
    QHBoxLayout,
    QHeaderView,
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

        # Полные пути выбранных книг
        self.books = []
        # Папка сохранения EPUB по умолчанию
        self.output_folder = (
            Path.home()
            / "Documents"
            / "FB2Kindle"
            / "Output"
        )

        self.output_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.create_ui()

    def create_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        title = QLabel("FB2Kindle")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            padding: 0;
        """)

        subtitle = QLabel("Конвертация книг FB2 → EPUB для Kindle")
        subtitle.setStyleSheet("""
            color: gray;
            padding-bottom: 10px;
        """)

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # ---------- Панель кнопок ----------

        buttons_layout = QHBoxLayout()

        self.add_button = QPushButton("Добавить книги")
        self.remove_button = QPushButton("Удалить")

        self.add_button.clicked.connect(self.add_books)
        self.remove_button.clicked.connect(self.remove_books)

        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.remove_button)
        buttons_layout.addStretch()

        main_layout.addLayout(buttons_layout)

        # ---------- Таблица ----------

        self.books_table = QTableWidget()

        self.books_table.setColumnCount(3)
        self.books_table.setHorizontalHeaderLabels(
            ["Имя книги", "Размер", "Статус"]
        )

        header = self.books_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self.books_table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.books_table.setSelectionMode(
            QAbstractItemView.ExtendedSelection
        )

        self.books_table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        main_layout.addWidget(self.books_table)

        # ---------- Папка сохранения ----------

        folder_layout = QHBoxLayout()

        folder_label = QLabel("Папка сохранения:")

        self.folder_edit = QLineEdit()
        self.folder_edit.setText(str(self.output_folder))

        self.browse_button = QPushButton("Обзор...")
        self.browse_button.clicked.connect(
            self.select_output_folder
        )

        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.folder_edit, 1)
        folder_layout.addWidget(self.browse_button)

        main_layout.addLayout(folder_layout)

        # ---------- Кнопка конвертации ----------

        self.convert_button = QPushButton("Конвертировать")
        self.convert_button.setEnabled(False)

        main_layout.addWidget(self.convert_button)

        # ---------- Журнал ----------

        log_label = QLabel("Журнал работы:")

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        main_layout.addWidget(log_label)
        main_layout.addWidget(self.log)

        self.log.append("FB2Kindle запущен.")

    # ======================================================

    def format_size(self, size: int) -> str:

        if size < 1024:
            return f"{size} B"

        if size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"

        return f"{size / (1024 * 1024):.1f} MB"

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

            self.books_table.setItem(
                row,
                0,
                QTableWidgetItem(Path(file_path).name)
            )

            self.books_table.setItem(
                row,
                1,
                QTableWidgetItem(
                    self.format_size(
                        os.path.getsize(file_path)
                    )
                )
            )

            self.books_table.setItem(
                row,
                2,
                QTableWidgetItem("Ожидание")
            )

            added += 1

        if self.books:
            self.convert_button.setEnabled(True)

        self.log.append(f"Добавлено книг: {added}")

    # ======================================================

    def remove_books(self):

        rows = sorted(
            {
                index.row()
                for index in self.books_table.selectedIndexes()
            },
            reverse=True
        )

        if not rows:
            return

        for row in rows:
            self.books_table.removeRow(row)
            del self.books[row]

        if not self.books:
            self.convert_button.setEnabled(False)

        self.log.append(f"Удалено книг: {len(rows)}")

        self.books_table.clearSelection()

    # ======================================================

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Выберите папку для сохранения EPUB"
        )

        if not folder:
            return

        self.output_folder = Path(folder)

        self.folder_edit.setText(str(self.output_folder))

        self.log.append(
            f"Папка сохранения изменена:\n{self.output_folder}"
        )