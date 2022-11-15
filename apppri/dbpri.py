import sqlite3
import sys

from apppri import app


def connect_db():
    coon = sqlite3.connect(app.config['DATABASE'])
    coon.row_factory = sqlite3.Row
    return coon


def create_db():
    '''Функция для создания БД'''
    db = connect_db()
    with app.open_resource('sql_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addMenu(self, title, url):
        try:
            self.__cur.execute('INSERT INTO mainmenu VALUES (NULL, ?,?)', (title, url))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления меню в БД ', + str(e))
            return False
        return True

    def delMenu(self, id=0):
        try:
            if id == 0:
                self.__cur.execute('DELETE FROM mainmenu')
            else:
                pass
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка удаления меню в БД ', + str(e))
            return False
        return True
    def getMenu(self, ):
        sql = '''SELECT * FROM mainmenu '''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except :
            print('Ошибка чтения из БД ',)
            return False
        return []



if __name__ == '__main__':
    db = connect_db()
    db = FDataBase(db)
    print('1')
    for k in db.getMenu():
        print(k['id'], k['url'])
        # for i, j in k:
        #     print(i, j)
    #print(db.addMenu('Главная', 'index_bd'))
    #print(db.addMenu('Добавить пост', 'add_post'))
    #print(db.delMenu())
    # print(*sys.path, sep='\n')
    print('2')
