import sys, pypyodbc, os
from PyQt6 import QtCore, QtGui, QtWidgets
from form.form import Ui_MainWindow


def db_connect() -> pypyodbc.connect:
    pypyodbc.lowercase = False

    conn = pypyodbc.connect(
        "Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
        rf"Dbq={os.path.dirname(os.path.realpath(__file__))}\data\students_db.accdb;")
    return conn


def get_students_table(cursor :pypyodbc.Cursor):
    cursor.execute("SELECT * FROM Студенты")

    return cursor.fetchall()


def get_faculty_table(cursor :pypyodbc.Cursor):
    cursor.execute("SELECT * FROM Факультеты")

    return cursor.fetchall()


def get_groups_table(cursor :pypyodbc.Cursor):
    cursor.execute("SELECT * FROM Группы")

    return cursor.fetchall()


class App(Ui_MainWindow):
    def __init__(self, MainWindow, conn :pypyodbc.connect) -> None:
        super().__init__()
        self.setupUi(MainWindow)

        self.last_table = 0
        self.last_col = 0
        self.need_reverse = False  

        self.student_data = get_students_table(conn.cursor())
        self.group_data = get_groups_table(conn.cursor())
        self.faculty_data = get_faculty_table(conn.cursor())

        self.set_table_data(self.student_data, self.student_table, True)
        self.set_table_data(self.group_data, self.group_table, True)
        self.set_table_data(self.faculty_data, self.faculty_table, True)

        self.student_search.textChanged.connect(lambda s: self.search(self.student_table, s))
        self.group_search.textChanged.connect(lambda s: self.search(self.group_table, s))
        self.faculty_search.textChanged.connect(lambda s: self.search(self.faculty_table, s))

        
    def search(self, table :QtWidgets.QTableWidget, s):
        table.setCurrentItem(None)

        if not s:
            return

        matching_items = table.findItems(s, QtCore.Qt.MatchFlag.MatchContains)

        if matching_items:
            for item in matching_items:
                item.setSelected(True)
                


    def set_table_data(self, data, table :QtWidgets.QTableWidget, set_header=False):
        table.setRowCount(len(data))

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                new_item = QtWidgets.QTableWidgetItem(str(item))
                table.setItem(i, j, new_item)
        
        header = table.horizontalHeader()      
        for i in range(0, len(data[0])):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
        
        if set_header:
            header.setSectionsClickable(True)
            header.sectionClicked.connect(lambda b: self.sort(data, table, b))
    
    def sort(self, data, table, col):
        self.update_need_reverse(table, col)
        data = sorted(data, 
                    key=lambda item:item[col],
                    reverse=self.need_reverse)
        self.set_table_data(data, table)

        self.last_table = table
        self.last_col = col
    
    def update_need_reverse(self, table, col):
        if table is self.last_table and col is self.last_col and self.need_reverse:
            self.need_reverse = False
        elif table is self.last_table and col is self.last_col:
            self.need_reverse = True
        else:
            self.need_reverse = False


if __name__ == "__main__":
    conn = db_connect()
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = App(MainWindow, conn)
    MainWindow.show()
    sys.exit(app.exec())