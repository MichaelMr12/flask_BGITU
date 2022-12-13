from apppri import app
from flask import render_template, request, flash, session, redirect, url_for, abort, g

from apppri.dbpri import connect_db, FDataBase

menu = [{"title": "Начало", "url": "index"},
        {"title": "Главная", "url": "main"},
        {"title": "Помощь", "url": "help"},
        {"title": "О приложении", "url": "about"},
        {"title": "Обратная связь", "url": "callback"},
        {"title": "Авторизация", "url": "login"},
        {"title": "База данных главная", "url": "/db/index_db"}
        ]


def get_db():
    ''' Соединение с БД '''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    '''Закрытие соединения с БД, если оно было установленно'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/db/index_db')
def index_db():
    db = get_db()
    dbase = FDataBase(db)

    return render_template('index_db.html', title='БД', menu=dbase.getMenu())


@app.route('/')
@app.route('/index')
def index():
    best_pri = {'username': 'Макарцев'}

    return render_template('index.html', title='2022 Forever', menu=menu, user=best_pri)


@app.route('/help')
def help():
    return render_template('help.html', title='Помощь', menu=menu)


@app.route('/about')
def about():
    return render_template('help.html', title='C горем попалам ПРИ', menu=menu)


@app.route('/main')
def main():
    return render_template('main.html', menu=menu, title='Главная')


@app.route('/callback', methods=["POST", "GET"])
def callback():
    if request.method == 'POST':
        if len(request.form['username']) > 2 and '@' in request.form['email']:
            flash('Сообщение отправлено', category='success')
        else:
            flash('  Ошибка отправки', category='error')
        print(request.form)
        print(request.form['email'])
    return render_template('callback.html', menu=menu, title="Обратная связь")


@app.route('/db/add_post', methods=["POST", "GET"])
def add_post():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        if len(request.form['name']) > 2 and len(request.form['post']) > 4:
            res = dbase.addPost(request.form['name'], request.form['url'], request.form['post'])
            if not res:
                flash('  Ошибка добавления', category='error')
            else:

                flash('Cтатья добавлена', category='success')
        else:
            flash('  Ошибка добавления', category='error')
    print(dbase.getMenu()[1]['url'])
    return render_template('addpost.html', menu=dbase.getMenu(), title="Добавить статью")


@app.route('/profile/<username>')
def profile(username):
    if 'userlogged' not in session or session['userlogged'] != username:
        abort(401)
    return f"<h1> Привет {username} </h1>"


@app.route('/login', methods=["POST", "GET"])
def login():
    if 'userlogged' in session:
        return redirect(url_for('profile', username=session['userlogged']))
    elif request.method == 'POST' and request.form['username'] == '1' and request.form['psw'] == '1':
        session['userlogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userlogged']))

    return render_template('login.html', title='Авторизация', menu=menu)


@app.errorhandler(404)
def page_404(error):
    return render_template('page404.html', title='Страница не найдена', menu=menu, error=error)
