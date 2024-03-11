from ui.UI_MainWindow import Ui_MainWindow
from ui.login import Ui_login
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt

class DB:
    def __init__(self, query, headers):
        self.model = QSqlQueryModel()
        self.query = query
        self.headers: list = headers

    def setHeaders(self):
        for i in range(1, len(self.headers) + 1, 1):
            self.model.setHeaderData(i, Qt.Orientation.Horizontal, str(self.headers[i - 1]))

    def setQuery(self):
        self.model.setQuery(str(self.query))

    def getmodel(self):
        return self.model

    def delete(self, table, type):
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setStandardButtons(QMessageBox.Ok)
        if type == 1:
            text = "select info.delete_Storage('"
        if type == 2:
            text = "select info.delete_Cashier('"
        if type == 3:
            text = "select info.delete_Product('"
        if type == 4:
            text = "select info.delete_Bill('"
        if type == 5:
            text = "select info.delete_view('"
        text = text + str(table.model().index(table.currentIndex().row(),0).data()) + "');"
        guery = QSqlQuery()
        guery.exec(text)
        if (guery.lastError().number() == 42501):
            msg.setText("Нет доступа к данной функции")
            msg.exec()

        elif (guery.lastError().number() == -1):
            msg.setWindowTitle("Удаление")
            msg.setText("Данные удалены")
            msg.exec()
            self.model.setQuery(str(self.query))
        else:
            msg.setText("Ошибка \n" + guery.lastError().text())
            msg.exec()

    def add(self, lines, type, index):
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setStandardButtons(QMessageBox.Ok)
        text = ""
        if type == 1:
            text = "select info.add_Storage('"
        if type == 2:
            text = "call info.add_cashier_witch_age_check('"
        if type == 3:
            text = "select info.add_Product('" + index + "' , '"
        if type == 4:
            if(lines[2] != ""):
                text = "select info.add_Bill('" + index[0] + "' , '" + index[1] + "' , '" + str(
                    round((float(index[2]) - float(index[2]) * (float(lines[2]) / 100)))) + "' , '"
        if type == 5:
            text = "select info.add_view('"
        for i in range(len(lines)):
            if lines[i] == "":
                msg.setText("Не все данные введены")
                msg.exec()
                return
            text = text + lines[i]
            if i+1 != len(lines):
                text = text + "' , '"
        text = text + "');"
        guery = QSqlQuery()
        guery.exec(text)
        if(guery.lastError().number() == 42501):
            msg.setText("Нет доступа к данной функции")
            msg.exec()

        elif(guery.lastError().number() == -1):
            msg.setWindowTitle("Добавление")
            msg.setText("Данные записаны")
            msg.exec()
            self.model.setQuery(str(self.query))
        else:
            msg.setText("Ошибка \n" + guery.lastError().text())
            msg.exec()

    def change(self,lines, type, index):
        text = ""
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setStandardButtons(QMessageBox.Ok)
        if type == 1:
            text = "select info.change_Storage('"
        if type == 2:
            text = "select info.change_Cashier('"
        if type == 3:
            text = "select info.change_Product('" + index[1] + "' , '"
        if type == 4:
            text = "select info.change_Bill('" + index[1] + "' , '" + index[2] + "' , '"
        if type == 5:
            text = "select info.change_view('"
        text = text + index[0] + "' , '"
        for i in range(len(lines)):
            if lines[i] == '':
                msg.setText("Не все данные введены")
                msg.exec()
                return
            text = text + lines[i]
            if i + 1 != len(lines):
                text = text + "' , '"
        text = text + "');"
        guery = QSqlQuery()
        guery.exec(text)
        if (guery.lastError().number() == 42501):
            msg.setText("Нет доступа к данной функции")
            msg.exec()

        elif (guery.lastError().number() == -1):
            msg.setWindowTitle("Добавление")
            msg.setText("Данные записаны")
            msg.exec()
            self.model.setQuery(str(self.query))
        else:
            msg.setText("Ошибка \n" + guery.lastError().text())
            msg.exec()


