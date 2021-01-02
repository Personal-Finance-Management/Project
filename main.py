import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication,QMainWindow
from PyQt5.QtWidgets import QTableView,QTableWidget,QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
import sqlite3 
import matplotlib.pyplot as plt
import pandas as pd 

def createConnection():
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName("csdl.db")
    if not con.open():
        QMessageBox.critical(
            None,
            "QTableView Example - Error!",
            "Database Error: %s" % con.lastError().databaseText(),
        )
        return False
    return True

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)

    def loginfunction(self):
        email = self.email.text()
        password = self.password.text()

        connection = sqlite3.connect("csdl.db")
        sql = "SELECT * FROM users WHERE username=\'" + email + "\' AND password=\'" + password + "\'"
        cursor = connection.execute(sql)
        list = []
        for row in cursor:
            list.append(row)
        connection.close()

        if len(list)==1:
            #msg = QMessageBox()
            #msg.setWindowTitle("Congratulation!")
            #my_message = "Successfully logged in with email: " + email 
            #msg.setText(my_message)
            #x= msg.exec_()           
            mainwindow = MainWindow()
            widget.addWidget(mainwindow)
            widget.setCurrentIndex(widget.currentIndex()+1)            
        else:
            #print("Successfully logged in with email: ", email, " and password: ", password)
            msg = QMessageBox()
            msg.setWindowTitle("Failed attempt!")
            my_message = "There is no such user with: " + email 
            msg.setText(my_message)
            x= msg.exec_()

    def gotocreate(self):
        createacc=CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("createacc.ui",self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.backtologinbutton.clicked.connect(self.backtologin)
        
    def createaccfunction(self):
        email = self.email.text()
        if self.password.text()==self.confirmpass.text():
            password = self.password.text()

            connection = sqlite3.connect("csdl.db")
            sql = "INSERT INTO users(username, password) VALUES (\'" + email + "\', \'" + password + "\')"
            connection.execute(sql)
            connection.commit()
            connection.close()

            #print("Successfully created account with email: ", email, "and password: ", password)
            msg = QMessageBox()
            msg.setWindowTitle("Congratulation!")
            my_message = "Successfully created account with email: " + email 
            msg.setText(my_message)
            x= msg.exec_()
            login=Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            #print("Password should be identical!")
            msg = QMessageBox()
            msg.setWindowTitle("Failed attempt!")
            my_message = "\"Confirmed Password\" should be identical to \"Password\"!"
            msg.setText(my_message)
            x= msg.exec_()
            #self.email.clear()
            self.password.clear()
            self.confirmpass.clear()

    def backtologin(self):
        loginback=Login()
        widget.addWidget(loginback)
        widget.setCurrentIndex(widget.currentIndex()+1)

class MainWindow(QMainWindow):    
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("mainwindow.ui",self)
        self.importbutton.clicked.connect(self.import_data)
        self.updatebutton.clicked.connect(self.update_data)
        self.analysebutton.clicked.connect(self.analyse_data)
        self.quitbutton.clicked.connect(self.quit_program)
    
    def import_data(self):
        pass

    def update_data(self):
        #self.adddata=AddData()
        #self.adddata.show()
        adddata=AddData()
        widget.addWidget(adddata)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def analyse_data(self):
        analysedata=AnalyseData()
        widget.addWidget(analysedata)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def quit_program(self):        
        sys. exit() 

class AddData(QMainWindow):    
    def __init__(self):
        super(AddData,self).__init__()
        loadUi("adddata.ui",self)
        self.count = 0
        self.addincomebutton.clicked.connect(self.add_income)
        self.addcostbutton.clicked.connect(self.add_cost)
        self.showincomebutton.clicked.connect(self.show_income)
        self.showcostbutton.clicked.connect(self.show_cost)
        self.backbutton.clicked.connect(self.back_window)

    def add_income(self):
        self.setWindowTitle("Add income interface")
        self.count = self.count + 1 # this is incrementing counter
        
        month = self.month.text()
        income = self.income.text()
        incometype = self.incometype.text()
        if self.month.text()!="" and self.income.text()!="" and self.incometype.text()!="":
            connection = sqlite3.connect("csdl.db")
            sql = "INSERT INTO incomes(month, income, incometype) VALUES (\'" + month + "\', \'" + income + "\', \'" + incometype + "\')"
            connection.execute(sql)
            connection.commit()
            connection.close()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Failed attempt!")
            my_message = "Input value for " 
            if self.month.text()=="":
                my_message += " \"Month\" "
            if self.income.text()=="":
                my_message += " \"Income\" "
            if self.incometype.text()=="":
                my_message += " \"Income Type\" " 
            msg.setText(my_message)
            x= msg.exec_()     

        #self.editdata=EditData()
        #self.editdata.show()
             
    def add_cost(self):
        self.setWindowTitle("Add cost interface")
        self.count = self.count + 1 # this is incrementing counter
        
        month = self.month.text()
        cost = self.cost.text()
        costtype = self.costtype.text()
        if self.month.text()!="" and self.cost.text()!="" and self.costtype.text()!="":
            connection = sqlite3.connect("csdl.db")
            sql = "INSERT INTO costs(month, cost, costtype) VALUES (\'" + month + "\', \'" + cost + "\', \'" + costtype + "\')"
            connection.execute(sql)
            connection.commit()
            connection.close()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Failed attempt!")
            my_message = "Input value for " 
            if self.month.text()=="":
                my_message += " \"Month\" "
            if self.cost.text()=="":
                my_message += " \"Cost\" "
            if self.costtype.text()=="":
                my_message += " \"Cost Type\" " 
            msg.setText(my_message)
            x= msg.exec_()    
        #self.editdata=EditData()
        #self.editdata.show()

    def show_income(self):
        self.showincome=ShowIncome()
        self.showincome.show()

    def show_cost(self):
        self.showcost=ShowCost()
        self.showcost.show()
    
    def back_window(self):
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)            

