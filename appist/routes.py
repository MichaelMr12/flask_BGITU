import datetime
import sqlite3

from appist import app
from flask import render_template, request, flash, get_flashed_messages, session, redirect, url_for, abort, g

from appist.bd_ex import FDataBase

menu = [{'name': 'Главная', 'url': 'index'}, {'name': 'Помощь', 'url': 'help'},
        {'name': 'Обратная связь', 'url': 'contact'}, {'name': 'Авторизация', 'url': 'login'},
        {'name': 'Главная БД', 'url': '/db/index_db'}]

app.permanent_session_lifetime = datetime.timedelta(seconds=120)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    '''Соединение с БД, если оно еще не установленнно'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно есть'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/db/index_db')
def index_db():
    db = get_db()
    db = FDataBase(db)

    return render_template('index_db.html', title='2022 Forever', menu=db.getMenu())


@app.route('/db/feedback')
def feedback():
    return render_template('index_db.html', title='2022 Forever', menu=[])


@app.route('/')
@app.route('/index')
def index():
    best_ist = {'username': 'Виктория'}
    favorite_writes = [{'author': {'username': 'Tolkien'},
                        'body': ' Lords of the ring'
                        },
                       {'author': {'username': 'Pushkin'},
                        'body': ' Capitans of the daughter'
                        },
                       {'author': {'username': 'Lermontov'},
                        'body': ' Парус'
                        }]

    return render_template('index.html', title='2022 Forever', menu=menu, user=best_ist,
                           favorite_writes=favorite_writes)


@app.route('/help')
def help():
    return render_template('help.html', title=' Помощь', menu=menu)


@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        if len(request.form['username']) >= 2:
            flash('Сообщение отправлено', category='success')
            print(get_flashed_messages(True))
            print(request.form)
            print(request.form['username'])
        else:
            flash("Ошибка отправки", category='error')

    return render_template('contact.html', title=' Контакт', menu=menu)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'userlogged' in session:
        return redirect(url_for('profile', username=session['userlogged']))
    elif request.method == "POST" and request.form['username'] == '1' and request.form['psw'] == '2':
        session['userlogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userlogged']))
    return render_template('login.html', title='Авторизация', menu=menu)


@app.route('/profile/<username>')
def profile(username):
    if 'userlogged' not in session or session['userlogged'] != username:
        abort(401)
    return f"<h1> Пользователь: {username} </h1>"


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Внимание страница не найдена', menu=menu, error=error), 404
