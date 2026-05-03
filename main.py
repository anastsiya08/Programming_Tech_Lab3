import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QVBoxLayout, QPushButton, QLabel, QTableWidget,QTableWidgetItem,QHeaderView, QLineEdit)


class InfectionTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)  # Вертикальное расположение элементов

        layout.addWidget(QLabel("Данные об инфекционных заболеваниях:"))

        self.table = QTableWidget()  # Таблица для данных
        layout.addWidget(self.table)

        self.btn_analyze = QPushButton("Выполнить анализ и построить график")  # Кнопка
        self.btn_analyze.clicked.connect(self.analyze_infections) #вызов функции analyze_infections
        layout.addWidget(self.btn_analyze)

        self.figure = plt.figure()  # Область для графика
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.load_and_show_table() # Загружаем данные при запуске
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.result_label = QLabel("")
        layout.addWidget(self.result_label)
        layout.addWidget(QLabel("Прогноз на N лет (экстраполяция):"))
        self.n_input = QLineEdit("5")  # Поле для ввода числа N (по умолчанию 5 лет)
        layout.addWidget(self.n_input) # Добавляем поле ввода в интерфейс

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

    def analyze_infections(self):
        try:
            df = pd.read_csv('infection_data.csv')
            n_years = int(self.n_input.text())
            self.figure.clear()

            diseases = df.columns[1:]  # Все болезни
            num_diseases = len(diseases)

            for i, disease in enumerate(diseases):
                ax = self.figure.add_subplot(3, 2, i + 1)

                # Реальные данные
                line, = ax.plot(df['Год'], df[disease], marker='o', markersize=4, label='Факт')
                color = line.get_color()

                # Экстраполяция (Прогноз)
                last_year = df['Год'].max()
                avg_growth = df[disease].diff().tail(3).mean()

                future_years = [last_year + j for j in range(1, n_years + 1)]
                future_values = [df[disease].iloc[-1] + avg_growth * j for j in range(1, n_years + 1)]
                ax.plot([df['Год'].iloc[-1]] + future_years,
                        [df[disease].iloc[-1]] + future_values,
                        linestyle='--', color=color, alpha=0.7, label='Прогноз')

                ax.set_title(disease, fontsize=10)
                ax.grid(True, linestyle=':', alpha=0.6)
                if i == 0: ax.legend(fontsize='x-small')  # Легенда только на первом для чистоты

            self.figure.tight_layout()
            self.canvas.draw()

            # Анализ
            decreases = {col: df[col].iloc[-1] - df[col].iloc[0] for col in diseases}
            best = min(decreases, key=decreases.get)
            worst = max(decreases, key=decreases.get)

            self.result_label.setText(
                f"📉 Снизилась больше всех: {best} (на {abs(decreases[best])} чел.)\n"
                f"📈 Снизилась меньше всех: {worst} (на {abs(decreases[worst])} чел.)"
            )
        except Exception as e:
            print(f"Ошибка: {e}")

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