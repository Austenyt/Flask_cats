import os
import hashlib

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from models import Cat, Breed, Gender, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'


def password_hash(password):
    hash_object = hashlib.sha256(password.encode()).hexdigest()
    return hash_object


@app.route('/')
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
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        if password != password_confirm:
            return render_template('register.html', error='Пароли не совпадают')
        try:
            User.create(
                username=username,
                email=email,
                password_hash=password_hash(password),
            )
            return redirect(url_for('index'))
        except Exception as error:
            return render_template('register.html', error=error)


@app.route('/authorize', methods=['GET', 'POST'])
def authorize():
    if request.method == 'GET':
        return render_template('authorize.html')
    else:
        email = request.form['email']
        password = request.form['password']
        user = User.get_or_none(User.email == email)

        if user:
            if user.password_hash == password_hash(password):
                session['user_id'] = user.id
                session['username'] = user.username
                return redirect(url_for('index'))
            else:
                return render_template('authorize.html', error='Неверный пароль')
        else:
            return render_template('authorize.html', error='Пользователь не найден')


@app.route('/profile', methods=['GET'])
def profile():
    user = User.get_or_none(User.id == session['user_id'])

    return render_template('profile.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)