class login(QtWidgets.QMainWindow):
    def __init__(self):
        super(login, self).__init__()
        self.ui = Ui_login()
        self.ui.setupUi(self)
        self.ui.lineEdit.returnPressed.connect(self.con)
        self.ui.lineEdit_2.returnPressed.connect(self.con)

    def con(self):
        con = QSqlDatabase.addDatabase("QPSQL")
        con.setDatabaseName("Kyrsach")
        con.setHostName("localhost")
        con.setPort(5432)
        con.setUserName(str(self.ui.lineEdit.text()))
        con.setPassword(str(self.ui.lineEdit_2.text()))
        self.ui.label_3.setText(str(con.open()))
        self.ui.label_4.setText(str(con.lastError().text()))
        if con.open():
            self.application = mywindow()
            self.application.show()


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        application.close()
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        Storage = DB("select s_id,place,address from info.Storage", ['Place', 'Address'])
        Cashier = DB("select c_id,flname,tel,post,Con,age from info.Cashier", ['FLName', 'Tel', 'Post', 'Сountry', 'Age', ])
        Product = DB("select p.p_id, p.p_name, p.price, p.vat, p.amount, s.place, s.address from info.product as p left join info.storage as s on p.storageid = s.s_id", ['P_Name', 'Price', 'VAT', 'Amount','Place','Address'])
        Bill = DB("select b.b_id,p.p_name, p.price, b.buytime, b.officenumber, b.sale, b.finalprice, b.paymentype,c.flname,c.post from info.bill as b left join info.product as p on b.productid = p.p_id left join info.cashier as c on b.cashierid = c.c_id",['Product','Price','BuyTime', 'OfficeNumber', 'Sale', 'FinalPrice','PaymenType','Flname','Post'])
        Case = DB("select b.b_id, p.p_name, p.price, b.finalprice,CASE when b.sale = 0 THEN 'Без Скидки' ELSE 'Со Скидкой' END AS sale From info.bill AS b JOIN info.product as p ON b.productid = p.p_id",['Название Товара','Цена','Итоговая цена','Скидка'])
        View = DB("select * from info.cashier_view", ['ФИО', 'Телефон', 'Должность', 'Страна', 'Возраст', 'Время обновления записи'])
        Having = DB("SELECT count(p.price),c.flname, sum(p.price) as bruh From info.bill as b  join info.cashier as c on b.cashierid = c.c_id join info.product as p on b.productid = p.p_id GROUP BY c.flname Having (sum(p.price) > 1000)",['ФИО', 'Сумма'])
        Any = DB("select c.c_id,c.flname, c.post, b.finalprice from info.bill as b left join info.cashier as c on b.cashierid = c.c_id where b_id = any (select b_id from info.bill where finalprice > 150)",['ФИО', 'Должность', 'Цена'])
        self.display(Storage,self.ui.tableView)
        self.display(Storage, self.ui.tableView_5)
        self.display(Cashier, self.ui.tableView_2)
        self.display(Product, self.ui.tableView_3)
        self.display(Bill, self.ui.tableView_4)
        self.display(Cashier, self.ui.tableView_7)
        self.display(Product, self.ui.tableView_6)
        self.display(Case, self.ui.tableView_8)
        self.display(View, self.ui.tableView_9)
        self.display(Cashier, self.ui.tableView_10)
        self.display(Having, self.ui.tableView_11)
        self.display(Any, self.ui.tableView_12)
        self.ui.lineEdit_21.returnPressed.connect(lambda:self.Cursor(Cashier,self.ui.lineEdit_21.text()))
        self.ui.pushButton_15.clicked.connect(lambda:Cashier.setQuery())
        self.ui.pushButton_18.clicked.connect(lambda:Having.setQuery())
        self.ui.pushButton_19.clicked.connect(lambda:Any.setQuery())

        self.ui.pushButton.clicked.connect(lambda:Storage.add([self.ui.lineEdit_2.text(),self.ui.lineEdit_3.text()],1,0))
        self.ui.pushButton_9.clicked.connect(lambda:Product.add([self.ui.lineEdit_7.text(),self.ui.lineEdit_8.text(),self.ui.lineEdit_9.text(),self.ui.lineEdit_16.text()],3,str(self.ui.tableView_5.model().index(self.ui.tableView_5.currentIndex().row(),0).data())))
        self.ui.pushButton_6.clicked.connect(lambda:Cashier.add([self.ui.lineEdit_4.text(),self.ui.lineEdit_5.text(),self.ui.lineEdit_6.text(),self.ui.lineEdit_13.text(),self.ui.lineEdit_14.text()],2,0))
        self.ui.pushButton_12.clicked.connect(lambda:Bill.add([self.ui.lineEdit.text(),self.ui.lineEdit_10.text(),self.ui.lineEdit_11.text(),self.ui.lineEdit_15.text()],4,[str(self.ui.tableView_7.model().index(self.ui.tableView_7.currentIndex().row(),0).data()),str(self.ui.tableView_6.model().index(self.ui.tableView_6.currentIndex().row(),0).data()),str(self.ui.tableView_6.model().index(self.ui.tableView_6.currentIndex().row(),2).data())]))

        self.ui.pushButton_2.clicked.connect(lambda:Storage.delete(self.ui.tableView,1))
        self.ui.pushButton_7.clicked.connect(lambda:Product.delete(self.ui.tableView_3,3))
        self.ui.pushButton_4.clicked.connect(lambda:Cashier.delete(self.ui.tableView_2,2))
        self.ui.pushButton_10.clicked.connect(lambda:Bill.delete(self.ui.tableView_4,4))
        self.ui.pushButton_17.clicked.connect(lambda: View.delete(self.ui.tableView_9, 5))

        self.ui.pushButton_13.clicked.connect(lambda: Case.setQuery())
        self.ui.pushButton_14.clicked.connect(lambda: View.setQuery())

        self.ui.pushButton_16.clicked.connect(
            lambda: (Cashier.change([self.ui.lineEdit_12.text(), self.ui.lineEdit_17.text(), self.ui.lineEdit_18.text(), self.ui.lineEdit_19.text(), self.ui.lineEdit_20.text()], 5, [
                str(self.ui.tableView_9.model().index(self.ui.tableView_9.currentIndex().row(), 0).data())]),View.setQuery()))
        self.ui.pushButton_3.clicked.connect(
            lambda: Storage.change([self.ui.lineEdit_2.text(), self.ui.lineEdit_3.text()], 1,[str(self.ui.tableView.model().index(self.ui.tableView.currentIndex().row(),0).data())]))
        self.ui.pushButton_8.clicked.connect(
            lambda: Product.change([self.ui.lineEdit_7.text(), self.ui.lineEdit_8.text(), self.ui.lineEdit_9.text(),self.ui.lineEdit_16.text()], 3,[str(self.ui.tableView_3.model().index(self.ui.tableView_3.currentIndex().row(),0).data()),str(self.ui.tableView_5.model().index(self.ui.tableView_5.currentIndex().row(),0).data())]))
        self.ui.pushButton_5.clicked.connect(lambda: Cashier.change(
            [self.ui.lineEdit_4.text(), self.ui.lineEdit_5.text(), self.ui.lineEdit_6.text(),
             self.ui.lineEdit_13.text(), self.ui.lineEdit_14.text()], 2,[str(self.ui.tableView_2.model().index(self.ui.tableView_2.currentIndex().row(),0).data())]))
        self.ui.pushButton_11.clicked.connect(lambda: Bill.change(
            [self.ui.lineEdit.text(), self.ui.lineEdit_10.text(), self.ui.lineEdit_11.text(),
             self.ui.lineEdit_15.text()], 4,[str(self.ui.tableView_4.model().index(self.ui.tableView_4.currentIndex().row(),0).data()),str(self.ui.tableView_7.model().index(self.ui.tableView_7.currentIndex().row(),0).data()),str(self.ui.tableView_6.model().index(self.ui.tableView_6.currentIndex().row(),0).data())]))



        self.ui.tableView.clicked.connect(lambda:self.selchang([self.ui.lineEdit_2,self.ui.lineEdit_3],2,self.ui.tableView))
        self.ui.tableView_3.clicked.connect(
            lambda: self.selchang([self.ui.lineEdit_7, self.ui.lineEdit_8,self.ui.lineEdit_9,self.ui.lineEdit_16], 4, self.ui.tableView_3))
        self.ui.tableView_2.clicked.connect(
            lambda: self.selchang([self.ui.lineEdit_4, self.ui.lineEdit_5, self.ui.lineEdit_6, self.ui.lineEdit_13,self.ui.lineEdit_14], 5,
                                  self.ui.tableView_2))
        self.ui.tableView_4.clicked.connect(
            lambda: self.selchang(
                [self.ui.lineEdit, self.ui.lineEdit_10, self.ui.lineEdit_11, self.ui.lineEdit_15],4,self.ui.tableView_4))
        self.ui.tableView_9.clicked.connect(
            lambda: self.selchang(
                [self.ui.lineEdit_12, self.ui.lineEdit_17, self.ui.lineEdit_18, self.ui.lineEdit_19,self.ui.lineEdit_20], 5,
                self.ui.tableView_9))
        self.ui.tableView_10.clicked.connect(lambda: self.selchang([self.ui.lineEdit_21], 1,self.ui.tableView_10))
    def selchang(self,line,col,table):
        if (table == self.ui.tableView_4):
            line[0].setText((table.model().index(table.currentIndex().row(), 3).data()).toString(Qt.DefaultLocaleLongDate))
            line[1].setText(str(table.model().index(table.currentIndex().row(), 4).data()))
            line[2].setText(str(table.model().index(table.currentIndex().row(), 5).data()))
            line[3].setText(str(table.model().index(table.currentIndex().row(), 7).data()))
        elif(table == self.ui.tableView_10):
            line[0].setText(str(table.model().index(table.currentIndex().row(), 2).data()))
        else:
            for i in range(0, col, 1):
                line[i].setText(str(table.model().index(table.currentIndex().row(), i + 1).data()))



    def display(self,model,table):
        model.setQuery()
        model.setHeaders()
        table.setModel(model.getmodel())
        table.setColumnHidden(0, 1)

    def Cursor(self,model,tel):
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setStandardButtons(QMessageBox.Ok)
        guery = QSqlQuery()
        guery.exec("call info.cursos_delete_telephone('"+str(tel)+"')")
        if (guery.lastError().number() == -1):
            msg.setWindowTitle("Добавление")
            msg.setText("Данные удалены")
            msg.exec()
            model.setQuery()
            model.setHeaders()
        else:
            msg.setText("Ошибка \n" + guery.lastError().text())
            msg.exec()



app = QtWidgets.QApplication([])
application = login()
application.show()
sys.exit(app.exec())
