import sys
import os
import PyQt5
dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'Qt5', 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QVBoxLayout, QPushButton, QLineEdit, QLabel)


class SalaryTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Прогноз на N лет (экстраполяция):"))
        self.n_input = QLineEdit("3")
        layout.addWidget(self.n_input)

        self.btn_calc = QPushButton("Загрузить данные и построить графики")
        layout.addWidget(self.btn_calc)

        # Подключаем метод загрузки
        self.btn_calc.clicked.connect(self.load_data)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def load_data(self):
        try:
            # Читаем данные
            self.df = pd.read_csv('salary_data.csv')
            print("Данные успешно загружены:")
            print(self.df.head())  # Вывод первых строк в консоль

            # Вычисляем процент роста (подготовка к анализу)
            self.df['Men_Growth'] = self.df['Men'].pct_change() * 100
            self.df['Women_Growth'] = self.df['Women'].pct_change() * 100

            self.btn_calc.setText("Данные загружены. Нажми для графиков")
        except FileNotFoundError:
            print("Ошибка: Файл salary_data.csv не найден!")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализ зарплат в РФ (Вариант 8)")
        self.setCentralWidget(SalaryTab())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())