class AnalyseData(QMainWindow):    
    def __init__(self):
        super(AnalyseData,self).__init__()
        loadUi("analysedata.ui",self)
        self.incomemonthbutton.clicked.connect(self.income_bymonth)
        self.incometypebutton.clicked.connect(self.income_bytype)
        self.costmonthbutton.clicked.connect(self.cost_bymonth)
        self.costtypebutton.clicked.connect(self.cost_bytype)
        self.incomecostbutton.clicked.connect(self.compare_incomecost)
        self.backbutton.clicked.connect(self.back_window)

    def income_bymonth(self):
        # x-coordinates of left sides of bars  
        left = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] 
  
        # heights of bars 
        connection = sqlite3.connect("csdl.db")
        sql = "SELECT SUM(income) FROM incomes GROUP BY month"
        cursor = connection.execute(sql)
        income_values = []
        for row in cursor:
            income_values.append(row[0])
        connection.close()

        # labels for bars 
        tick_label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] 
  
        # plotting a bar chart 
        plt.bar(left, income_values, tick_label = tick_label, width = 0.8, color = ['red', 'green']) 
  
        # naming the x-axis 
        plt.xlabel('Months') 
        # naming the y-axis 
        plt.ylabel('Income') 
        # plot title 
        plt.title('Income over months!') 
  
        # function to show the plot 
        plt.show()

    def income_bytype(self):
        connection = sqlite3.connect("csdl.db")
        
        # defining labels 
        sql = "SELECT incometype FROM incomes GROUP BY incometype"
        cursor = connection.execute(sql)
        types = []
        for row in cursor:
            types.append(row[0])

        # portion covered by each label
        sql = "SELECT SUM(income) FROM incomes GROUP BY incometype"
        cursor = connection.execute(sql)
        slices = []
        for row in cursor:
            slices.append(row[0])
        connection.close()

        # plot title 
        plt.title('Income from different activities!') 

        # plotting the pie chart 
        explode_list = []
        start_value = 0
        for i in range(0,len(slices)):
            explode_list.append(start_value)
            start_value += 0.025
            print(start_value)
        slices.sort(reverse=True)
        plt.pie(slices, labels = types, colors=None, startangle=0, shadow = False, explode = explode_list, radius = 1, autopct = '%1.1f%%') 
  
        # plotting legend 
        plt.legend() 
  
        # showing the plot 
        plt.show() 

    def cost_bymonth(self):
        # x-coordinates of left sides of bars  
        left = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] 
  
        # heights of bars 
        connection = sqlite3.connect("csdl.db")
        sql = "SELECT SUM(cost) FROM costs GROUP BY month"
        cursor = connection.execute(sql)
        cost_values = []
        for row in cursor:
            cost_values.append(row[0])
        connection.close()

        # labels for bars 
        tick_label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] 
  
        # plotting a bar chart 
        plt.bar(left, cost_values, tick_label = tick_label, width = 0.8, color = ['red', 'green']) 
  
        # naming the x-axis 
        plt.xlabel('Months') 
        # naming the y-axis 
        plt.ylabel('Cost') 
        # plot title 
        plt.title('Cost over months!') 
  
        # function to show the plot 
        plt.show()


    def cost_bytype(self):
        connection = sqlite3.connect("csdl.db")
        
        # defining labels 
        sql = "SELECT costtype FROM costs GROUP BY costtype"
        cursor = connection.execute(sql)
        types = []
        for row in cursor:
            types.append(row[0])

        # portion covered by each label
        sql = "SELECT SUM(cost) FROM costs GROUP BY costtype"
        cursor = connection.execute(sql)
        slices = []
        for row in cursor:
            slices.append(row[0])

        connection.close()

        # plot title 
        plt.title('Cost from different activities!') 

        # plotting the pie chart 
        explode_list = []
        start_value = 0
        for i in range(0,len(slices)):
            explode_list.append(start_value)
            start_value += 0.025
            print(start_value)
        slices.sort(reverse=True)
        plt.pie(slices, labels = types, colors=None, startangle=0, shadow = False, explode = explode_list, radius = 1, autopct = '%1.1f%%')  
  
        # plotting legend 
        plt.legend() 
  
        # showing the plot 
        plt.show() 


    def compare_incomecost(self):
        connection = sqlite3.connect("csdl.db")
        
        # preparing aggregated income values
        sql = "SELECT SUM(income) FROM incomes GROUP BY month"
        cursor = connection.execute(sql)
        income_values = []
        for row in cursor:
            income_values.append(row[0])
        
        # preparing aggregated cost values
        sql = "SELECT SUM(cost) FROM costs GROUP BY month"
        cursor = connection.execute(sql)
        cost_values = []
        for row in cursor:
            cost_values.append(row[0])
        connection.close()
        plotdata = pd.DataFrame({'Income': income_values, 'Cost': cost_values}, index = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])    
        plotdata.plot(kind="bar")
        plt.title("Income versus Cost")
        plt.xlabel("Months")
        plt.ylabel("Income/Cost values")
        
        # showing the plot 
        plt.show()

    def back_window(self):
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1) 

