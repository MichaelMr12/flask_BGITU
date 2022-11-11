import sqlite3
from appist import app
from appist.routes import connect_db


def create_db():
    '''Вспомогательная функция для создания таблиц БД '''
    db = connect_db()
    with app.open_resource('sql_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()
    print('файл создан')
    return True
    pass


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addMenu(self, title, url):
        try:
            self.__cur.execute("INSERT INTO mainmenu VALUES(NULL, ?, ?)", (title, url))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления названий страниц ' + str(e))
            return False
        return True

    def delMenu(self, id=0):
        try:
            if id == 0:
                self.__cur.execute(f"DELETE FROM mainmenu")
            else:
                self.__cur.execute(f"DELETE FROM mainmenu WHERE id=={id}")
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка удаления названий страниц ' + str(e))
            return False
        return True


print(create_db.__doc__)
db = connect_db()
db = FDataBase(db)
#print(db.addMenu('Главная', 'index'))
print(db.delMenu(5))
