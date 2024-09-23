from multiprocessing.managers import view_type

from fontTools.ttLib import TTFont

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtGui import QFontDatabase, QFont, QStandardItemModel, QStandardItem

from ttfFontViwerForm import Ui_MainWindow

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionOpen_ttf.triggered.connect(self.open_file_dialog)
        self.ui.actionExit.triggered.connect(self.exit_action)

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open TTF File", "", "TTF Files (*.ttf);;All Files (*)")
        print("File  = ", file_name)
        if file_name:
            # Додаємо шрифт до бази даних шрифтів
            font_id = QFontDatabase.addApplicationFont(file_name)

            if font_id != -1:
                # Отримуємо ім'я шрифту
                font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
                print("Font name: ", font_family)

                # Встановлюємо шрифт для таблиці
                font = QFont(font_family)
                self.ui.tableView.setFont(font)
                self.populate_table_with_unicode()

                # Отримуємо підтримувані символи Unicode
                supported_unicode = self.get_supported_unicode_from_ttf(file_name)

                # Виводимо список кодів Unicode
                print(f"Supported Unicode characters in {file_name}:")
                for code in sorted(supported_unicode):
                    print(f"U+{code:04X} : {chr(code)}")  # Виводимо Unicode і відповідний символ

            else:
                print("Failed to load font.")


    def exit_action(self):
        print("exit")
        QApplication.quit()

    def populate_table_with_unicode(self):
        # Create a model for the table
        model = QStandardItemModel()

        # Add column headers (0-9)
        model.setHorizontalHeaderLabels([str(i) for i in range(10)])

        # Populate the table with Unicode symbols
        for row in range(14918):
            row_items = []
            for col in range(10):
                # Calculate the Unicode value: 10 * row + col
                unicode_value = 10 * row + col
                try:
                    # Convert Unicode to character
                    char = chr(unicode_value)
                except ValueError:
                    # If Unicode value is invalid, leave it empty
                    char = ''
                # Add the character to the row
                row_items.append(QStandardItem(char))
            # Append the row to the model
            model.appendRow(row_items)

        # Set the model to the tableView
        self.ui.tableView.setModel(model)

        # Set the width of each column to a fixed value
        for col in range(10):
            self.ui.tableView.setColumnWidth(col, 50)  # Width set to 50 pixels for each column

        # Налаштування для заголовків колонок і рядків (за замовчуванням — системний шрифт)
        self.ui.tableView.horizontalHeader().setFont(QApplication.font())  # Системний шрифт для заголовків колонок
        self.ui.tableView.verticalHeader().setFont(QApplication.font())  # Системний шрифт для заголовків рядків

    def get_supported_unicode_from_ttf(self, ttf_file_path):
        # Відкриваємо шрифт TTF
        font = TTFont(ttf_file_path)

        # Отримуємо таблицю 'cmap', яка містить інформацію про відповідність Unicode кодів гліфам
        cmap = font['cmap']

        # Створюємо множину для унікальних кодів Unicode
        supported_unicode = set()

        # Проходимо через всі підтаблиці cmap і витягуємо коди символів
        for table in cmap.tables:
            if table.isUnicode():
                supported_unicode.update(table.cmap.keys())

        return supported_unicode


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
