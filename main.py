import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QVBoxLayout, QPushButton, QLabel, QTableWidget,QTableWidgetItem)


class InfectionTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)  # Вертикальное расположение элементов

        layout.addWidget(QLabel("Данные об инфекционных заболеваниях:"))

        self.table = QTableWidget()  # Таблица для данных
        layout.addWidget(self.table)

        self.btn_analyze = QPushButton("Выполнить анализ и построить график")  # Кнопка
        layout.addWidget(self.btn_analyze)

        self.figure = plt.figure()  # Область для графика
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.load_and_show_table() # Загружаем данные при запуске

    def load_and_show_table(self):
        try:
            df = pd.read_csv('infection_data.csv')

            # Настройка таблицы под размер данных
            self.table.setRowCount(len(df))
            self.table.setColumnCount(len(df.columns))
            self.table.setHorizontalHeaderLabels(df.columns)

            # Заполнение ячеек
            for i in range(len(df)):
                for j in range(len(df.columns)):
                    self.table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))

            print("Таблица заполнена данными об инфекциях")
        except FileNotFoundError:
            print("Файл infection_data.csv не найден!")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализ инфекций в РФ (Вариант 15)")
        self.setCentralWidget(InfectionTab())  # Вставляем  вкладку в главное окно


if __name__ == "__main__":  # Точка входа в программу
    app = QApplication(sys.argv)  # Создаём приложение
    window = MainWindow()          # Создаём окно
    window.show()                  # Показываем окно
    sys.exit(app.exec_())          # Запускаем цикл обработки событий (чтобы окно не закрывалось)