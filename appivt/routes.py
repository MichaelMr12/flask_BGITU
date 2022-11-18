import datetime

from appivt import app
from flask import render_template, request, flash, get_flashed_messages, session, redirect, url_for, abort, g

from appivt.bd_exs import connect_db, FDataBase

menu = [{'name': 'Главная', 'url': 'index'}, {'name': 'Блюда', 'url': 'dishes'}, {'name': 'Помощь', 'url': 'help'},
        {'name': 'Контакт', 'url': 'contact'}, {'name': 'Авторизация', 'url': 'login'},
        {'name': 'Главная БД', 'url': '/db/index_db'}]

bd_contact = []

app.permanent_session_lifetime = datetime.timedelta(seconds=120)


def get_db():
    '''соединение с БД, если оно не установленно'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно открыто'''
    if hasattr(g, 'link_db'):
        g.link_db.close()




@app.route('/db/index_db')
def index_db():
    db = get_db()
    database = FDataBase(db)
    #print(db.getMenu())
    return render_template('index_db.html', menu=database.getMenu())

@app.route('/db/post_db', methods=['POST', 'GET'])
def post_db():
    db = get_db()
    database = FDataBase(db)
    if request.method == 'POST':
        if len(request.form['name'])>4 and len(request.form['post'])>10:
            res = database.addPost(request.form['name'], request.form['post'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')
    #print(db.getMenu())

    return render_template('post_db.html', menu=database.getMenu(), title='Добавление статей')


@app.route('/')
@app.route('/index')
def index():
    best_ivt = {'username': 'Шляпкин'}
    favorite_writes = [{'author': {'username': 'Tolkien'},
                        'body': ' Lords of the ring'
                        },
                       {'author': {'username': 'Pushkin'},
                        'body': ' Capitans of the daughter'
                        },
                       {'author': {'username': 'Lermontov'},
                        'body': ' Парус'
                        }]

    return render_template('index.html', title='2022 Forever', user=best_ivt, favorite_writes=favorite_writes,
                           menu=menu)


@app.route('/dishes')
def dish():
    best_user = {'username': 'Николай'}
    favorite_dishes = [{'name': {'dishname': 'Fried chicken'},
                        'ingridients': {'ingr1': 'Meat of chicken',
                                        'ingr2': 'some spicy sauce'},
                        'photo': 'https://hi-news.ru/wp-content/uploads/2020/06/chicken_home_image_one-750x558.jpg'}]

    return render_template('dishes.html', title='2022 Forever', abuser=best_user, favorite_dishes=favorite_dishes,
                           menu=menu)


@app.route('/help')
def help():
    return render_template('help.html', title='Cправка', menu=menu)


def rec(bd, f):
    print(f['username'])
    bd.append({'username': f['username'], 'message': f['message']})


@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
            rec(bd_contact, request.form)
        else:
            flash('Ошибка отправки', category='error')
        print(get_flashed_messages(True))
        print(request.form['username'])
        print(bd_contact)

    return render_template('contact.html', title='Контакты', menu=menu)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'userlogged' in session:
        return redirect(url_for('profile', username=session['userlogged']))
    elif request.method == 'POST' and request.form['username'] == '1' and request.form['psw'] == '2':
        session['userlogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userlogged']))
    return render_template('login.html', title='Авторизация', menu=menu)


@app.route('/profile/<username>')
def profile(username):
    if 'userlogged' not in session or session['userlogged'] != username:
        abort(401)
    return f'<h3>Пользователь : {username}</h3>'


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Все сломалось', menu=menu)
