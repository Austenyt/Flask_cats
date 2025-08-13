import os

from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
# from flask_login import LoginManager, login_required, current_user, login_user, logout_user

# from forms import RegistrationForm, LoginForm
from models import Cat, Breed, Gender

app = Flask(__name__)


# app.secret_key = 'you_will_never_guess'
# login = LoginManager(app)
# login.login_view = 'login'


@app.route('/')
# @login_required
def index():
    cats = Cat.select().join(Breed).switch(Cat).join(Gender)
    return render_template('cats.html', cats=cats)


@app.route('/add_cat', methods=['GET', 'POST'])
def add_cat():
    if request.method == 'POST':
        name = request.form['name']
        breed = request.form['breed']
        gender = request.form['gender']
        age = request.form['age']
        color = request.form['color']
        weight = request.form['weight']
        temper = request.form['temper']
        description = request.form.get('description')
        has_passport = request.form.get('has_passport') == 'on'
        image = request.files.get('image')
        print(image)
        if image:
            image.save('media/' + image.filename)
            image = 'media/' + image.filename

        Cat.create(
            name=name,
            breed=breed,
            gender=gender,
            age=age,
            color=color,
            weight=weight,
            temper=temper,
            description=description,
            has_passport=has_passport,
            image_path=image,
        )
        return redirect(url_for('index'))
    breeds = Breed.select()
    genders = Gender.select()
    return render_template('add_cat.html', breeds=breeds, genders=genders)


@app.route('/media/<filepath>')
def media(filepath):
    return send_from_directory(directory=os.path.dirname('media/' + filepath),
                               path=os.path.basename('media/' + filepath))


@app.route('/edit_cat/<int:cat_id>', methods=['GET', 'POST'])
def edit_cat(cat_id):
    cat = Cat.get_or_none(Cat.id == cat_id)
    if not cat:
        return redirect(url_for('index'))

    if request.method == 'POST':
        cat.name = request.form['name']

        breed_id = request.form['breed']
        breed_obj = Breed.get_or_none(Breed.id == breed_id)
        cat.breed = breed_obj

        gender_id = request.form['gender']
        gender_obj = Gender.get_or_none(Gender.id == gender_id)
        cat.gender = gender_obj

        cat.age = float(request.form['age'])
        cat.color = request.form['color']
        cat.weight = float(request.form['weight'])
        cat.temper = request.form['temper']
        cat.description = request.form.get('description')
        cat.has_passport = 'has_passport' in request.form
        image = request.files.get('image')
        if image:
            image.save('media/' + image.filename)
            cat.image_path = 'media/' + image.filename
        cat.save()
        return redirect(url_for('index'))

    breeds = Breed.select()
    genders = Gender.select()
    return render_template('edit_cat.html', cat=cat, breeds=breeds, genders=genders)


@app.route('/add_breed', methods=['GET', 'POST'])
def add_breed():
    if request.method == 'POST':
        name = request.form['name']

        Breed.create(
            name=name
        )
        return redirect(url_for('index'))

    return render_template('add_breed.html')


@app.route('/cat/<int:cat_id>', methods=['GET'])
def cat_detail(cat_id):
    cat = Cat.get(Cat.id == cat_id)
    return render_template('cat_detail.html', cat=cat)


@app.route('/delete/<int:cat_id>', methods=['POST'])
def delete_cat(cat_id):
    cat = Cat.get_or_none(Cat.id == cat_id)
    if cat:
        cat.delete_instance()
    return redirect(url_for('index'))


@app.route('/delete_confirm/<int:cat_id>', methods=['GET', 'POST'])
def delete_confirm(cat_id):
    cat = Cat.get_or_none(Cat.id == cat_id)
    if not cat:
        return redirect(url_for('index'))

    if request.method == 'POST':
        cat.delete_instance()
        return redirect(url_for('index'))

    return render_template('delete_confirm.html', cat=cat)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        if password != password_confirm:
            flash('Пароли не совпадают', 'danger')
            return render_template('register.html')

        if User.select().where((User.username == username) | (User.email == email)).exists():
            flash('Пользователь с таким логином или email уже существует', 'danger')
            return render_template('register.html')

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        flash('Регистрация прошла успешно! Войдите в систему.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(username=form.username.data, email=form.email.data)
#         user.set_password(form.password.data)
#         user.save()  # Сохраните пользователя в базе данных
#         flash('Congratulations, you are now a registered user!')
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form)
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.get_or_none(User.username == form.username.data)
#         if user and user.check_password(form.password.data):
#             login_user(user)
#             return redirect(url_for('index'))
#         else:
#             flash('Invalid username or password')
#     return render_template('login.html', title='Login', form=form)
#
#
# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
