from flask import Flask, render_template, request, redirect
from forms.user import RegisterForm, LoginForm
from data.news import News
from data.users import User
from data import db_session

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/main')
def news():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news, title="Главная")


@app.route('/shop', methods=['POST', 'GET'])
def shop():
    if request.method == 'GET':
        return render_template('shop.html', title="Магазин")
    elif request.method == 'POST':
        args = {}
        args['name'] = request.form.get('name')
        args['phone'] = request.form.get('phone')
        args['address'] = request.form.get('address')
        args['delivery'] = request.form.get('delivery')
        
        discount = False
        if request.form.get('ifspecial') == 'yes':
            discount = True

        items = []
        count = 0
        # if the item is selected
        if request.form.get('polo') is not None:
            num = int(request.form.get('polonum'))
            if discount:
                count += num * 6000
            else:
                count += num * 8000
            items.append([f'Поло размера {request.form.get("polo_size")}', num])
        if request.form.get('hoodie') is not None:
            num = int(request.form.get('hoodienum'))
            if discount:
                count += num * 12000
            else:
                count += num * 15000
            items.append([f'Толстовка размера {request.form.get("hoodie_size")}', num])
        if request.form.get('poolover') is not None:
            num = int(request.form.get('poolovernum'))
            if discount:
                count += num * 7000
            else:
                count += num * 9000
            items.append([f'Кофта размера {request.form.get("poolover_size")}', num])
        if request.form.get('cap') is not None:
            num = int(request.form.get('capnum'))
            if discount:
                count += num * 4000
            else:
                count += num * 5000
            items.append([f'Бейсболка размера {request.form.get("cap_size")}', num])
        if request.form.get('backpack') is not None:
            num = int(request.form.get('backpacknum'))
            if discount:
                count += num * 10000
            else:
                count += num * 15000
            items.append(['Рюкзак', num])
        if request.form.get('student_tie') is not None:
            num = int(request.form.get('student_tienum'))
            if discount:
                count += num * 4000
            else:
                count += num * 5000
            items.append(['Галстук ученика', num])
        if request.form.get('scarf') is not None:
            num = int(request.form.get('scarfnum'))
            if discount:
                count += num * 2500
            else:
                count += num * 3000
            items.append(['scarf', num])
        if request.form.get('teacher_tie') is not None:
            num = int(request.form.get('teacher_tienum'))
            if discount:
                count += num * 5000
            else:
                count += num * 7000
            items.append(['Галстук учителя', num])
        if request.form.get('laptop_case') is not None:
            num = int(request.form.get('laptop_casenum'))
            if discount:
                count += num * 4000
            else:
                count += num * 5000
            items.append(['Чехол для ноутбука', num])
        if request.form.get('icon') is not None:
            num = int(request.form.get('iconnum'))
            if discount:
                count += num * 1500
            else:
                count += num * 2000
            items.append(['Значок', num])
        if request.form.get('notebook') is not None:
            num = int(request.form.get('notebooknum'))
            if discount:
                count += num * 1500
            else:
                count += num * 3000
            items.append(['Блокнот', num])

        args['items'] = items
        args['summa'] = count

        return render_template('check.html', **args)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    main()