class ShowIncome(QMainWindow):    
    def __init__(self):
        super(ShowIncome,self).__init__()
        self.load_initial_data()

    def load_initial_data(self):
        self.setWindowTitle("Show Income")
        self.resize(250, 250)
        # Set up the view and load the data
        self.view = QTableWidget()
        self.view.setColumnCount(3)
        self.view.setHorizontalHeaderLabels(["Month", "Income", "Income Type"])
        query = QSqlQuery("SELECT month, income, incometype FROM incomes")
        while query.next():
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            self.view.setItem(rows, 0, QTableWidgetItem(str(query.value(0))))
            self.view.setItem(rows, 1, QTableWidgetItem(str(query.value(1))))
            self.view.setItem(rows, 2, QTableWidgetItem(str(query.value(2))))
        self.view.resizeColumnsToContents()
        self.setCentralWidget(self.view)

class ShowCost(QMainWindow):    
    def __init__(self):
        super(ShowCost,self).__init__()
        self.load_initial_data()

    def load_initial_data(self):
        self.setWindowTitle("Show Cost")
        self.resize(250, 250)
        # Set up the view and load the data
        self.view = QTableWidget()
        self.view.setColumnCount(3)
        self.view.setHorizontalHeaderLabels(["Month", "Cost", "Cost Type"])
        query = QSqlQuery("SELECT month, cost, costtype FROM costs")
        while query.next():
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            self.view.setItem(rows, 0, QTableWidgetItem(str(query.value(0))))
            self.view.setItem(rows, 1, QTableWidgetItem(str(query.value(1))))
            self.view.setItem(rows, 2, QTableWidgetItem(str(query.value(2))))
        self.view.resizeColumnsToContents()
        self.setCentralWidget(self.view)


app = QApplication(sys.argv)
if not createConnection():
    msg = QMessageBox()
    msg.setWindowTitle("Error in opening data source!")
    my_message = "Could not open the data source. The program wil be closed! "  
    msg.setText(my_message)
    x= msg.exec_()
    sys.exit(1)
logindialog = Login()

widget = QtWidgets.QStackedWidget()
widget.addWidget(logindialog)
widget.setFixedWidth(510)
widget.setFixedHeight(620)
widget.show()
app.exec_()