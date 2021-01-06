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
from AnalyseData import AnalyseData 

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
#Do not let username and password leave blank
        if email == "" or password =="":
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            my_message = "Please fill in username and password"
            msg.setText(my_message)
            x= msg.exec_() 
        else: 
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
                my_message = "There is no username as " + email 
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
        password = self.password.text()
        confirmpass = self.confirmpass.text()
        safetyquestion = self.safetyquestion.text()
        
        if email == "" or password =="" or confirmpass =="" or safetyquestion == "":
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            my_message = "Please fill in username, password, and confirmed password"
            msg.setText(my_message)
            x= msg.exec_() 
        else: 
            if self.password.text()==self.confirmpass.text():
                #checking username availability in database
                connection = sqlite3.connect("csdl.db")
                query = "SELECT * from users WHERE username =\'" + email+ "\'"
                table = connection.execute(query)
                list = []
                for row in table:
                    list.append(row)
                connection.close()

                if len(list)==1: 
                    print ("The username has already registered. Please try the other name")
                    msg = QMessageBox()
                    msg.setWindowTitle("Fail to creat an account!")
                    my_message = "The chosen username ID has already existed. Please try another name" 
                    msg.setText(my_message)
                    x= msg.exec_()

                else: 
                    if self.checkbox.clicked and self.checkbox_2.clicked or self.checkbox.clicked and self.checkbox_3.clicked or self.checkbox_2.clicked and self.checkbox_3.clicked:
                        print ("Please choose only one safety question")
                        msg = QMessageBox()
                        msg.setWindowTitle("Fail to creat an account!")
                        error_message = "Please only choose one safety question!!!" 
                        msg.setText(error_message)
                        x= msg.exec_()
                    else:
                        connection = sqlite3.connect("csdl.db")
                        sql = "INSERT INTO users(username, password,safetyquestion) VALUES (\'" + email + "\', \'" + password + "\',\'" + safetyquestion + "\' )"
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
        analysedata=AnalyseData(widget, MainWindow)
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
widget.setFixedHeight(800)
widget.show()
app.exec_()
