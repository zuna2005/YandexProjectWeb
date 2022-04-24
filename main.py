from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/main')
def news():
    return render_template('base.html', title="Главная")


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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')