import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QLineEdit, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib import style
from DataCollector import DataCollector


class PlotCanvas(QDialog):
    def __init__(self, parent=None):
        super(PlotCanvas, self).__init__(parent)
        self.setWindowTitle("Graph generator")
        self.setGeometry(200, 200, 1000, 700)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.initUI()

    def initUI(self):
        style.use("seaborn")
        self.button_date_plot = QtWidgets.QPushButton(self)
        self.button_date_plot.setText("Date plot")
        self.button_date_plot.move(50, 10)
        self.button_date_plot.setStyleSheet("background-color: grey")
        self.button_date_plot.clicked.connect(self.date_plot)

        self.button_pie_plot = QtWidgets.QPushButton(self)
        self.button_pie_plot.setText("Pie plot")
        self.button_pie_plot.move(170, 10)
        self.button_pie_plot.setStyleSheet("background-color: grey")
        self.button_pie_plot.clicked.connect(self.pie_plot)

        self.button_bar_plot = QtWidgets.QPushButton(self)
        self.button_bar_plot.setText("Bar plot")
        self.button_bar_plot.move(270, 10)
        self.button_bar_plot.setStyleSheet("background-color: grey")
        self.button_bar_plot.clicked.connect(self.bar_plot)

        self.button_loadgraph = QtWidgets.QPushButton(self)
        self.button_loadgraph.setText("Load graphs")
        self.button_loadgraph.setStyleSheet("background-color: grey")
        self.button_loadgraph.clicked.connect(self.csv)

        self.button_read = QtWidgets.QPushButton(self)
        self.button_read.setText("Load csv file")
        self.button_read.setStyleSheet("background-color: grey")
        self.button_read.clicked.connect(self.clicked)

        self.textedit = QTextEdit(self)

        self.textbox1 = QLineEdit(self)
        self.textbox1.setStyleSheet("background-color: white")

        self.textbox2 = QLineEdit(self)
        self.textbox2.setStyleSheet("background-color: white")

        layoutV = QVBoxLayout()
        layoutV.addStretch(1)
        layoutV.addWidget(self.toolbar)
        layoutV.addWidget(self.canvas)
        layoutV.addWidget(self.button_date_plot)
        layoutV.addWidget(self.button_pie_plot)
        layoutV.addWidget(self.button_bar_plot)
        layoutV.addWidget(self.button_read)
        layoutV.addWidget(self.button_loadgraph)
        layoutV.addWidget(self.textbox1)
        layoutV.addWidget(self.textbox2)
        layoutV.addWidget(self.textbox1)
        layoutV.addWidget(self.textbox2)

        layoutH = QHBoxLayout()
        layoutH.addWidget(self.textedit)
        layoutH.addLayout(layoutV)

        self.setLayout(layoutV)
        self.setLayout(layoutH)

    def csv(self):
        self.data = pd.read_csv(self.path)
        self.country1 = self.data[self.data.geoId == f"{self.textbox1.text()}"]
        self.country2 = self.data[self.data.geoId == f"{self.textbox2.text()}"]

    def date_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot_date(self.country1.dateRep, self.country1.cases, linestyle='solid')
        ax.set_title("Date plot")
        ax.set_xlabel("Data")
        ax.set_ylabel("Ilość przypadków")
        self.canvas.draw()

    def pie_plot(self):
        self.figure.clear()
        self.world_cases = [sum(self.country1.cases), sum(self.country2.cases)]
        ax = self.figure.add_subplot(111)
        ax.pie(self.world_cases, autopct='%1.1f%%')
        ax.set_title("Pie plot \n Procentowy udział krajów w sumie przypadków zakazenia")
        self.canvas.draw()

    def bar_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        bar_data1 = [self.textbox1.text(), self.textbox2.text()]
        bar_data2 = [sum(self.country1.cases), sum(self.country2.cases)]
        ax.bar(bar_data1, bar_data2)
        ax.set_title("Bar plot")
        ax.set_xlabel("Kraje")
        ax.set_ylabel("Ilość przypadków")
        self.canvas.draw()

    def clicked(self):
        self.data_loader()

    def data_loader(self):
        dataCollector = DataCollector()
        dataCollector.open_dialog_box()
        self.path = dataCollector.path
        self.file = dataCollector.file

        if self.file[0]:
            f = open(self.file[0], "r")

            with f:
                ddata = f.read()
                self.textedit.setText(ddata)
