import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import PyQt5
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLineEdit, QLabel, QTableWidget,
                             QTableWidgetItem, QHeaderView, QTabWidget)

# Настройка окружения для корректной работы PyQt5
dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'Qt5', 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

class SalaryTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.stats_label = QLabel("Нажмите кнопку для расчета статистики")
        self.stats_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        layout.addWidget(self.stats_label)

        layout.addWidget(QLabel("Прогноз на N лет (экстраполяция):"))
        self.n_input = QLineEdit("3")
        layout.addWidget(self.n_input)

        self.btn_calc = QPushButton("Загрузить данные и построить графики")
        layout.addWidget(self.btn_calc)

        self.btn_calc.clicked.connect(self.load_data)

        self.table = QTableWidget()
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def load_data(self):
        try:
            self.df = pd.read_csv('salary_data.csv')
            n_years = int(self.n_input.text())
            print("Данные успешно загружены")

            self.table.setRowCount(len(self.df))
            self.table.setColumnCount(len(self.df.columns))
            self.table.setHorizontalHeaderLabels(self.df.columns)

            for i in range(len(self.df)):
                for j in range(len(self.df.columns)):
                    val = self.df.iloc[i, j]
                    if isinstance(val, float):
                        val = f"{val:.2f}"
                    self.table.setItem(i, j, QTableWidgetItem(str(val)))

            self.figure.clear()
            ax = self.figure.add_subplot(111)

            ax.plot(self.df['Year'], self.df['Men'], 'b-o', label='Мужчины (факт)')
            ax.plot(self.df['Year'], self.df['Women'], 'r-s', label='Женщины (факт)')

            last_year = self.df['Year'].max()
            avg_growth_m = self.df['Men'].diff().tail(3).mean()
            avg_growth_w = self.df['Women'].diff().tail(3).mean()

            future_years = [last_year + i for i in range(1, n_years + 1)]
            future_men = [self.df['Men'].iloc[-1] + avg_growth_m * i for i in range(1, n_years + 1)]
            future_women = [self.df['Women'].iloc[-1] + avg_growth_w * i for i in range(1, n_years + 1)]

            ax.plot([self.df['Year'].iloc[-1]] + future_years,
                    [self.df['Men'].iloc[-1]] + future_men, 'b--', alpha=0.5, label='Прогноз (М)')
            ax.plot([self.df['Year'].iloc[-1]] + future_years,
                    [self.df['Women'].iloc[-1]] + future_women, 'r--', alpha=0.5, label='Прогноз (Ж)')

            ax.set_title(f'Анализ зарплат и прогноз на {n_years} лет')
            ax.legend()
            ax.grid(True)
            self.canvas.draw()

            m_pct = self.df['Men'].pct_change() * 100
            w_pct = self.df['Women'].pct_change() * 100

            m_max, m_min = m_pct.max(), m_pct.min()
            w_max, w_min = w_pct.max(), w_pct.min()

            stats_text = (
                f"Мужчины: макс. рост {m_max:.2f}%, мин. {m_min:.2f}%\n"
                f"Женщины: макс. рост {w_max:.2f}%, мин. {w_min:.2f}%"
            )
            self.stats_label.setText(stats_text)

        except Exception as e:
            print(f"Ошибка в расчетах: {e}")

class InfectionTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Данные об инфекционных заболеваниях:"))

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.btn_analyze = QPushButton("Выполнить анализ и построить график")
        self.btn_analyze.clicked.connect(self.analyze_infections)
        layout.addWidget(self.btn_analyze)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.load_and_show_table()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.result_label = QLabel("")
        layout.addWidget(self.result_label)
        layout.addWidget(QLabel("Прогноз на N лет (экстраполяция):"))
        self.n_input = QLineEdit("5")
        layout.addWidget(self.n_input)

    def load_and_show_table(self):
        try:
            df = pd.read_csv('infection_data.csv')
            self.table.setRowCount(len(df))
            self.table.setColumnCount(len(df.columns))
            self.table.setHorizontalHeaderLabels(df.columns)

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

            diseases = df.columns[1:]
            for i, disease in enumerate(diseases):
                ax = self.figure.add_subplot(3, 2, i + 1)
                line, = ax.plot(df['Год'], df[disease], marker='o', markersize=4, label='Факт')
                color = line.get_color()

                last_year = df['Год'].max()
                avg_growth = df[disease].diff().tail(3).mean()

                future_years = [last_year + j for j in range(1, n_years + 1)]
                future_values = [df[disease].iloc[-1] + avg_growth * j for j in range(1, n_years + 1)]
                ax.plot([df['Год'].iloc[-1]] + future_years,
                        [df[disease].iloc[-1]] + future_values,
                        linestyle='--', color=color, alpha=0.7, label='Прогноз')

                ax.set_title(disease, fontsize=10)
                ax.grid(True, linestyle=':', alpha=0.6)
                if i == 0: ax.legend(fontsize='x-small')

            self.figure.tight_layout()
            self.canvas.draw()

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
        self.setWindowTitle("Анализ данных в РФ (Варианты 8 и 15)")
        self.resize(1000, 800)
        
        # Интеграция обеих работ через вкладки
        self.tabs = QTabWidget()
        self.tabs.addTab(SalaryTab(), "Зарплаты (Вар. 8)")
        self.tabs.addTab(InfectionTab(), "Инфекции (Вар. 15)")
        self.setCentralWidget(self.tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())