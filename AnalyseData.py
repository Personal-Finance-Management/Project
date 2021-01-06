from PyQt5.QtWidgets import QDialog,QApplication,QMainWindow
from PyQt5.uic import loadUi
import sqlite3 
import matplotlib.pyplot as plt
import pandas as pd 
class AnalyseData(QMainWindow):    
    def __init__(self, widget, MainWindow):
        super(AnalyseData,self).__init__()
        loadUi("analysedata.ui",self)
        self.incomemonthbutton.clicked.connect(self.income_bymonth)
        self.incometypebutton.clicked.connect(self.income_bytype)
        self.costmonthbutton.clicked.connect(self.cost_bymonth)
        self.costtypebutton.clicked.connect(self.cost_bytype)
        self.incomecostbutton.clicked.connect(self.compare_incomecost)
        self.backbutton.clicked.connect(self.back_window)

        self.widget = widget
        self.MainWindow = MainWindow

    def get_data(self, sql): 
        connection = sqlite3.connect("csdl.db")
        cursor = connection.execute(sql)
        values = []
        for row in cursor:
            values.append(row[0])
        connection.close()
        return values

    def draw_bar_graph(self, sql, title, xlabel, ylabel):
        left = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] 
        tick_label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] 
        right = self.get_data(sql) 

        plt.ion()
        fig = plt.figure(figsize=(10,8))
        ax = fig.add_axes([0.1,0.1,0.8,0.8])
        ax.bar(left, right, tick_label = tick_label, width = 0.8, color = ['red', 'green']) 
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

    def draw_pie_graph(self, title, types, slices): 
        plt.ion()
        plt.title(title)

        explode_list = []
        start_value = 0
        for i in range(0,len(slices)):
            explode_list.append(start_value)
            start_value += 0.025
        slices.sort(reverse=True)
        plt.pie(slices, labels = types, colors=None, startangle=0, shadow = False, explode = explode_list, radius = 1, autopct = '%1.1f%%')  
        plt.legend() 

    def income_bymonth(self):
        sql = "SELECT SUM(income) FROM incomes GROUP BY month"
        self.draw_bar_graph(sql, 'Income over months!', 'Months', 'Income')

    def income_bytype(self):
        types = self.get_data("SELECT incometype FROM incomes GROUP BY incometype")
        slices = self.get_data("SELECT SUM(income) FROM incomes GROUP BY incometype")
        self.draw_pie_graph('Income from different activities!', types, slices)

    def cost_bymonth(self):
        sql = "SELECT SUM(cost) FROM costs GROUP BY month"
        self.draw_bar_graph(sql, 'Cost over months!', 'Months', 'Cost')

    def cost_bytype(self):
        types = self.get_data("SELECT costtype FROM costs GROUP BY costtype")
        slices = self.get_data("SELECT SUM(cost) FROM costs GROUP BY costtype")
        self.draw_pie_graph('Cost from different activities!', types, slices)

    def compare_incomecost(self):
        income_values = self.get_data("SELECT SUM(income) FROM incomes GROUP BY month")
        cost_values = self.get_data("SELECT SUM(cost) FROM costs GROUP BY month")
        plt.ion()
        plotdata = pd.DataFrame({'Income': income_values, 'Cost': cost_values}, index = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])    
        plotdata.plot(kind="bar")
        plt.title("Income versus Cost")
        plt.xlabel("Months")
        plt.ylabel("Income/Cost values")

    def back_window(self):
        mainwindow = self.MainWindow()
        self.widget.addWidget(mainwindow)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1) 