from apppi import app, connect_db
from flask import render_template, url_for, g
from random import choice

menu = [{"name": 'Главная', "url": 'index'}, {"name": 'О программе', "url": 'about'}, {"name": 'Помощь', "url": 'help'}]

def get_db():
    '''Установление соединения с БД'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.teardown_appcontext
def close_db(error):
    'Разрыв соединения с БД'
    print(g.__dict__)
    if hasattr(g, 'link_db'):
        g.link_db.close()
    print(g.__dict__)

@app.route('/')
@app.route('/index')
def index():
    best_pi = {'username': 'Елизавета'}
    print(url_for('static', filename='css/styles.css'))

    return render_template('index.html', title='2022 Forever', user=best_pi, menu=menu)


@app.route('/help')
def help():
    sp = ['PI', '2014', '']
    return render_template('help.html', title=choice(sp), menu=menu)


@app.route('/about')
def about():
    return render_template('about.html', menu=menu)

@app.route('/index_db')

def index_db():
    db = get_db()
    return render_template('index_db.html', menu=[])

