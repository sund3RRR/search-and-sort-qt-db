import sqlite3

conn = sqlite3.connect("data/students.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE Студенты")
cursor.execute("DROP TABLE Группы")
cursor.execute("DROP TABLE Факультеты")
conn.commit()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Студенты(
        Код INTEGER,
        ФИО TEXT,
        Адрес TEXT,
        Телефон INTEGER,
        КодГруппы INTEGER);
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Группы(
        Код INTEGER,
        НазваниеГруппы TEXT,
        Фамилиястаросты TEXT,
        Количество INTEGER,
        КодФакультета INTEGER
    );''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Факультеты(
        Код INTEGER,
        Факультет TEXT,
        Курс INTEGER,
        Количествогрупп INTEGER
    );''')

conn.commit()
cursor.execute('''INSERT INTO Студенты(Код, ФИО, Адрес, Телефон, КодГруппы) VALUES (0, "Иванов Иван Иванович", "Москва", 999, 0)''')  
cursor.execute('''INSERT INTO Группы(Код, НазваниеГруппы, Фамилиястаросты, Количество, КодФакультета) VALUES (0, "ПИ1-2", "Карамзин", 1, 0)''')
cursor.execute('''INSERT INTO Факультеты(Код, Факультет, Курс, Количествогрупп) VALUES (0, "ИИС", 1, 1)''')
conn.commit()