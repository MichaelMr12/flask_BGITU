import sqlite3
from appivt import app


def connect_db():
    '''создание соединения с БД'''
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    ''' Вспомогательная функция для создания таблиц БД'''
    db = connect_db()
    with app.open_resource('sql_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addmenu(self, title, url):
        try:
            self.__cur.execute("INSERT INTO  mainmenu VALUES(NULL, ?, ?)", (title, url))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления меню в БД" + str(e))
            return False
        return True


if __name__ == '__main__':
    db = connect_db()
    database = FDataBase(db)
    print(database.addmenu('Главная2', 'index2'))
    pass