from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/main')
def news():
    return render_template('base.html', title="Главная")


@app.route('/shop')
def shop():
    return render_template('shop.html', title="Магазин")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')