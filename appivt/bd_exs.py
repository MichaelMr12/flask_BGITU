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

    def delmenu(self, id=0):
        try:
            if id == 0:
                self.__cur.execute("DELETE from  mainmenu ")
            else:
                self.__cur.execute(f"DELETE from  mainmenu WHERE id={id}")

            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления меню в БД" + str(e))
            return False
        return True

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = list(self.__cur.fetchall())
            # res = self.__cur.fetchall()
            # for m in res:
            #     print(m['url'])
            #     print(m['title'])
            # #print(*res)
            if res:
                return res
        except:
            print("Ошибка чтения из БД")
        return []


if __name__ == '__main__':
    db = connect_db()
    database = FDataBase(db)
    database.getMenu()
    #print(database.addmenu('Главная БД', 'index_db'))
    # print(database.delmenu(5))
    # for i in database.getMenu().:
    #     print(*i)
    # pass
