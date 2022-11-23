import pypyodbc, os

def my_sort(data : list[list]):
    return sorted(data, key=lambda item:item[1])


def db_connect() -> pypyodbc.Cursor:
    pypyodbc.lowercase = False

    conn = pypyodbc.connect(
        "Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
        rf"Dbq={os.path.dirname(os.path.realpath(__file__))}\data\students_db.accdb;")
    return conn.cursor()


def get_students_table(cursor :pypyodbc.Cursor):
    cursor.execute("SELECT * FROM Студенты")

    return cursor.fetchall

if __name__ == "__main__":
    cursor = db_connect()

    data = get_students_table(cursor)

    print(my_sort(data))