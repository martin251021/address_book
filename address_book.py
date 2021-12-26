import sys
import os
from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5.QtCore import (QFile, Qt)
from PyQt5.QtSql import QSqlTableModel, QSqlQuery, QSqlDatabase
from PyQt5.QtWidgets import QTableView ,QMessageBox, QDialog, QMenu
from PyQt5 import QtSql

qt_creator_file = "main.ui"
Ui_main_widget, QtBaseClass = uic.loadUiType(qt_creator_file)

ID, Name, Surname, Address, ZIP, City, Tel_number, E_mail = range(8)

class MainWindow(QDialog):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.ui = Ui_main_widget()
        self.ui.setupUi(self)

        self.model = QtSql.QSqlTableModel(self)

        self.model.setTable("Data")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)

        self.model.setSort(Name, Qt.AscendingOrder)
        self.model.setSort(ID, Qt.AscendingOrder)
        self.model.setHeaderData(ID, Qt.Horizontal, "ID")
        self.model.setHeaderData(Name, qtc.Qt.Horizontal, "Name")
        self.model.setHeaderData(Surname, qtc.Qt.Horizontal, "Surname")
        self.model.setHeaderData(Address, qtc.Qt.Horizontal, "Address")
        self.model.setHeaderData(ZIP, qtc.Qt.Horizontal, "ZIP")
        self.model.setHeaderData(City, qtc.Qt.Horizontal, "City")
        self.model.setHeaderData(Tel_number, qtc.Qt.Horizontal, "Telephone number")
        self.model.setHeaderData(E_mail, qtc.Qt.Horizontal, "E-mail")

        self.model.select()

        self.view = self.ui.table
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()
        self.view.setSelectionMode(QTableView.SingleSelection)
        self.view.setSelectionBehavior(QTableView.SelectRows)
        self.view.setColumnHidden(ID, True)

        menu = QMenu(self)
        sortByNameAction = menu.addAction("Sort by &Name")
        sortBySurnameAction = menu.addAction("Sort by &Surname")
        sortByAddressAction = menu.addAction("Sort by &Address")
        sortByZIPAction = menu.addAction("Sort by &ZIP")
        sortByCityAction = menu.addAction("Sort by &City")
        sortByTelNumberAction = menu.addAction("Sort by &TelNumber")
        sortByEmailAction = menu.addAction("Sort by &E_mail")
        sortByIDAction = menu.addAction("Sort by &ID")
        self.ui.sort_button.setMenu(menu)

        self.ui.add_button.clicked.connect(self.add_contact)
        self.ui.save_button.clicked.connect(self.accept)
        self.ui.delete_button.clicked.connect(self.delete)
        sortByNameAction.triggered.connect(lambda: self.sort(Name))
        sortBySurnameAction.triggered.connect(lambda: self.sort(Surname))
        sortByAddressAction.triggered.connect(lambda: self.sort(Address))
        sortByZIPAction.triggered.connect(lambda: self.sort(ZIP))
        sortByCityAction.triggered.connect(lambda: self.sort(City))
        sortByTelNumberAction.triggered.connect(lambda: self.sort(TelNumber))
        sortByEmailAction.triggered.connect(lambda: self.sort(E_mail))
        sortByIDAction.triggered.connect(lambda: self.sort(ID))
        self.ui.add_button.setFocusPolicy(Qt.NoFocus)





        self.view.show()

    def add_contact(self):
        row = self.model.rowCount()
        self.model.insertRow(row)
        index = self.model.index(row, Name)
        self.view.setCurrentIndex(index)
        self.view.edit(index)

    def delete(self):
        index = self.view.currentIndex()
        if not index.isValid():
            return
        self.model.removeRow(index.row())
        self.model.submitAll()
        self.model.select()

    def sort(self, column):
        self.model.setSort(column, Qt.AscendingOrder)
        self.model.select()







if __name__ == "__main__":

    app = qtw.QApplication([])

    filename = os.path.join(os.path.dirname(__file__), "data.db")
    create = not QFile.exists(filename)

    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(filename)
    if not db.open():
        QMessageBox.warning(None, "Reference Data",
                            "Database Error: {0}".format(db.lastError().text()))
        sys.exit(1)

    if create:
        query = QSqlQuery()
        query.exec_("""CREATE TABLE IF NOT EXISTS Data (
                 ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NULL,
                 meno TEXT,
                 priezvisko TEXT,
                 adresa TEXT,
                 PSC INTEGER,
                 mesto TEXT,
                 tel_cislo INTEGER,
                 email TEXT
                 ) """ )



    form = MainWindow()
    form.show()

    sys.exit(app.exec())