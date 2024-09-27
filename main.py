from fontTools.ttLib import TTFont
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QTableWidget
from PyQt6.QtGui import QFontDatabase

from ttfFontViwerForm import Ui_MainWindow

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Змінюємо tableView на tableWidget для можливості використання QLabel у комірках
        self.ui.tableWidget = QTableWidget(self)
        self.ui.tableWidget.setGeometry(self.ui.tableView.geometry())  # Використовуємо ті ж розміри, що й у tableView
        self.setCentralWidget(self.ui.tableWidget)  # Замінюємо основний віджет

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

                # Встановлюємо шрифт для символів
                self.font_ttf = font_family

                # Отримуємо підтримувані символи Unicode
                supported_unicode = self.get_supported_unicode_from_ttf(file_name)

                # Оновлюємо таблицю підтримуваними символами
                self.populate_table_with_unicode(supported_unicode)

            else:
                print("Failed to load font.")

    def exit_action(self):
        print("exit")
        QApplication.quit()

    def populate_table_with_unicode(self, supported_unicode):
        # Очищаємо таблицю перед заповненням
        self.ui.tableWidget.clear()

        # Встановлюємо кількість колонок і рядків
        self.ui.tableWidget.setColumnCount(10)
        self.ui.tableWidget.setRowCount((len(supported_unicode) + 9) // 10)

        # Сортуємо список підтримуваних Unicode символів
        supported_unicode = sorted(supported_unicode)

        # Рахуємо кількість рядків, потрібних для всіх символів
        row_count = (len(supported_unicode) + 9) // 10
        for row in range(row_count):
            for col in range(10):
                index = row * 10 + col
                if index < len(supported_unicode):
                    unicode_value = supported_unicode[index]
                    char = chr(unicode_value)

                    # Створюємо QLabel для відображення символу і коду Unicode
                    label = QLabel()
                    label.setText(f"<span style='font-family:{self.font_ttf}; font-size: 24px;'>{char}</span><br>"
                                  f"<span style='font-family: sans-serif; font-size: 12px;'>U+{unicode_value:04X}</span>")
                    label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Вирівнюємо по центру

                    # Вставляємо QLabel у таблицю
                    self.ui.tableWidget.setCellWidget(row, col, label)

            # Встановлюємо висоту рядка (за замовчуванням, 50 пікселів)
            self.ui.tableWidget.setRowHeight(row, 60)  # Встановлюємо більшу висоту для кожного рядка

        # Встановлюємо ширину колонок
        for col in range(10):
            self.ui.tableWidget.setColumnWidth(col, 120)  # Ширина для символа і коду Unicode

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
