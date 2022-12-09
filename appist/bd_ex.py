import math
import sqlite3
import time


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

    def getMenu(self):
        try:
            sql = '''SELECT * FROM mainmenu'''
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print('Ошибка чтения из БД')

        return []

    def addfeedback(self, title, text):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO feedback VALUES(NULL,?, ?, ?)", (title, text, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления отзыва ' + str(e))
            return False
        return True

    def addPost(self, title, text, url):
        try:
            self.__cur.execute("SELECT COUNT() as 'count' FROM posts WHERE url LIKE ?", (url,))
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Статья с таким url уже есть!')
                return False
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES(NULL,?, ?, ?, ?)", (title, text, url, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления стать в БД ' + str(e))
            return False
        return True

    def getPost(self, alias):
        try:
            sql = "SELECT title, text FROM posts WHERE url LIKE ? LIMIT 1"
            self.__cur.execute(sql, (alias,))
            res = self.__cur.fetchone()
            if res: return res
        except sqlite3.Error as e:
            print('Ошибка чтения  статьи из БД' + str(e))

        return (False, False)


if __name__ == '__main__':
    from appist import app
    from appist.routes import connect_db

    # print(create_db.__doc__)
    db = connect_db()
    db = FDataBase(db)
    # # print(db.addMenu('Главная БД', 'index_db'))
    # # print(db.addMenu('Отзыв', 'feedback'))
    # print(db.delMenu(13))
    # for i in db.getMenu():
    #     print(i['url'])
    # print(db.addMenu('Добавить статью', 'add_post'))
    # create_db()
